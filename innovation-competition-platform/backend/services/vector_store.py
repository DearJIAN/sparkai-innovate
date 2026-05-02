import os
import json
import logging
import hashlib

logger = logging.getLogger(__name__)

VECTOR_BASE_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    'vector_stores'
)

FAISS_AVAILABLE = False
BM25_AVAILABLE = False

try:
    import faiss
    FAISS_AVAILABLE = True
except ImportError:
    logger.warning('faiss-cpu 未安装，将降级到 BM25 检索')

try:
    from rank_bm25 import BM25Plus
    BM25_AVAILABLE = True
except ImportError:
    try:
        from rank_bm25 import BM25Okapi as BM25Plus
        BM25_AVAILABLE = True
    except ImportError:
        logger.warning('rank-bm25 未安装，将降级到关键词检索')


def _ensure_dir(path):
    os.makedirs(path, exist_ok=True)


def _get_index_path(source_type, source_id):
    return os.path.join(VECTOR_BASE_DIR, f'{source_type}_{source_id}')


def _compute_file_hash(file_path):
    h = hashlib.sha256()
    try:
        with open(file_path, 'rb') as f:
            while True:
                chunk = f.read(8192)
                if not chunk:
                    break
                h.update(chunk)
        return h.hexdigest()
    except Exception:
        return None


def _split_text(text, chunk_size=500, overlap=50):
    if not text:
        return []
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        if chunk.strip():
            chunks.append(chunk.strip())
        start += chunk_size - overlap
    return chunks


def _simple_tokenize(text):
    import re
    try:
        import jieba
        cn_chars = re.findall(r'[\u4e00-\u9fff]+', text)
        en_tokens = re.findall(r'[a-zA-Z0-9]+', text.lower())
        cn_tokens = []
        for seg in cn_chars:
            cn_tokens.extend(jieba.lcut(seg))
        return cn_tokens + en_tokens
    except ImportError:
        tokens = re.findall(r'[\u4e00-\u9fff]|[a-zA-Z0-9]+', text.lower())
        return tokens


class FAISSIndex:
    def __init__(self, index_path):
        self.index_path = index_path
        self.index = None
        self.documents = []
        self.metadatas = []
        self._embeddings = None

    def _get_embeddings(self):
        if self._embeddings is not None:
            return self._embeddings
        try:
            from langchain_openai import OpenAIEmbeddings
            import os
            self._embeddings = OpenAIEmbeddings(
                model=os.getenv('ARK_EMBEDDING_MODEL', 'doubao-embedding'),
                openai_api_key=os.getenv('ARK_API_KEY'),
                openai_api_base=os.getenv('ARK_BASE_URL', 'https://ark.cn-beijing.volces.com/api/v3'),
            )
            return self._embeddings
        except Exception as e:
            logger.warning(f'OpenAI Embeddings 初始化失败: {e}，尝试本地 Embeddings')
        try:
            from langchain_community.embeddings import HuggingFaceEmbeddings
            self._embeddings = HuggingFaceEmbeddings(
                model_name='shibing624/text2vec-base-chinese',
            )
            return self._embeddings
        except Exception as e:
            logger.warning(f'HuggingFace Embeddings 初始化失败: {e}')
            return None

    def build(self, documents, metadatas=None):
        embeddings = self._get_embeddings()
        if embeddings is None:
            return False

        try:
            texts = [doc for doc in documents]
            vector = embeddings.embed_documents(texts)
            import numpy as np
            vectors = np.array(vector, dtype=np.float32)

            dimension = vectors.shape[1]
            self.index = faiss.IndexFlatL2(dimension)
            self.index.add(vectors)
            self.documents = texts
            self.metadatas = metadatas or [{} for _ in texts]
            return True
        except Exception as e:
            logger.error(f'FAISS 索引构建失败: {e}')
            return False

    def search(self, query, top_k=4):
        if self.index is None or not self.documents:
            return []
        embeddings = self._get_embeddings()
        if embeddings is None:
            return []

        try:
            query_vector = embeddings.embed_query(query)
            import numpy as np
            query_vector = np.array([query_vector], dtype=np.float32)
            distances, indices = self.index.search(query_vector, min(top_k, len(self.documents)))
            results = []
            for i, idx in enumerate(indices[0]):
                if idx < len(self.documents):
                    results.append({
                        'content': self.documents[idx],
                        'metadata': self.metadatas[idx] if idx < len(self.metadatas) else {},
                        'score': float(distances[0][i]),
                    })
            return results
        except Exception as e:
            logger.error(f'FAISS 检索失败: {e}')
            return []

    def save(self):
        if self.index is None:
            return False
        try:
            _ensure_dir(self.index_path)
            import faiss as faiss_mod
            faiss_mod.write_index(self.index, os.path.join(self.index_path, 'index.faiss'))
            with open(os.path.join(self.index_path, 'documents.json'), 'w', encoding='utf-8') as f:
                json.dump({
                    'documents': self.documents,
                    'metadatas': self.metadatas,
                }, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            logger.error(f'FAISS 索引保存失败: {e}')
            return False

    def load(self):
        try:
            index_file = os.path.join(self.index_path, 'index.faiss')
            docs_file = os.path.join(self.index_path, 'documents.json')
            if not os.path.exists(index_file) or not os.path.exists(docs_file):
                return False
            import faiss as faiss_mod
            self.index = faiss_mod.read_index(index_file)
            with open(docs_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.documents = data.get('documents', [])
            self.metadatas = data.get('metadatas', [{} for _ in self.documents])
            return True
        except Exception as e:
            logger.error(f'FAISS 索引加载失败: {e}')
            return False


class BM25Index:
    def __init__(self, index_path):
        self.index_path = index_path
        self.bm25 = None
        self.documents = []
        self.metadatas = []
        self.tokenized_corpus = []

    def build(self, documents, metadatas=None):
        try:
            self.documents = documents
            self.metadatas = metadatas or [{} for _ in documents]
            self.tokenized_corpus = [_simple_tokenize(doc) for doc in documents]
            self.bm25 = BM25Plus(self.tokenized_corpus)
            return True
        except Exception as e:
            logger.error(f'BM25 索引构建失败: {e}')
            return False

    def search(self, query, top_k=4):
        if self.bm25 is None or not self.documents:
            return []
        try:
            tokenized_query = _simple_tokenize(query)
            scores = self.bm25.get_scores(tokenized_query)
            top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]
            results = []
            for idx in top_indices:
                if scores[idx] > -1:
                    results.append({
                        'content': self.documents[idx],
                        'metadata': self.metadatas[idx] if idx < len(self.metadatas) else {},
                        'score': float(scores[idx]),
                    })
            return results
        except Exception as e:
            logger.error(f'BM25 检索失败: {e}')
            return []

    def save(self):
        try:
            _ensure_dir(self.index_path)
            with open(os.path.join(self.index_path, 'bm25_data.json'), 'w', encoding='utf-8') as f:
                json.dump({
                    'documents': self.documents,
                    'metadatas': self.metadatas,
                }, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            logger.error(f'BM25 索引保存失败: {e}')
            return False

    def load(self):
        try:
            docs_file = os.path.join(self.index_path, 'bm25_data.json')
            if not os.path.exists(docs_file):
                return False
            with open(docs_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.documents = data.get('documents', [])
            self.metadatas = data.get('metadatas', [{} for _ in self.documents])
            self.tokenized_corpus = [_simple_tokenize(doc) for doc in self.documents]
            self.bm25 = BM25Plus(self.tokenized_corpus)
            return True
        except Exception as e:
            logger.error(f'BM25 索引加载失败: {e}')
            return False


class KeywordIndex:
    def __init__(self, index_path):
        self.index_path = index_path
        self.documents = []
        self.metadatas = []

    def build(self, documents, metadatas=None):
        self.documents = documents
        self.metadatas = metadatas or [{} for _ in documents]
        return True

    def search(self, query, top_k=4):
        if not self.documents:
            return []
        query_terms = set(_simple_tokenize(query))
        scored = []
        for i, doc in enumerate(self.documents):
            doc_terms = set(_simple_tokenize(doc))
            overlap = len(query_terms & doc_terms)
            if overlap > 0:
                scored.append((i, overlap))
        scored.sort(key=lambda x: x[1], reverse=True)
        results = []
        for idx, score in scored[:top_k]:
            results.append({
                'content': self.documents[idx],
                'metadata': self.metadatas[idx] if idx < len(self.metadatas) else {},
                'score': float(score),
            })
        return results

    def save(self):
        try:
            _ensure_dir(self.index_path)
            with open(os.path.join(self.index_path, 'keyword_data.json'), 'w', encoding='utf-8') as f:
                json.dump({
                    'documents': self.documents,
                    'metadatas': self.metadatas,
                }, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            logger.error(f'关键词索引保存失败: {e}')
            return False

    def load(self):
        try:
            docs_file = os.path.join(self.index_path, 'keyword_data.json')
            if not os.path.exists(docs_file):
                return False
            with open(docs_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.documents = data.get('documents', [])
            self.metadatas = data.get('metadatas', [{} for _ in self.documents])
            return True
        except Exception as e:
            logger.error(f'关键词索引加载失败: {e}')
            return False


def index_documents(source_type, source_id, parsed_results, chunk_size=500, overlap=50):
    index_path = _get_index_path(source_type, source_id)
    all_chunks = []
    all_metadatas = []
    skipped_details = []

    for result in parsed_results:
        if result['status'] != 'success' or not result.get('content'):
            skipped_details.append({
                'file_name': result['file_name'],
                'reason': result.get('reason', '内容为空或解析失败'),
            })
            continue

        chunks = _split_text(result['content'], chunk_size, overlap)
        for j, chunk in enumerate(chunks):
            all_chunks.append(chunk)
            all_metadatas.append({
                'file_id': result['file_id'],
                'file_name': result['file_name'],
                'material_type': result.get('material_type'),
                'chunk_index': j,
            })

    if not all_chunks:
        return {
            'success': False,
            'engine': 'none',
            'indexed_chunks': 0,
            'skipped_details': skipped_details,
            'message': '没有可索引的文本内容',
        }

    engine = 'none'
    index_obj = None

    if FAISS_AVAILABLE:
        faiss_idx = FAISSIndex(index_path)
        if faiss_idx.build(all_chunks, all_metadatas):
            if faiss_idx.save():
                engine = 'faiss'
                index_obj = faiss_idx
                logger.info(f'FAISS 索引构建成功: {source_type}_{source_id}, {len(all_chunks)} chunks')

    if engine == 'none' and BM25_AVAILABLE:
        bm25_idx = BM25Index(index_path)
        if bm25_idx.build(all_chunks, all_metadatas):
            if bm25_idx.save():
                engine = 'bm25'
                index_obj = bm25_idx
                logger.info(f'BM25 索引构建成功: {source_type}_{source_id}, {len(all_chunks)} chunks')

    if engine == 'none':
        kw_idx = KeywordIndex(index_path)
        if kw_idx.build(all_chunks, all_metadatas):
            if kw_idx.save():
                engine = 'keyword'
                index_obj = kw_idx
                logger.info(f'关键词索引构建成功: {source_type}_{source_id}, {len(all_chunks)} chunks')

    return {
        'success': engine != 'none',
        'engine': engine,
        'indexed_chunks': len(all_chunks),
        'skipped_details': skipped_details,
        'index_path': index_path,
        'message': f'索引构建完成，使用 {engine} 引擎，共 {len(all_chunks)} 个文本块' if engine != 'none' else '所有索引引擎均不可用',
    }


def search_documents(source_type, source_id, query, top_k=4):
    index_path = _get_index_path(source_type, source_id)

    if FAISS_AVAILABLE:
        faiss_idx = FAISSIndex(index_path)
        if faiss_idx.load():
            results = faiss_idx.search(query, top_k)
            if results:
                return {'engine': 'faiss', 'results': results}

    if BM25_AVAILABLE:
        bm25_idx = BM25Index(index_path)
        if bm25_idx.load():
            results = bm25_idx.search(query, top_k)
            if results:
                return {'engine': 'bm25', 'results': results}

    kw_idx = KeywordIndex(index_path)
    if kw_idx.load():
        results = kw_idx.search(query, top_k)
        if results:
            return {'engine': 'keyword', 'results': results}

    return {'engine': 'none', 'results': []}


def index_exists(source_type, source_id):
    index_path = _get_index_path(source_type, source_id)
    faiss_file = os.path.join(index_path, 'index.faiss')
    bm25_file = os.path.join(index_path, 'bm25_data.json')
    kw_file = os.path.join(index_path, 'keyword_data.json')
    return os.path.exists(faiss_file) or os.path.exists(bm25_file) or os.path.exists(kw_file)


def delete_index(source_type, source_id):
    import shutil
    index_path = _get_index_path(source_type, source_id)
    if os.path.exists(index_path):
        try:
            shutil.rmtree(index_path)
            return True
        except Exception as e:
            logger.error(f'删除索引失败: {e}')
            return False
    return True


def get_index_info(source_type, source_id):
    index_path = _get_index_path(source_type, source_id)
    info = {
        'exists': False,
        'engine': 'none',
        'path': index_path,
    }

    if os.path.exists(os.path.join(index_path, 'index.faiss')):
        info['exists'] = True
        info['engine'] = 'faiss'
    elif os.path.exists(os.path.join(index_path, 'bm25_data.json')):
        info['exists'] = True
        info['engine'] = 'bm25'
    elif os.path.exists(os.path.join(index_path, 'keyword_data.json')):
        info['exists'] = True
        info['engine'] = 'keyword'

    if info['exists']:
        docs_file = os.path.join(index_path, 'documents.json')
        if not os.path.exists(docs_file):
            docs_file = os.path.join(index_path, 'bm25_data.json')
        if not os.path.exists(docs_file):
            docs_file = os.path.join(index_path, 'keyword_data.json')
        if os.path.exists(docs_file):
            try:
                with open(docs_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                info['chunk_count'] = len(data.get('documents', []))
            except Exception:
                pass

    return info
