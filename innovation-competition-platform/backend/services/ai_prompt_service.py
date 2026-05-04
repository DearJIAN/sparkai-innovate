import os
import json
import logging
import traceback

logger = logging.getLogger(__name__)

_llm = None
_agent_executor = None

NAVIGATION_MAP = {
    'portal': {'route': '/portal', 'label': '平台首页', 'keywords': ['首页', '主页', '平台', '回到首页', '返回首页']},
    'competition_square': {'route': '/competitions', 'label': '竞赛广场', 'keywords': ['竞赛广场', '竞赛列表', '浏览竞赛', '看竞赛', '找竞赛', '比赛列表', '有什么比赛', '竞赛大厅']},
    'competition_register': {'route': '/competitions', 'label': '竞赛报名', 'keywords': ['报名', '竞赛报名', '我要报名', '参加比赛', '报名比赛', '我要参赛', '报名竞赛', '互联网+', '挑战杯', '创新创业']},
    'my_registrations': {'route': '/my-registrations', 'label': '我的赛事', 'keywords': ['我的赛事', '我的报名', '报名状态', '审核结果', '报名审核', '报名了什么', '我报了什么', '报名进度']},
    'my_projects': {'route': '/my-projects', 'label': '我的项目', 'keywords': ['我的项目', '项目列表', '查看项目', '我的项目在哪', '我参与的项目', '看看项目']},
    'create_project': {'route': '/create-project', 'label': '创建项目', 'keywords': ['创建项目', '新建项目', '添加项目', '建项目', '我要创建', '发起项目']},
    'guide_projects': {'route': '/guide-projects', 'label': '指导项目', 'keywords': ['指导项目', '我指导的', '指导的项目', '学生项目']},
    'project_review': {'route': '/project-review', 'label': '项目审核', 'keywords': ['项目审核', '审核项目', '审核学生', '审批项目']},
    'pending_reviews': {'route': '/pending-reviews', 'label': '待评审项目', 'keywords': ['待评审', '评审项目', '评审任务', '待评项目', '要评的']},
    'review_history': {'route': '/review-history', 'label': '评审记录', 'keywords': ['评审记录', '评审历史', '已评审', '评过的']},
    'user_management': {'route': '/user-management', 'label': '用户管理', 'keywords': ['用户管理', '管理用户', '用户列表']},
    'project_management': {'route': '/project-management', 'label': '项目管理', 'keywords': ['项目管理', '管理项目', '所有项目']},
    'competition_management': {'route': '/competition-management', 'label': '竞赛管理', 'keywords': ['竞赛管理', '管理竞赛', '比赛管理']},
    'registration_management': {'route': '/registration-management', 'label': '报名管理', 'keywords': ['报名管理', '管理报名', '审核报名']},
    'review_management': {'route': '/review-management', 'label': '评审管理', 'keywords': ['评审管理', '管理评审']},
    'training_camps': {'route': '/training-camps', 'label': '训练营', 'keywords': ['训练营', '培训', '学习营']},
    'courses': {'route': '/courses', 'label': '在线课程', 'keywords': ['课程', '在线课程', '学习', '视频课']},
    'industry_topics': {'route': '/industry-topics', 'label': '产业命题', 'keywords': ['产业命题', '企业命题', '命题', '企业题']},
    'certificates': {'route': '/certificates', 'label': '证书成果', 'keywords': ['证书', '获奖', '成果', '荣誉']},
    'dashboard': {'route': '/dashboard', 'label': '工作台', 'keywords': ['工作台', '仪表盘', '概览', '总览', '首页工作台']},
    'ai_assistant': {'route': '/ai-assistant', 'label': 'AI助手', 'keywords': ['AI助手', '智能助手', '聊天', '对话']},
}


def get_llm():
    global _llm
    if _llm is not None:
        return _llm
    try:
        from langchain_openai import ChatOpenAI
        _llm = ChatOpenAI(
            model_name=os.getenv('GLM_MODEL', 'glm-5'),
            openai_api_key=os.getenv('GLM_API_KEY'),
            openai_api_base=os.getenv('GLM_BASE_URL', 'https://open.bigmodel.cn/api/paas/v4'),
            temperature=0.4,
            max_tokens=4096,
            timeout=120,
            request_timeout=120,
        )
        logger.info('GLM-5 LLM 初始化成功')
        return _llm
    except Exception as e:
        logger.error(f'LLM 初始化失败: {e}')
        return None


def _build_context_from_search(search_result):
    if not search_result or not search_result.get('results'):
        return ''
    parts = []
    for i, item in enumerate(search_result['results'][:6], 1):
        meta = item.get('metadata', {})
        file_name = meta.get('file_name', '未知文件')
        content = item.get('content', '')
        parts.append(f'【来源：{file_name}】\n{content}')
    return '\n\n'.join(parts)


def _build_project_info_text(project):
    if not project:
        return '暂无项目信息'
    parts = []
    if hasattr(project, 'name') and project.name:
        parts.append(f'项目名称：{project.name}')
    if hasattr(project, 'description') and project.description:
        parts.append(f'项目描述：{project.description}')
    if hasattr(project, 'category') and project.category:
        parts.append(f'项目类别：{project.category}')
    if hasattr(project, 'status') and project.status:
        parts.append(f'项目状态：{project.status}')
    if hasattr(project, 'innovation_point') and project.innovation_point:
        parts.append(f'创新点：{project.innovation_point}')
    if hasattr(project, 'target_market') and project.target_market:
        parts.append(f'目标市场：{project.target_market}')
    if hasattr(project, 'team_info') and project.team_info:
        parts.append(f'团队信息：{project.team_info}')
    return '\n'.join(parts) if parts else '暂无项目详细信息'


def _call_llm_with_fallback(prompt_text, fallback_template=''):
    llm = get_llm()
    if llm is None:
        return fallback_template or 'AI 服务暂不可用，请稍后再试。', True
    try:
        from langchain_core.messages import HumanMessage
        response = llm.invoke([HumanMessage(content=prompt_text)])
        return response.content, False
    except Exception as e:
        logger.error(f'LLM 调用失败: {e}')
        traceback.print_exc()
        return fallback_template or f'AI 服务调用失败，请稍后再试。错误信息：{str(e)[:200]}', True


def smart_navigate(user_message, user_role='student'):
    nav_context = '当前平台可用页面：\n'
    for key, info in NAVIGATION_MAP.items():
        nav_context += f'- {info["label"]}（路由：{info["route"]}）\n'

    role_desc = {
        'student': '学生',
        'teacher': '指导老师',
        'judge': '评委',
        'admin': '管理员',
    }.get(user_role, '学生')

    prompt = f"""你是火花智创 SparkAI Innovate的智能引航助手，当前用户角色是{role_desc}。

{nav_context}

用户说："{user_message}"

请判断用户想要做什么，并返回 JSON 格式的结果（不要返回其他内容，只返回 JSON）：
{{
  "intent": "意图描述",
  "route": "对应的路由路径",
  "label": "页面名称",
  "reply": "友好的回复语（20字以内）",
  "action": "navigate"
}}

如果用户的问题不需要跳转页面（比如只是闲聊、问知识性问题），则返回：
{{
  "intent": "通用对话",
  "route": "",
  "label": "",
  "reply": "这个问题我直接为您解答~",
  "action": "chat"
}}

只返回 JSON，不要其他内容。"""

    result, is_fallback = _call_llm_with_fallback(prompt)
    if is_fallback:
        best_match = _keyword_match_navigate(user_message)
        if best_match:
            return {
                'intent': best_match['label'],
                'route': best_match['route'],
                'label': best_match['label'],
                'reply': f'好的，帮你打开{best_match["label"]}~',
                'action': 'navigate',
            }
        return {
            'intent': '通用对话',
            'route': '',
            'label': '',
            'reply': '我暂时无法理解，请换个说法试试~',
            'action': 'chat',
        }

    try:
        cleaned = result.strip()
        if cleaned.startswith('```'):
            cleaned = cleaned.split('\n', 1)[-1]
        if cleaned.endswith('```'):
            cleaned = cleaned.rsplit('```', 1)[0]
        cleaned = cleaned.strip()
        nav_result = json.loads(cleaned)
        if 'action' not in nav_result:
            nav_result['action'] = 'navigate' if nav_result.get('route') else 'chat'
        return nav_result
    except json.JSONDecodeError:
        best_match = _keyword_match_navigate(user_message)
        if best_match:
            return {
                'intent': best_match['label'],
                'route': best_match['route'],
                'label': best_match['label'],
                'reply': f'好的，帮你打开{best_match["label"]}~',
                'action': 'navigate',
            }
        return {
            'intent': '通用对话',
            'route': '',
            'label': '',
            'reply': result[:100],
            'action': 'chat',
        }


def _keyword_match_navigate(user_message):
    msg = user_message.lower()
    best = None
    best_score = 0
    for key, info in NAVIGATION_MAP.items():
        score = 0
        for kw in info['keywords']:
            if kw in msg:
                score = max(score, len(kw))
        if score > best_score:
            best_score = score
            best = info
    return best


def project_idea_generate(competition_name='', competition_category='', track='', skills='', interests=''):
    prompt = f"""你是火花智创 SparkAI Innovate的 AI 创意助手，专门帮助学生生成项目创意。

竞赛信息：
- 竞赛名称：{competition_name or '未指定'}
- 竞赛类别：{competition_category or '未指定'}
- 赛道：{track or '未指定'}

学生信息：
- 技能特长：{skills or '未指定'}
- 兴趣方向：{interests or '未指定'}

请基于以上信息，生成 3-5 个创新项目方向建议。对每个建议，请提供：

## 项目方向 N：[项目名称]

### 核心创意
简要描述项目的核心创意（2-3句话）

### 解决的痛点
描述该项目解决的实际问题

### 技术路线
建议采用的技术方案和工具

### 创新亮点
项目的创新之处（技术创新/模式创新/应用创新）

### 可行性分析
简要分析项目的技术可行性和市场可行性

### 推荐赛道
建议报名的竞赛和赛道

请使用 Markdown 格式输出，内容要具体、可操作、有创新性。"""

    result, is_fallback = _call_llm_with_fallback(
        prompt,
        '当前无法生成项目创意，请稍后再试。'
    )
    return {
        'ideas': result,
        'is_fallback': is_fallback,
    }


def mock_defense(project=None, search_result=None, question_type='general', project_info_text=None):
    context = _build_context_from_search(search_result)
    project_info = project_info_text or _build_project_info_text(project)

    type_desc = {
        'general': '综合提问（涵盖创新性、可行性、市场、团队等方面）',
        'technical': '技术深度提问（侧重技术方案、架构、实现细节）',
        'business': '商业提问（侧重商业模式、盈利、市场、竞争）',
        'tough': '压力提问（质疑项目可行性、创新性、风险）',
    }.get(question_type, '综合提问')

    if not context.strip():
        prompt = f"""你是高校创新创业竞赛的模拟评委，正在对学生项目进行路演答辩提问。

项目基本信息：
{project_info}

提问风格：{type_desc}

请扮演 3 位不同风格的评委，各提出 1-2 个问题，并给出每个问题的参考回答要点。

## 评委 A（温和型）
### 提问
### 参考回答要点

## 评委 B（专业型）
### 提问
### 参考回答要点

## 评委 C（犀利型）
### 提问
### 参考回答要点

## 答辩建议
给出 3-5 条答辩技巧建议

请使用 Markdown 格式输出。"""
    else:
        prompt = f"""你是高校创新创业竞赛的模拟评委，正在对学生项目进行路演答辩提问。

以下是项目材料片段：
{context}

项目基本信息：
{project_info}

提问风格：{type_desc}

请基于项目材料，扮演 3 位不同风格的评委，各提出 1-2 个有针对性的问题，并给出参考回答要点。

## 评委 A（温和型）
### 提问
### 参考回答要点

## 评委 B（专业型）
### 提问
### 参考回答要点

## 评委 C（犀利型）
### 提问
### 参考回答要点

## 答辩建议
给出 3-5 条答辩技巧建议

请使用 Markdown 格式输出，问题要基于项目材料内容，有针对性。"""

    result, is_fallback = _call_llm_with_fallback(
        prompt,
        '当前无法进行模拟答辩，请稍后再试。'
    )
    return {
        'defense': result,
        'question_type': question_type,
        'is_fallback': is_fallback,
    }


def batch_review_assist(projects_info=None):
    if not projects_info:
        return {
            'report': '暂无待审核项目数据',
            'is_fallback': True,
        }

    projects_text = ''
    for i, p in enumerate(projects_info[:10], 1):
        projects_text += f'\n### 项目 {i}：{p.get("name", "未知")}\n'
        projects_text += f'- 描述：{p.get("description", "无")}\n'
        projects_text += f'- 类别：{p.get("category", "无")}\n'
        projects_text += f'- 状态：{p.get("status", "无")}\n'
        projects_text += f'- 负责人：{p.get("leader", "未知")}\n'
        if p.get('teacher_feedback'):
            projects_text += f'- 之前反馈：{p["teacher_feedback"]}\n'

    prompt = f"""你是火花智创 SparkAI Innovate的 AI 审核助手，帮助指导老师快速了解待审核项目的情况。

以下是待审核项目列表：
{projects_text}

请为每个项目提供审核建议，输出以下内容：

## 审核概览
简要总结所有项目的整体情况

## 逐项审核建议
对每个项目给出：

### 项目：[名称]
- **建议操作**：通过 / 建议修改 / 驳回
- **审核要点**：需要关注的关键问题
- **修改建议**：如果建议修改，具体修改什么
- **风险提示**：项目可能存在的风险

## 优先级排序
建议老师优先审核哪些项目（按紧急程度排序）

⚠️ 注意：以上仅为 AI 辅助建议，最终审核决定由老师做出。

请使用 Markdown 格式输出。"""

    result, is_fallback = _call_llm_with_fallback(
        prompt,
        '当前无法进行批量审核分析，请稍后再试。'
    )
    return {
        'report': result,
        'is_fallback': is_fallback,
    }


def smart_feedback_generate(project=None, search_result=None, feedback_type='modify', project_info_text=None):
    context = _build_context_from_search(search_result)
    project_info = project_info_text or _build_project_info_text(project)

    type_desc = {
        'modify': '建议修改（项目需要改进后重新提交）',
        'approve': '建议通过（项目符合要求）',
        'reject': '建议驳回（项目存在严重问题）',
    }.get(feedback_type, '建议修改')

    prompt = f"""你是火花智创 SparkAI Innovate的 AI 助手，帮助指导老师生成项目审核反馈意见。

项目基本信息：
{project_info}

{'以下是项目材料片段：\n' + context if context.strip() else '暂无项目材料文档。'}

反馈类型：{type_desc}

请生成一份专业的审核反馈意见，包含以下内容：

## 总体评价
简要概括项目的整体情况（2-3句话）

## 优点
列出项目的优点和亮点

## 存在问题
列出项目存在的问题和不足

## 修改建议
给出具体的修改建议（如果是建议修改类型）

## 下一步建议
建议学生接下来应该做什么

请使用 Markdown 格式输出，语气专业但友善，建议要具体可操作。"""

    result, is_fallback = _call_llm_with_fallback(
        prompt,
        '当前无法生成反馈意见，请稍后再试。'
    )
    return {
        'feedback': result,
        'feedback_type': feedback_type,
        'is_fallback': is_fallback,
    }


def review_draft_generate(project=None, search_result=None, scoring_dimensions=None, project_info_text=None):
    context = _build_context_from_search(search_result)
    project_info = project_info_text or _build_project_info_text(project)

    dimensions = scoring_dimensions or [
        {'name': '创新性', 'weight': 25},
        {'name': '可行性', 'weight': 20},
        {'name': '市场前景', 'weight': 20},
        {'name': '团队', 'weight': 15},
        {'name': '商业模式', 'weight': 20},
    ]

    dims_text = '\n'.join([f'- {d["name"]}（权重{d["weight"]}%）' for d in dimensions])

    prompt = f"""你是火花智创 SparkAI Innovate的 AI 评审助手，帮助评委快速生成评审意见草稿。

项目基本信息：
{project_info}

{'以下是项目材料片段：\n' + context if context.strip() else '暂无项目材料文档。'}

评分维度：
{dims_text}

请基于以上信息，生成评审意见草稿：

## 项目概述
简要概括项目核心内容（3-5句话）

## 各维度评审意见
对每个评分维度给出定性评价：

{chr(10).join([f"### " + d["name"] + chr(10) + "- 评价：[定性描述]" + chr(10) + "- 亮点：[具体亮点]" + chr(10) + "- 不足：[具体不足]" for d in dimensions])}

## 综合评审意见
整体评价和建议（100-200字）

## 建议追问问题
列出 3-5 个建议在答辩时追问的问题

⚠️ 重要声明：
1. 以上仅为 AI 生成的评审意见草稿，供评委参考
2. 评委应根据自身专业判断做出最终评审决定
3. AI 不提供具体评分，评分由评委人工决定

请使用 Markdown 格式输出。"""

    result, is_fallback = _call_llm_with_fallback(
        prompt,
        '当前无法生成评审意见草稿，请稍后再试。'
    )
    return {
        'draft': result,
        'dimensions': [d['name'] for d in dimensions],
        'is_fallback': is_fallback,
    }


def score_consistency_check(review_data=None):
    if not review_data:
        return {
            'report': '暂无评审数据可供分析',
            'is_fallback': True,
        }

    scores_text = ''
    for key, value in review_data.items():
        if key not in ('comment', 'judge_name', 'project_name'):
            scores_text += f'- {key}：{value}\n'

    comment = review_data.get('comment', '无')

    prompt = f"""你是火花智创 SparkAI Innovate的 AI 评审质量检查助手，帮助评委检查评分与文字评价的一致性。

评委评分：
{scores_text}

评委文字评价：
{comment}

请检查评分与文字评价之间是否存在不一致，输出以下内容：

## 一致性检查结果
- ✅ 一致 / ⚠️ 存在不一致

## 详细分析
逐个维度检查评分是否与文字评价一致：

### 各维度分析
对每个评分维度：
- 评分：X 分
- 文字评价中的描述：[引用]
- 是否一致：✅/⚠️
- 说明：[如果不一致，说明矛盾之处]

## 改进建议
如果不一致，给出修改建议（是调整评分还是补充评价）

⚠️ 注意：此检查仅为辅助工具，评委的评分决定权在评委本人。

请使用 Markdown 格式输出。"""

    result, is_fallback = _call_llm_with_fallback(
        prompt,
        '当前无法进行评分一致性检查，请稍后再试。'
    )
    return {
        'report': result,
        'is_fallback': is_fallback,
    }


def material_qa(question, project=None, search_result=None, project_info_text=None):
    context = _build_context_from_search(search_result)
    project_info = project_info_text or _build_project_info_text(project)

    if not context.strip():
        prompt = f"""你是火花智创 SparkAI Innovate的 AI 助手。用户提出了关于项目材料的问题，但目前没有检索到相关材料文档。

项目基本信息：
{project_info}

用户问题：{question}

由于暂无材料文档可参考，请基于项目基本信息尽量回答，并在回答开头说明"当前未检索到项目材料文档，以下基于项目基本信息回答："。

如果项目基本信息也不足以回答，请建议用户先上传项目材料并建立索引。"""
    else:
        prompt = f"""你是火花智创 SparkAI Innovate的 AI 助手，专门帮助用户理解项目材料内容。

以下是检索到的相关项目材料片段：
{context}

项目基本信息：
{project_info}

用户问题：{question}

请基于以上材料和信息回答用户问题。要求：
1. 回答要准确、具体，尽量引用材料中的内容
2. 如果材料不足以回答问题，请明确说明并建议补充哪些材料
3. 如果涉及创新点、商业模式、市场风险等，请给出专业分析
4. 回答使用中文"""

    result, is_fallback = _call_llm_with_fallback(
        prompt,
        f'当前无法进行 AI 材料问答。请确保：\n1. 已上传项目材料\n2. 已建立材料索引\n3. AI 服务正常运行\n\n您的问题：{question}'
    )

    sources = []
    if search_result and search_result.get('results'):
        seen = set()
        for item in search_result['results']:
            meta = item.get('metadata', {})
            fn = meta.get('file_name', '')
            if fn and fn not in seen:
                seen.add(fn)
                sources.append({'file_name': fn, 'relevance': round(item.get('score', 0), 4)})

    return {
        'answer': result,
        'sources': sources,
        'is_fallback': is_fallback,
    }


def bp_check(project=None, search_result=None, project_info_text=None):
    context = _build_context_from_search(search_result)
    project_info = project_info_text or _build_project_info_text(project)

    if not context.strip():
        prompt = f"""你是火花智创 SparkAI Innovate的 AI 助手，专门帮助检查商业计划书完整性。

项目基本信息：
{project_info}

目前未检索到项目材料文档，请仅基于项目基本信息进行简版分析，并在开头说明"当前未检索到项目材料，以下基于项目基本信息进行简版分析："。

请从以下维度分析：
1. 亮点：项目有哪些值得肯定的地方
2. 不足：项目信息中可能存在的不足
3. 缺失模块：建议补充哪些材料或信息
4. 优化建议：如何改进
5. 风险提示：可能面临的风险"""
    else:
        prompt = f"""你是火花智创 SparkAI Innovate的 AI 助手，专门帮助检查商业计划书完整性。

以下是检索到的项目材料片段：
{context}

项目基本信息：
{project_info}

请基于以上材料和信息，对商业计划书进行全面体检，输出以下内容：

## 亮点
列出商业计划书中的亮点和优势

## 不足
列出商业计划书中存在的不足和问题

## 缺失模块
列出商业计划书中缺失的重要模块（如：团队介绍、竞品分析、财务预测、风险评估、商业模式画布等）

## 优化建议
给出具体的优化建议

## 风险提示
提示可能面临的风险

请使用 Markdown 格式输出，内容要具体、可操作。"""

    result, is_fallback = _call_llm_with_fallback(
        prompt,
        '当前无法进行商业计划书体检。请确保已上传材料并建立索引。'
    )

    return {
        'report': result,
        'is_fallback': is_fallback,
    }


def roadshow_generate(project=None, search_result=None, duration=3, style='formal', project_info_text=None):
    context = _build_context_from_search(search_result)
    project_info = project_info_text or _build_project_info_text(project)

    style_desc = {
        'formal': '正式专业',
        'passionate': '激情澎湃',
        'concise': '简洁精炼',
        'story': '故事叙述',
    }.get(style, '正式专业')

    word_target = 850 if duration == 3 else (1400 if duration == 5 else 2200)

    if not context.strip():
        prompt = f"""你是火花智创 SparkAI Innovate的 AI 助手，专门帮助生成路演稿。

项目基本信息：
{project_info}

目前未检索到项目材料文档，请仅基于项目基本信息生成简版路演稿，并在开头说明"当前未检索到项目材料，以下基于项目基本信息生成简版路演稿："。

路演时长：{duration}分钟（约{word_target}字）
风格：{style_desc}

请按以下结构生成路演稿：
## 开场
## 痛点
## 方案
## 创新点
## 商业模式
## 团队
## 结尾"""
    else:
        prompt = f"""你是火花智创 SparkAI Innovate的 AI 助手，专门帮助生成路演稿。

以下是检索到的项目材料片段：
{context}

项目基本信息：
{project_info}

路演时长：{duration}分钟（约{word_target}字）
风格：{style_desc}

请基于以上材料和信息，生成一份结构完整、内容充实的路演稿。按以下结构组织：

## 开场
用引人入胜的方式开场，点明项目要解决的问题

## 痛点
描述目标用户面临的痛点和需求

## 方案
介绍项目的解决方案和核心功能

## 创新点
突出项目的创新之处和技术/模式差异化

## 商业模式
说明盈利模式、目标市场和竞争优势

## 团队
介绍团队核心成员和优势

## 结尾
用有力的结尾呼吁支持或投资

请使用 Markdown 格式输出，语言{style_desc}，字数控制在{word_target}字左右。"""

    result, is_fallback = _call_llm_with_fallback(
        prompt,
        f'当前无法生成路演稿。请确保已上传材料并建立索引。\n\n项目：{project_info[:200]}'
    )

    word_count = len(result) if result else 0

    return {
        'script': result,
        'word_count': word_count,
        'estimated_minutes': duration,
        'is_fallback': is_fallback,
    }


def review_assist(project=None, search_result=None, project_info_text=None):
    context = _build_context_from_search(search_result)
    project_info = project_info_text or _build_project_info_text(project)

    if not context.strip():
        prompt = f"""你是火花智创 SparkAI Innovate的 AI 评审辅助助手，帮助评委更好地理解项目。

项目基本信息：
{project_info}

目前未检索到项目材料文档，请仅基于项目基本信息进行简版分析，并在开头说明"当前未检索到项目材料，以下基于项目基本信息进行简版分析："。

请从以下维度提供评审参考：
1. 项目摘要
2. 创新亮点
3. 可行性风险
4. 市场风险
5. 团队风险
6. 商业模式风险
7. 建议追问问题
8. 各评分维度参考

注意：你不应给出任何具体分数或评分建议，只提供定性分析。"""
    else:
        prompt = f"""你是火花智创 SparkAI Innovate的 AI 评审辅助助手，帮助评委更好地理解项目。

以下是检索到的项目材料片段：
{context}

项目基本信息：
{project_info}

请基于以上材料和信息，为评委提供评审参考。输出以下内容：

## 项目摘要
简要概括项目的核心内容

## 创新亮点
列出项目的创新之处和亮点

## 可行性风险
分析项目在技术、资源、时间等方面的可行性风险

## 市场风险
分析项目面临的市场风险和竞争风险

## 团队风险
分析团队构成和能力方面可能存在的风险

## 商业模式风险
分析商业模式方面可能存在的风险

## 建议追问问题
列出评委可以进一步追问的问题（3-5个）

## 各评分维度参考
为每个评分维度（创新性、可行性、市场前景、团队、商业模式）提供定性参考意见

⚠️ 重要：你不应给出任何具体分数或评分建议，只提供定性分析和参考意见。最终评分由评委人工决定。

请使用 Markdown 格式输出。"""

    result, is_fallback = _call_llm_with_fallback(
        prompt,
        '当前无法进行评审辅助分析。请确保已上传材料并建立索引。'
    )

    return {
        'analysis': result,
        'disclaimer': 'AI 结果仅供评审参考，最终评分由评委人工决定。',
        'is_fallback': is_fallback,
    }


def competition_recommend(project=None, competitions=None, project_info_text=None):
    project_info = project_info_text or _build_project_info_text(project)

    competitions_text = ''
    if competitions:
        comp_parts = []
        for comp in competitions:
            parts = [f'竞赛名称：{comp.get("name", "未知")}']
            if comp.get('description'):
                parts.append(f'描述：{comp["description"]}')
            if comp.get('category'):
                parts.append(f'类别：{comp["category"]}')
            if comp.get('tracks'):
                if isinstance(comp['tracks'], list):
                    track_names = [t.get('name', '') if isinstance(t, dict) else str(t) for t in comp['tracks']]
                    parts.append(f'赛道：{", ".join(track_names)}')
                else:
                    parts.append(f'赛道：{comp["tracks"]}')
            if comp.get('status'):
                parts.append(f'状态：{comp["status"]}')
            if comp.get('registration_start') or comp.get('registration_end'):
                parts.append(f'报名时间：{comp.get("registration_start", "?")} ~ {comp.get("registration_end", "?")}')
            comp_parts.append('\n'.join(parts))
        competitions_text = '\n\n---\n\n'.join(comp_parts)

    if not competitions_text.strip():
        prompt = f"""你是火花智创 SparkAI Innovate的 AI 助手，专门帮助学生推荐合适的竞赛。

项目基本信息：
{project_info}

目前系统中没有可报名的竞赛数据。请基于项目信息，给出一般性的竞赛推荐建议，包括：
1. 适合该项目的竞赛类型
2. 建议关注的竞赛方向
3. 准备建议"""
    else:
        prompt = f"""你是火花智创 SparkAI Innovate的 AI 助手，专门帮助学生推荐合适的竞赛。

项目基本信息：
{project_info}

当前可报名的竞赛列表：
{competitions_text}

请基于项目信息和竞赛数据，推荐最适合该项目的竞赛和赛道。对每个推荐，请提供：
1. 推荐的竞赛名称和赛道
2. 匹配理由（为什么这个竞赛适合该项目）
3. 建议准备的材料
4. 注意事项

请按匹配度从高到低排列，使用 Markdown 格式输出。"""

    result, is_fallback = _call_llm_with_fallback(
        prompt,
        '当前无法进行竞赛推荐。请确保系统中有可报名的竞赛数据。'
    )

    return {
        'recommendation': result,
        'is_fallback': is_fallback,
    }
