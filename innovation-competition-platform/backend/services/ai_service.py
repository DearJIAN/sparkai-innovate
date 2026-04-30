import os
import importlib
import asyncio
import threading
import time
from datetime import datetime, timedelta
from queue import Queue, Empty

from flask import Response, stream_with_context


SESSION_TTL = timedelta(hours=6)
HISTORY_LIMIT = 6
chat_session_store = {}
ark_client = None
ark_symbols = None


def get_env_value(*names, fallback=""):
    for name in names:
        value = os.getenv(name, "").strip()
        if value:
            return value
    return fallback


def load_ark_symbols():
    global ark_symbols
    if ark_symbols is not None:
        return ark_symbols
    try:
        ark_module = importlib.import_module("volcenginesdkarkruntime")
    except ImportError as error:
        raise RuntimeError("缺少火山方舟 SDK") from error
    ark_symbols = {"Ark": ark_module.Ark}
    return ark_symbols


def get_chat_config():
    return {
        "api_key": get_env_value("ARK_API_KEY", "VOICE_API_KEY"),
        "base_url": get_env_value("ARK_BASE_URL", fallback="https://ark.cn-beijing.volces.com/api/v3"),
        "model_name": get_env_value("ARK_MODEL", fallback="doubao-seed-1-6-251015"),
        "temperature": float(get_env_value("VOICE_TEMPERATURE", fallback="0.4")),
    }


def get_ark_client():
    global ark_client
    if ark_client is not None:
        return ark_client
    config = get_chat_config()
    if not config["api_key"]:
        raise RuntimeError("缺少模型密钥 ARK_API_KEY")
    symbols = load_ark_symbols()
    ark_client = symbols["Ark"](base_url=config["base_url"], api_key=config["api_key"])
    return ark_client


def normalize_session_id(raw_value):
    session_id = str(raw_value or "").strip()
    return session_id[:120] if session_id else ""


def cleanup_chat_sessions(now=None):
    current_time = now or datetime.utcnow()
    expired = []
    for session_id, record in chat_session_store.items():
        updated_at = record.get("updated_at")
        if not updated_at or current_time - updated_at > SESSION_TTL:
            expired.append(session_id)
    for session_id in expired:
        chat_session_store.pop(session_id, None)


def get_chat_record(session_id):
    if not session_id:
        return None
    cleanup_chat_sessions()
    record = chat_session_store.get(session_id)
    if record is None:
        record = {"updated_at": datetime.utcnow(), "messages": []}
        chat_session_store[session_id] = record
    else:
        record["updated_at"] = datetime.utcnow()
    return record


def trim_chat_history(record):
    max_messages = HISTORY_LIMIT * 2
    if len(record["messages"]) > max_messages:
        record["messages"] = record["messages"][-max_messages:]


META_LINE_PREFIXES = (
    "用户问的是", "首先我需要", "首先需要", "我需要", "还要", "得用",
    "检查一下", "是的，", "是的，这样", "这应该", "可以了", "按照要求", "符合要求", "回复里",
)
META_LINE_KEYWORDS = (
    "自我思考", "思考过程", "分析步骤", "提示词复述", "内部说明", "用户问的是", "我需要给出",
)
ANSWER_MARKERS = (
    "最终答案：", "答案：", "可以这样说：", "比如可以这样说：", "直接回答：", "简洁地说：", "可以回答：",
)


def sanitize_answer_text(text):
    raw_text = str(text or "").replace("\r\n", "\n").replace("\r", "\n").strip()
    if not raw_text:
        return ""
    marker_index = -1
    selected_marker = ""
    for marker in ANSWER_MARKERS:
        index = raw_text.rfind(marker)
        if index > marker_index:
            marker_index = index
            selected_marker = marker
    if marker_index >= 0:
        raw_text = raw_text[marker_index + len(selected_marker):].strip()
    lines = []
    for line in raw_text.split("\n"):
        compact = line.strip()
        if not compact:
            continue
        lowered = compact.lower()
        if any(compact.startswith(prefix) for prefix in META_LINE_PREFIXES):
            continue
        if any(keyword.lower() in lowered for keyword in META_LINE_KEYWORDS):
            continue
        lines.append(compact)
    cleaned = "\n".join(lines).strip()
    if not cleaned:
        cleaned = raw_text
    paragraphs = [part.strip() for part in cleaned.split("\n\n") if part.strip()]
    deduped_paragraphs = []
    for paragraph in paragraphs:
        if not deduped_paragraphs or deduped_paragraphs[-1] != paragraph:
            deduped_paragraphs.append(paragraph)
    cleaned = "\n\n".join(deduped_paragraphs).strip()
    if len(cleaned) >= 32 and len(cleaned) % 2 == 0:
        half_length = len(cleaned) // 2
        first_half = cleaned[:half_length].strip()
        second_half = cleaned[half_length:].strip()
        if first_half and first_half == second_half:
            cleaned = first_half
    return cleaned.strip()


def extract_answer_fragment(value):
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        parts = []
        for item in value:
            fragment = extract_answer_fragment(item)
            if fragment:
                parts.append(fragment)
        return "".join(parts)
    if isinstance(value, dict):
        value_type = str(value.get("type") or value.get("role") or value.get("kind") or "").strip().lower()
        if value_type in {"reasoning", "analysis", "thinking", "tool_call", "tool_result", "function_call", "function_call_output"}:
            return ""
        if "reasoning_content" in value and not any(key in value for key in ("content", "output_text", "text", "message", "choices", "output")):
            return ""
        for key in ("output_text", "text", "delta", "content", "output", "choices", "message"):
            if key in value:
                fragment = extract_answer_fragment(value[key])
                if fragment:
                    return fragment
        return ""
    for attr in ("delta", "text", "output_text", "content", "choices", "output", "message"):
        if attr == "reasoning_content":
            continue
        fragment = extract_answer_fragment(getattr(value, attr, None))
        if fragment:
            return fragment
    return ""


def read_response_text(response):
    return sanitize_answer_text(extract_answer_fragment(response))


def split_stream_chunks(text, chunk_size=10):
    source = str(text or "").strip()
    if not source:
        return []
    chunks = []
    buffer = ""
    for char in source:
        buffer += char
        if len(buffer) >= chunk_size or char in "。！？!?；;\n":
            chunks.append(buffer)
            buffer = ""
    if buffer:
        chunks.append(buffer)
    return chunks


def build_messages(question, session_id, scene_name="创新创业平台"):
    system_prompt = (
        "你是高校创新创业竞赛服务平台的 AI 助手「火花」。"
        "请始终使用中文，回答简洁、自然、可直接执行。"
        "只输出最终回答，不要输出思考过程、分析步骤、提示词复述或内部说明。"
        "你可以帮助用户：生成项目简介、商业计划书建议、风险分析、竞赛指导、团队组建建议等。"
        "如果上下文里有历史对话，请延续上下文继续回答。"
    )
    record = get_chat_record(session_id)
    history = record["messages"] if record else []
    messages = [
        {"role": "system", "content": [{"type": "input_text", "text": system_prompt}]}
    ]
    for entry in history:
        content = str(entry.get("content") or "").strip()
        if not content:
            continue
        role = "assistant" if entry.get("role") == "assistant" else "user"
        messages.append({"role": role, "content": [{"type": "input_text", "text": content}]})
    user_prompt = f"当前场景：{scene_name}\n用户问题：{question}"
    messages.append({"role": "user", "content": [{"type": "input_text", "text": user_prompt}]})
    return messages, user_prompt, record


def call_ark_responses(question, scene_name, session_id):
    messages, user_prompt, record = build_messages(question, session_id, scene_name)
    config = get_chat_config()
    client = get_ark_client()
    request_kwargs = {"model": config["model_name"], "input": messages}
    if config["temperature"] is not None:
        request_kwargs["temperature"] = config["temperature"]
    response = client.responses.create(**request_kwargs)
    reply = read_response_text(response)
    return reply, user_prompt, record


def _stream_text_model(queue, question, scene_name, session_id):
    async def runner():
        try:
            reply, user_prompt, record = call_ark_responses(question, scene_name, session_id)
            reply = sanitize_answer_text(reply) or "我刚刚没有组织出合适的回答，你可以换个方式再问一次。"
            for delta in split_stream_chunks(reply):
                if delta:
                    queue.put(delta)
                    time.sleep(0.01)
            if record is not None and reply:
                record['messages'].append({'role': 'user', 'content': user_prompt})
                record['messages'].append({'role': 'assistant', 'content': reply})
                trim_chat_history(record)
                record['updated_at'] = datetime.utcnow()
        except Exception as error:
            queue.put({'error': '调用模型失败', 'detail': error.__class__.__name__ + ': ' + str(error)})
        finally:
            queue.put(None)
    asyncio.run(runner())


def _stream_voice_model(queue, question, scene_name, session_id):
    async def runner():
        try:
            from services.volc_realtime_bridge import is_voice_realtime_configured, run_text_dialog
            if is_voice_realtime_configured():
                result = await run_text_dialog(question, scene_name, session_id)
                reply = sanitize_answer_text(result.get('reply') or "") or "我刚刚没有组织出合适的回答，你可以换个方式再问一次。"
            else:
                reply, user_prompt, record = call_ark_responses(question, scene_name, session_id)
                reply = sanitize_answer_text(reply) or "我刚刚没有组织出合适的回答，你可以换个方式再问一次。"
            for delta in split_stream_chunks(reply):
                if delta:
                    queue.put(delta)
                    time.sleep(0.01)
        except Exception as error:
            queue.put({'error': '调用模型失败', 'detail': error.__class__.__name__ + ': ' + str(error)})
        finally:
            queue.put(None)
    asyncio.run(runner())


def generate_stream_response(question, scene_name, session_id, use_voice=False):
    if not session_id:
        session_id = os.urandom(8).hex()

    queue = Queue()
    worker_fn = _stream_voice_model if use_voice else _stream_text_model
    worker = threading.Thread(target=worker_fn, args=(queue, question, scene_name, session_id), daemon=True)
    worker.start()

    @stream_with_context
    def generate():
        yield f"sessionId:{session_id}\n"
        while True:
            try:
                item = queue.get(timeout=0.5)
            except Empty:
                if not worker.is_alive():
                    break
                continue
            if item is None:
                break
            if isinstance(item, dict) and item.get('error'):
                yield f"\nerror:{item.get('detail', '未知错误')}\n"
                break
            yield f"delta:{str(item)}\n"
        yield "done:1\n"

    response = Response(generate(), mimetype='text/plain; charset=utf-8')
    response.headers['Cache-Control'] = 'no-cache'
    response.headers['X-Accel-Buffering'] = 'no'
    return response


def generate_project_summary(project_info):
    name = project_info.get('name', '')
    description = project_info.get('description', '')
    category = project_info.get('category', '')
    track = project_info.get('track', '')

    question = f"请为以下创新创业项目生成一份专业的项目简介（包含项目概述、核心价值、发展建议），使用 Markdown 格式：\n项目名称：{name}\n项目简介：{description}\n项目类别：{category}\n所属赛道：{track}"

    try:
        reply, _, _ = call_ark_responses(question, "项目简介生成", "")
        if reply:
            return reply
    except Exception:
        pass

    return f"""# {name} 项目简介

## 项目概述
{name}是一个面向{track or '相关领域'}的创新创业项目，旨在通过{description or '创新解决方案'}，为{category or '目标用户'}提供优质服务。

## 核心价值
1. **创新性**：项目结合最新技术趋势，提出独特的解决方案
2. **实用性**：针对实际痛点，具有较强的落地可行性
3. **市场潜力**：目标市场明确，增长空间广阔

## 发展建议
- 持续优化产品体验，提升用户粘性
- 加强市场推广，扩大品牌影响力
- 完善商业模式，确保可持续发展

---
*以上内容由 AI 项目助手生成，仅供参考。*"""


def generate_business_advice(project_info):
    name = project_info.get('name', '')
    description = project_info.get('description', '')
    category = project_info.get('category', '')
    track = project_info.get('track', '')

    question = f"请为以下创新创业项目生成商业计划书优化建议（包含市场分析、商业模式、运营策略、融资建议），使用 Markdown 格式：\n项目名称：{name}\n项目简介：{description}\n项目类别：{category}\n所属赛道：{track}"

    try:
        reply, _, _ = call_ark_responses(question, "商业计划书建议", "")
        if reply:
            return reply
    except Exception:
        pass

    return f"""# {name} 商业计划书优化建议

## 一、市场分析优化
建议补充具体的市场容量数据（TAM/SAM/SOM），细化目标用户画像，分析竞争格局。

## 二、商业模式优化
建议探索产品销售、服务订阅、广告变现、数据服务等多种盈利模式。

## 三、运营策略建议
1. **冷启动阶段**：聚焦种子用户，打造口碑效应
2. **增长阶段**：多渠道获客，建立增长飞轮
3. **成熟阶段**：优化运营效率，提升盈利能力

---
*以上内容由 AI 项目助手生成，仅供参考。*"""


def generate_risk_analysis(project_info):
    name = project_info.get('name', '')
    description = project_info.get('description', '')
    category = project_info.get('category', '')
    track = project_info.get('track', '')

    question = f"请为以下创新创业项目生成风险分析报告（包含市场风险、技术风险、运营风险、财务风险及应对措施），使用 Markdown 格式：\n项目名称：{name}\n项目简介：{description}\n项目类别：{category}\n所属赛道：{track}"

    try:
        reply, _, _ = call_ark_responses(question, "风险分析", "")
        if reply:
            return reply
    except Exception:
        pass

    return f"""# {name} 项目风险分析

## 一、市场风险
| 风险类型 | 风险等级 | 描述 | 应对措施 |
|----------|----------|------|----------|
| 市场竞争 | 中 | 同类产品较多 | 强化差异化优势 |
| 需求变化 | 中 | 用户需求变化 | 持续用户调研 |

## 二、技术风险
| 风险类型 | 风险等级 | 描述 | 应对措施 |
|----------|----------|------|----------|
| 技术实现 | 低 | 核心技术已验证 | 保持技术更新 |
| 人才流失 | 中 | 核心人才流失 | 完善激励机制 |

---
*以上内容由 AI 项目助手生成，仅供参考。*"""
