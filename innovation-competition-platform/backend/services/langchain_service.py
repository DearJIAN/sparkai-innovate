import os
import logging
import traceback

logger = logging.getLogger(__name__)

_llm = None


def get_llm():
    global _llm
    if _llm is not None:
        return _llm
    try:
        from langchain_openai import ChatOpenAI
        _llm = ChatOpenAI(
            model_name=os.getenv('ARK_MODEL', 'doubao-seed-1-6-251015'),
            openai_api_key=os.getenv('ARK_API_KEY'),
            openai_api_base=os.getenv('ARK_BASE_URL', 'https://ark.cn-beijing.volces.com/api/v3'),
            temperature=0.4,
            max_tokens=4096,
            timeout=120,
            request_timeout=120,
        )
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


def material_qa(question, project=None, search_result=None, project_info_text=None):
    context = _build_context_from_search(search_result)
    project_info = project_info_text or _build_project_info_text(project)

    if not context.strip():
        prompt = f"""你是高校创新创业竞赛服务平台的 AI 助手。用户提出了关于项目材料的问题，但目前没有检索到相关材料文档。

项目基本信息：
{project_info}

用户问题：{question}

由于暂无材料文档可参考，请基于项目基本信息尽量回答，并在回答开头说明"当前未检索到项目材料文档，以下基于项目基本信息回答："。

如果项目基本信息也不足以回答，请建议用户先上传项目材料并建立索引。"""
    else:
        prompt = f"""你是高校创新创业竞赛服务平台的 AI 助手，专门帮助用户理解项目材料内容。

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
        prompt = f"""你是高校创新创业竞赛服务平台的 AI 助手，专门帮助检查商业计划书完整性。

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
        prompt = f"""你是高校创新创业竞赛服务平台的 AI 助手，专门帮助检查商业计划书完整性。

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
    }.get(style, '正式专业')

    word_target = 850 if duration == 3 else 1400

    if not context.strip():
        prompt = f"""你是高校创新创业竞赛服务平台的 AI 助手，专门帮助生成路演稿。

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
        prompt = f"""你是高校创新创业竞赛服务平台的 AI 助手，专门帮助生成路演稿。

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
        prompt = f"""你是高校创新创业竞赛服务平台的 AI 评审辅助助手，帮助评委更好地理解项目。

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
        prompt = f"""你是高校创新创业竞赛服务平台的 AI 评审辅助助手，帮助评委更好地理解项目。

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
        prompt = f"""你是高校创新创业竞赛服务平台的 AI 助手，专门帮助学生推荐合适的竞赛。

项目基本信息：
{project_info}

目前系统中没有可报名的竞赛数据。请基于项目信息，给出一般性的竞赛推荐建议，包括：
1. 适合该项目的竞赛类型
2. 建议关注的竞赛方向
3. 准备建议"""
    else:
        prompt = f"""你是高校创新创业竞赛服务平台的 AI 助手，专门帮助学生推荐合适的竞赛。

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
