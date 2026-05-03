import os
import json
import threading
import time
from datetime import datetime, timedelta
from queue import Queue, Empty

from flask import Response, stream_with_context


SESSION_TTL = timedelta(hours=6)
HISTORY_LIMIT = 6
chat_session_store = {}
_llm_instance = None


def get_env_value(*names, fallback=""):
    for name in names:
        value = os.getenv(name, "").strip()
        if value:
            return value
    return fallback


def get_chat_config():
    return {
        "api_key": get_env_value("GLM_API_KEY", "ARK_API_KEY", "VOICE_API_KEY"),
        "base_url": get_env_value("GLM_BASE_URL", "ARK_BASE_URL", fallback="https://dashscope.aliyuncs.com/compatible-mode/v1"),
        "model_name": get_env_value("GLM_MODEL", "ARK_MODEL", fallback="qwen-mt-flash"),
        "temperature": float(get_env_value("VOICE_TEMPERATURE", fallback="0.4")),
    }


def get_llm():
    global _llm_instance
    if _llm_instance is not None:
        return _llm_instance
    try:
        from langchain_openai import ChatOpenAI
        config = get_chat_config()
        _llm_instance = ChatOpenAI(
            model_name=config["model_name"],
            openai_api_key=config["api_key"],
            openai_api_base=config["base_url"],
            temperature=config["temperature"],
            max_tokens=4096,
            timeout=120,
            request_timeout=120,
        )
        return _llm_instance
    except Exception as e:
        raise RuntimeError(f"LLM 初始化失败: {e}")


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


SYSTEM_PROMPT = (
    "你是高校创新创业竞赛服务平台的 AI 助手「火花」。"
    "请始终使用中文，回答简洁、自然、可直接执行。"
    "只输出最终回答，不要输出思考过程、分析步骤、提示词复述或内部说明。"
    "\n\n【重要规则】"
    "\n1. 当用户问'你可以做什么'或类似问题时，根据用户角色列出对应功能："
    "\n   - 学生：智能引航（模糊指令跳转页面）、项目创意生成、模拟路演答辩、AI材料问答、商业计划书体检、路演稿生成、智能竞赛推荐"
    "\n   - 老师：智能引航、批量审核助手、智能反馈生成、AI材料问答、商业计划书体检、评审辅助、模拟路演答辩"
    "\n   - 评委：智能引航、评审意见草稿、评分一致性检查、AI材料问答、商业计划书体检、评审辅助"
    "\n   - 管理员：所有功能"
    "\n2. 当用户要求'生成项目简介/简历/创意'或'如何组建团队'等需要具体信息的问题时，你必须先追问用户的关键信息（如项目方向、技术领域、团队规模等），等用户回复后再生成具体内容。不要在缺少信息时直接编造。"
    "\n3. 回答时使用自然流畅的中文，可以适当使用加粗强调关键词，但不要过度使用标题符号。"
)


ROLE_MAP = {'student': '学生', 'teacher': '老师', 'judge': '评委', 'admin': '管理员'}


def build_langchain_messages(question, session_id, scene_name="创新创业平台", user_role='student'):
    from langchain_core.messages import HumanMessage, AIMessage

    role_desc = ROLE_MAP.get(user_role, '学生')
    record = get_chat_record(session_id)
    history = record["messages"] if record else []

    messages = []

    for entry in history:
        content = str(entry.get("content") or "").strip()
        if not content:
            continue
        entry_role = entry.get("role")
        if entry_role == "assistant":
            messages.append(AIMessage(content=content))
        else:
            messages.append(HumanMessage(content=content))

    user_prompt = f"{SYSTEM_PROMPT}\n\n当前用户角色：{role_desc}\n当前场景：{scene_name}\n用户问题：{question}"
    messages.append(HumanMessage(content=user_prompt))

    return messages, user_prompt, record


def call_llm_chat(question, scene_name, session_id, user_role='student'):
    llm = get_llm()
    messages, user_prompt, record = build_langchain_messages(question, session_id, scene_name, user_role)
    response = llm.invoke(messages)
    reply = sanitize_answer_text(response.content) if response.content else ""
    return reply, user_prompt, record


def _stream_text_model(queue, question, scene_name, session_id):
    try:
        reply, user_prompt, record = call_llm_chat(question, scene_name, session_id)
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


def _stream_voice_model(queue, question, scene_name, session_id):
    try:
        from services.volc_realtime_bridge import is_voice_realtime_configured, run_text_dialog
        if is_voice_realtime_configured():
            import asyncio
            result = asyncio.run(run_text_dialog(question, scene_name, session_id))
            reply = sanitize_answer_text(result.get('reply') or "") or "我刚刚没有组织出合适的回答，你可以换个方式再问一次。"
        else:
            reply, user_prompt, record = call_llm_chat(question, scene_name, session_id)
            reply = sanitize_answer_text(reply) or "我刚刚没有组织出合适的回答，你可以换个方式再问一次。"
        for delta in split_stream_chunks(reply):
            if delta:
                queue.put(delta)
                time.sleep(0.01)
    except Exception as error:
        queue.put({'error': '调用模型失败', 'detail': error.__class__.__name__ + ': ' + str(error)})
    finally:
        queue.put(None)


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
        reply, _, _ = call_llm_chat(question, "项目简介生成", "")
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


INTENT_PROMPT = """你是高校创新创业竞赛服务平台的意图识别引擎。根据用户消息判断意图，返回 JSON。

可用意图：
- navigate：用户想跳转到某个页面（如"我想报名"、"看我的项目"、"去竞赛广场"）
- mock_defense：用户明确要求模拟路演答辩（如"模拟答辩"、"练习路演"、"评委提问练习"）
- batch_review：用户明确要求批量审核项目（如"帮我批量审核"、"审核所有项目"）
- smart_feedback：用户明确要求生成审核反馈（如"给这个项目写审核反馈"、"生成反馈意见"）
- review_draft：用户明确要求生成评审草稿（如"帮我写评审意见草稿"、"生成评审草稿"）
- score_check：用户明确要求检查评分一致性（如"检查评分一致性"、"评分和评价矛盾吗"）
- chat：普通对话（包括所有其他情况，如"生成项目简介"、"如何组建团队"、"你可以做什么"、"竞赛有哪些赛道"等，这些都应该走普通对话，由AI先追问再回答）

重要规则：
- "帮我生成项目简介/简历"、"如何组建团队"、"有什么项目方向"等生成类问题，必须归类为 chat，不要归类为 project_idea
- 这些问题需要AI先追问用户的具体需求，等用户回复后再生成内容
- 只有用户非常明确地要求使用某个智能体功能时，才归类到对应意图

用户角色：{role}
用户消息：{message}

只返回 JSON，格式：{{"intent": "意图名", "params": {{}}}}
可能的 params：
- navigate: {{"route": "/competitions", "label": "竞赛广场"}}
- mock_defense: {{"question_type": "general"}}
- batch_review: {{}}
- smart_feedback: {{"feedback_type": "modify"}}
- review_draft: {{}}
- score_check: {{}}
- chat: {{}}"""

NAVIGATE_KEYWORDS = [
    '报名', '我想报名', '我要报名', '参加比赛', '竞赛广场', '看竞赛', '找竞赛',
    '我的项目', '看看项目', '我的赛事', '我的报名', '报名状态', '审核结果',
    '创建项目', '新建项目', '指导项目', '项目审核', '待评审', '评审记录',
    '用户管理', '竞赛管理', '报名管理', '评审管理', '训练营', '课程',
    '首页', '主页', '回到首页', '工作台', '仪表盘', 'AI助手',
]


def _quick_detect_navigate(message):
    msg = message.lower()
    for kw in NAVIGATE_KEYWORDS:
        if kw in msg:
            return True
    return False


def detect_intent(message, role='student'):
    if _quick_detect_navigate(message):
        return 'navigate', {}

    record = get_chat_record('')
    llm = get_llm()
    from langchain_core.messages import HumanMessage
    prompt = INTENT_PROMPT.format(role=role, message=message)
    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        cleaned = response.content.strip()
        if cleaned.startswith('```'):
            cleaned = cleaned.split('\n', 1)[-1]
        if cleaned.endswith('```'):
            cleaned = cleaned.rsplit('```', 1)[0]
        cleaned = cleaned.strip()
        result = json.loads(cleaned)
        intent = result.get('intent', 'chat')
        params = result.get('params', {})
        return intent, params
    except Exception:
        return 'chat', {}


def _has_conversation_history(session_id):
    if not session_id:
        return False
    record = chat_session_store.get(session_id)
    if not record:
        return False
    return len(record.get('messages', [])) > 0


def _stream_unified_model(queue, message, role, scene_name, session_id):
    try:
        has_history = _has_conversation_history(session_id)

        if has_history:
            reply, user_prompt, record = call_llm_chat(message, scene_name, session_id, user_role=role)
            if not reply:
                reply = '我刚刚没有组织出合适的回答，你可以换个方式再问一次。'
            if record is not None:
                record['messages'].append({'role': 'user', 'content': user_prompt})
                record['messages'].append({'role': 'assistant', 'content': reply})
                trim_chat_history(record)
                record['updated_at'] = datetime.utcnow()
            queue.put({'header': 'type:chat\n'})
            for delta in split_stream_chunks(reply):
                if delta:
                    queue.put(delta)
                    time.sleep(0.02)
        else:
            intent, params = detect_intent(message, role)

            if intent == 'navigate':
                from services.langchain_service import smart_navigate
                nav_result = smart_navigate(message, role)
                reply = nav_result.get('reply', '好的~')
                nav_json = json.dumps(nav_result, ensure_ascii=False)
                queue.put({'header': f'type:navigate\nnavigate:{nav_json}\n'})
                for delta in split_stream_chunks(reply):
                    if delta:
                        queue.put(delta)
                        time.sleep(0.02)
                record = get_chat_record(session_id)
                if record is not None:
                    record['messages'].append({'role': 'user', 'content': message})
                    record['messages'].append({'role': 'assistant', 'content': reply})
                    record['updated_at'] = datetime.utcnow()

            elif intent in ('mock_defense', 'batch_review', 'smart_feedback', 'review_draft', 'score_check'):
                agent_reply = ''
                capability = intent
                try:
                    if intent == 'mock_defense':
                        from services.langchain_service import mock_defense as _mock_defense
                        result = _mock_defense(question_type=params.get('question_type', 'general'))
                        agent_reply = result.get('defense', '')
                    elif intent == 'batch_review':
                        from services.langchain_service import batch_review_assist
                        result = batch_review_assist(projects_info=None)
                        agent_reply = result.get('report', '')
                    elif intent == 'smart_feedback':
                        from services.langchain_service import smart_feedback_generate
                        result = smart_feedback_generate(feedback_type=params.get('feedback_type', 'modify'))
                        agent_reply = result.get('feedback', '')
                    elif intent == 'review_draft':
                        from services.langchain_service import review_draft_generate
                        result = review_draft_generate()
                        agent_reply = result.get('draft', '')
                    elif intent == 'score_check':
                        from services.langchain_service import score_consistency_check
                        result = score_consistency_check(review_data=None)
                        agent_reply = result.get('report', '')
                except Exception as agent_err:
                    agent_reply = f'智能体调用失败：{str(agent_err)[:200]}'

                if not agent_reply:
                    agent_reply = '智能体暂时无法处理，请稍后再试。'
                queue.put({'header': f'type:agent_result\ncapability:{capability}\n'})
                for delta in split_stream_chunks(agent_reply):
                    if delta:
                        queue.put(delta)
                        time.sleep(0.02)
                record = get_chat_record(session_id)
                if record is not None:
                    record['messages'].append({'role': 'user', 'content': message})
                    record['messages'].append({'role': 'assistant', 'content': agent_reply})
                    record['updated_at'] = datetime.utcnow()

            else:
                reply, user_prompt, record = call_llm_chat(message, scene_name, session_id, user_role=role)
                if not reply:
                    reply = '我刚刚没有组织出合适的回答，你可以换个方式再问一次。'
                if record is not None:
                    record['messages'].append({'role': 'user', 'content': user_prompt})
                    record['messages'].append({'role': 'assistant', 'content': reply})
                    trim_chat_history(record)
                    record['updated_at'] = datetime.utcnow()
                queue.put({'header': 'type:chat\n'})
                for delta in split_stream_chunks(reply):
                    if delta:
                        queue.put(delta)
                        time.sleep(0.02)

    except Exception as error:
        queue.put({'error': '调用模型失败', 'detail': error.__class__.__name__ + ': ' + str(error)})
    finally:
        queue.put(None)


def generate_unified_stream(message, role, scene_name, session_id):
    if not session_id:
        session_id = os.urandom(8).hex()

    queue = Queue()
    worker = threading.Thread(
        target=_stream_unified_model,
        args=(queue, message, role, scene_name, session_id),
        daemon=True,
    )
    worker.start()

    @stream_with_context
    def generate():
        yield f"sessionId:{session_id}\n"
        header_sent = False
        while True:
            try:
                item = queue.get(timeout=120)
            except Empty:
                if not worker.is_alive():
                    break
                continue
            if item is None:
                break
            if isinstance(item, dict):
                if item.get('error'):
                    yield f"error:{item.get('detail', '未知错误')}\n"
                    break
                if item.get('header') and not header_sent:
                    yield item['header']
                    header_sent = True
                    continue
            yield f"delta:{str(item)}\n"
        yield "done:1\n"

    response = Response(generate(), mimetype='text/plain; charset=utf-8')
    response.headers['Cache-Control'] = 'no-cache'
    response.headers['X-Accel-Buffering'] = 'no'
    return response


def generate_business_advice(project_info):
    name = project_info.get('name', '')
    description = project_info.get('description', '')
    category = project_info.get('category', '')
    track = project_info.get('track', '')

    question = f"请为以下创新创业项目生成商业计划书优化建议（包含市场分析、商业模式、运营策略、融资建议），使用 Markdown 格式：\n项目名称：{name}\n项目简介：{description}\n项目类别：{category}\n所属赛道：{track}"

    try:
        reply, _, _ = call_llm_chat(question, "商业计划书建议", "")
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
        reply, _, _ = call_llm_chat(question, "风险分析", "")
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
