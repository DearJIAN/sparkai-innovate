import random
import json


def normal_score(mean=84, std=6, min_score=70, max_score=98):
    score = random.gauss(mean, std)
    return max(min_score, min(max_score, round(score)))


PPT_DIMENSIONS = [
    {"key": "structure", "name": "结构完整性", "max_score": 12, "desc": "是否包含项目背景、痛点、方案、市场、团队、计划等必要页面"},
    {"key": "visual", "name": "视觉版式与阅读体验", "max_score": 14, "desc": "页面是否整洁、层级是否清晰、图文比例是否合理"},
    {"key": "pain_point", "name": "痛点表达清晰度", "max_score": 12, "desc": "是否讲清楚目标用户、真实问题和需求场景"},
    {"key": "solution", "name": "解决方案呈现", "max_score": 14, "desc": "是否清楚展示产品、技术、服务或商业模式"},
    {"key": "innovation", "name": "创新亮点表达", "max_score": 14, "desc": "是否突出技术创新、模式创新或应用场景创新"},
    {"key": "business", "name": "商业与市场逻辑", "max_score": 12, "desc": "是否说明市场空间、用户价值、落地路径和增长逻辑"},
    {"key": "team", "name": "团队与执行计划", "max_score": 10, "desc": "是否展示团队分工、能力匹配和推进计划"},
    {"key": "persuasion", "name": "路演说服力", "max_score": 12, "desc": "是否适合现场表达，是否具备打动评委的叙事节奏"}
]

REPORT_DIMENSIONS = [
    {"key": "summary", "name": "项目摘要与定位", "max_score": 10, "desc": "是否准确说明项目要解决什么问题、面向谁、价值是什么"},
    {"key": "market", "name": "市场痛点与需求论证", "max_score": 12, "desc": "是否有调研、数据、用户场景、行业背景支撑"},
    {"key": "innovation", "name": "创新价值与技术路线", "max_score": 14, "desc": "是否体现技术、产品、模式或服务创新"},
    {"key": "business_model", "name": "商业模式与可持续性", "max_score": 14, "desc": "是否说明收入来源、成本结构、客户获取和增长逻辑"},
    {"key": "implementation", "name": "实施路径与里程碑", "max_score": 12, "desc": "是否有清晰阶段目标、任务拆解和落地计划"},
    {"key": "team_resource", "name": "团队能力与资源匹配", "max_score": 10, "desc": "团队背景、分工、资源是否支撑项目推进"},
    {"key": "risk_finance", "name": "财务、风险与应对", "max_score": 14, "desc": "是否说明资金、成本、风险、竞争与解决策略"},
    {"key": "completeness", "name": "材料规范与论证完整性", "max_score": 14, "desc": "结构、格式、表达、图表、引用和逻辑是否完整"}
]

PPT_KEYWORDS = [
    "痛点", "用户", "市场", "规模", "竞品", "商业模式", "盈利", "技术路线", "创新点",
    "团队", "落地", "试点", "融资", "计划", "里程碑", "风险", "优势", "专利", "数据", "案例"
]

REPORT_KEYWORDS = [
    "项目背景", "行业痛点", "用户需求", "市场规模", "竞品分析", "商业模式", "收入来源",
    "成本结构", "技术路线", "创新点", "实施计划", "里程碑", "团队分工", "风险分析",
    "财务预测", "社会价值", "推广策略", "调研数据", "专利", "成果转化"
]


def _generate_dimension_scores(total_score, dimensions, keyword_hits):
    scores = []
    remaining = total_score
    total_max = sum(d["max_score"] for d in dimensions)

    for i, dim in enumerate(dimensions):
        ratio = random.uniform(0.72, 0.98)
        if keyword_hits > 3:
            ratio = min(0.99, ratio + random.uniform(0.02, 0.06))
        raw = round(dim["max_score"] * ratio)
        raw = max(round(dim["max_score"] * 0.55), min(dim["max_score"], raw))

        if i == len(dimensions) - 1:
            dim_score = max(round(dim["max_score"] * 0.55), min(dim["max_score"], remaining))
        else:
            dim_score = raw

        remaining -= dim_score
        comment = _get_dimension_comment(dim["key"], dim_score, dim["max_score"])
        scores.append({
            "key": dim["key"],
            "name": dim["name"],
            "score": dim_score,
            "max_score": dim["max_score"],
            "desc": dim["desc"],
            "comment": comment
        })

    actual_total = sum(s["score"] for s in scores)
    if actual_total != total_score:
        diff = total_score - actual_total
        sorted_by_gap = sorted(scores, key=lambda s: s["max_score"] - s["score"], reverse=True)
        for s in sorted_by_gap:
            if diff == 0:
                break
            if diff > 0 and s["score"] < s["max_score"]:
                s["score"] += 1
                diff -= 1
            elif diff < 0 and s["score"] > round(s["max_score"] * 0.55):
                s["score"] -= 1
                diff += 1

    return scores


def _get_dimension_comment(dim_key, score, max_score):
    ratio = score / max_score
    comments_map = {
        "structure": [
            ("页面结构完整，涵盖项目论证所需的关键板块，信息层次分明", 0.85),
            ("整体结构较为合理，基本覆盖了项目展示的主要方面", 0.75),
            ("页面组织尚可，部分关键板块覆盖不够充分", 0.6)
        ],
        "visual": [
            ("视觉版式整洁规范，图文搭配合理，阅读体验流畅", 0.85),
            ("整体版式较为清晰，信息层级基本合理", 0.75),
            ("页面设计可以进一步优化，部分区域信息密度偏高", 0.6)
        ],
        "pain_point": [
            ("痛点表达清晰，用户场景与需求描述较为具体", 0.85),
            ("痛点识别基本到位，能够说明目标用户与核心问题", 0.75),
            ("痛点描述偏向概括性表述，可增加更具体的场景支撑", 0.6)
        ],
        "solution": [
            ("解决方案描述完整，产品/服务逻辑清晰，价值主张明确", 0.85),
            ("方案呈现较为清楚，能够让人理解产品核心功能", 0.75),
            ("方案框架已有，但在细节和差异化方面可以进一步充实", 0.6)
        ],
        "innovation": [
            ("创新点呈现突出，技术或模式创新表述具有较强的辨识度", 0.85),
            ("创新方向基本明确，具备一定的差异化特征", 0.75),
            ("创新亮点可以进一步凝练，与同类方案的差异需要更清晰表达", 0.6)
        ],
        "business": [
            ("商业逻辑清晰，市场空间与增长路径有较为合理的阐述", 0.85),
            ("商业模式基本成型，能够看出项目的商业潜力", 0.75),
            ("商业逻辑有待细化，盈利模式和增长路径可以进一步明确", 0.6)
        ],
        "team": [
            ("团队配置合理，成员能力与项目需求匹配度高，执行计划可操作性强", 0.85),
            ("团队背景基本能够支撑项目推进，分工较为清晰", 0.75),
            ("团队信息可以进一步丰富，突出成员与项目关键任务的关联", 0.6)
        ],
        "persuasion": [
            ("叙事节奏把握得当，关键信息传递高效，具备较强的路演感染力", 0.85),
            ("整体表达较为流畅，主要观点能够被评委快速理解", 0.75),
            ("表达节奏可以优化，重点内容需要更突出以增强说服效果", 0.6)
        ],
        "summary": [
            ("项目定位明确，核心价值主张清晰，能够快速建立认知", 0.85),
            ("项目摘要较为完整，基本说明要解决的问题和预期价值", 0.75),
            ("项目定位可以更加聚焦，建议用更精炼的语言概括核心亮点", 0.6)
        ],
        "market": [
            ("市场分析较为扎实，行业背景和用户需求有具体数据或案例支撑", 0.85),
            ("市场论证基本到位，能够说明目标市场的规模和机会", 0.75),
            ("市场分析偏向定性描述，建议补充量化数据或调研依据", 0.6)
        ],
        "business_model": [
            ("商业模式设计合理，收入来源、成本结构和增长逻辑较为完整", 0.85),
            ("商业闭环基本成型，主要盈利模式可以识别", 0.75),
            ("商业模式的可持续性论证可以进一步加强", 0.6)
        ],
        "implementation": [
            ("实施路径清晰，阶段目标和里程碑设置合理，可执行性强", 0.85),
            ("推进计划基本完整，能够看出项目落地的主要步骤", 0.75),
            ("实施计划可以更加细化，关键里程碑需要补充时间节点", 0.6)
        ],
        "team_resource": [
            ("团队能力与资源配置合理，能够有效支撑项目推进", 0.85),
            ("团队构成基本满足项目需求，核心角色有所覆盖", 0.75),
            ("团队信息可以进一步丰富，明确各成员的具体职责和贡献", 0.6)
        ],
        "risk_finance": [
            ("风险分析较为全面，财务预测合理，应对策略具有可操作性", 0.85),
            ("主要风险有所识别，财务框架基本清晰", 0.75),
            ("风险应对和财务分析可以更加具体，补充量化预估和预案", 0.6)
        ],
        "completeness": [
            ("材料规范完整，结构严谨，论证逻辑清晰，引用规范", 0.85),
            ("材料整体较为完整，关键章节和论证要素基本齐备", 0.75),
            ("部分章节内容可以进一步充实，提升论证的严谨性", 0.6)
        ]
    }

    entries = comments_map.get(dim_key, [("表现良好", 1)])
    for comment, threshold in entries:
        if ratio >= threshold:
            return comment
    return entries[-1][0]


PPT_SUMMARIES_HIGH = [
    "该PPT材料在结构完整性、视觉表达和创新亮点呈现方面表现突出，逻辑主线清晰，能够有效传递项目核心价值。叙事节奏把握得当，答辩说服力较强，已经具备良好的路演展示基础。建议进一步丰富市场数据和落地案例，以增强论证深度。",
    "该材料在多个评估维度上表现优异，页面组织合理，重点突出，能够快速建立项目认知。创新点表达具有较强的辨识度，商业逻辑较为清晰。已经达到参赛展示的良好水平，后续可以在细节和数据层面做进一步打磨。"
]

PPT_SUMMARIES_MID = [
    "该PPT材料整体结构较为完整，能够较清楚地呈现项目定位、核心方案与推进思路。视觉版式基本规范，主要信息传递较为有效。当前材料已经具备参赛展示基础，但在市场数据支撑、创新亮点凝练和答辩说服力方面仍有进一步提升空间。",
    "该材料在项目表达和逻辑组织方面表现良好，大部分关键信息能够被评委理解。建议重点优化痛点表达的真实性和具体性，补充更有说服力的市场数据和团队执行案例，进一步提升材料的整体竞争力。"
]

PPT_SUMMARIES_LOW = [
    "该PPT材料在项目愿景和团队执行意愿方面表现积极，但部分论证仍停留在概念描述层面。建议围绕目标用户、落地路径和商业闭环补充更具体的证据，优化页面信息层级，让评委能够更快抓住重点。",
    "材料已基本覆盖项目展示所需的主要板块，但在深度和细节方面需要加强。重点建议：用真实数据替代概括性描述，优化页面版式以降低信息密度，强化创新亮点与技术壁垒的表达。"
]

REPORT_SUMMARIES_HIGH = [
    "该报告在项目论证、市场分析和商业设计方面表现优异，结构严谨、逻辑清晰，关键维度均有较为充实的分析支撑。技术路线和创新价值表述突出，实施路径和风险应对具有较好的可操作性。整体已达到较高完成度，具备较强的评审竞争力。",
    "本项目报告在多个维度上展现了扎实的论证基础和清晰的商业思维，市场痛点识别准确，商业模式设计合理。报告整体完成度高，建议后续持续跟踪市场变化，动态更新数据和实施计划。"
]

REPORT_SUMMARIES_MID = [
    "该报告整体结构较为完整，能够较系统地阐述项目的背景、方案和市场逻辑。在项目定位、技术路线和团队配置方面表现良好，但在市场数据论证、财务预测和风险评估方面仍有提升空间。建议补充更多量化数据和行业对标分析，增强报告的说服力。",
    "报告在项目表达和商业逻辑方面表现良好，核心内容基本覆盖了评审关注的重点维度。当前版本已达到申报基础水平，建议重点强化市场调研的量化支撑和商业模式的可持续性论证。"
]

REPORT_SUMMARIES_LOW = [
    "该报告在项目方向识别和基本描述方面有一定基础，但论证深度和材料规范性需要进一步加强。建议重点补充市场调研数据、细化实施路径、完善风险分析，并优化报告的整体结构和表达方式，使其更加严谨和专业。",
    "报告已覆盖项目申报所需的主要板块，但大部分内容仍以概括性描述为主。建议围绕用户需求、市场验证、财务规划和风险预案四个方向进行深度补充，用数据和案例替代概念性表述，提升报告的整体质量。"
]

PPT_ADVANTAGES = [
    "项目定位较明确，能够围绕目标场景展开材料表达",
    "PPT结构具备基本完整性，评审能够较快理解项目主线",
    "技术创新方向清晰，差异化特征有所体现",
    "页面版式整洁，图文搭配较为合理，阅读体验良好",
    "路演叙事节奏较好，关键信息能够在有限页面内有效传递",
    "团队能力与项目方向具有一定匹配度",
    "解决方案描述具体，产品逻辑较为清楚",
    "市场机会识别准确，目标用户画像较为清晰",
    "创新亮点已有不错呈现，具备进一步深化的基础",
    "执行计划可操作性强，阶段目标设定合理"
]

REPORT_ADVANTAGES = [
    "项目定位清晰，核心价值主张具有较好的市场针对性",
    "报告结构完整，章节设置合理，论证逻辑较为清晰",
    "市场分析维度覆盖较全，行业背景和用户需求有一定阐述",
    "商业模式设计具有可行性，收入来源和增长逻辑基本明确",
    "技术路线描述较为详细，创新点有一定辨识度",
    "团队构成合理，核心成员背景与项目方向匹配",
    "实施路径阶段划分清楚，里程碑设置有较好的操作性",
    "风险评估覆盖了主要维度，具有一定的预案意识",
    "报告格式规范，引用来源标注清楚，整体专业性较强",
    "项目社会价值有所体现，与政策方向和行业趋势较为契合"
]

PPT_PROBLEMS = [
    "市场调研证据略显不足，缺少对目标用户真实需求的量化支撑",
    "商业模式的收入来源和成本结构描述仍偏概念化",
    "风险应对方案不够具体，建议补充技术、市场和运营层面的预案",
    "部分页面信息密度偏高，重点内容不够突出",
    "创新点与竞品的差异化对比不够直观",
    "缺少具体落地案例或试点数据来支撑可行性",
    "痛点描述偏向通用痛点，缺少针对细分场景的深度分析",
    "财务预期未提供合理测算依据"
]

REPORT_PROBLEMS = [
    "市场规模论证较为笼统，缺少细分市场数据和行业对标分析",
    "商业模式闭环不够清晰，客户获取成本和用户生命周期价值未充分说明",
    "实施路径中关键里程碑缺少具体的时间节点和可量化目标",
    "风险分析偏定性描述，未对风险等级和发生概率进行区分",
    "财务预测数据缺少测算逻辑和关键假设说明",
    "竞品分析维度较单一，未充分展示与主要竞品的差异化优势",
    "技术方案的可行性和壁垒论证不够充分",
    "团队分工与项目关键任务的对应关系不够明确"
]

PPT_SUGGESTIONS = [
    "建议补充真实用户访谈、竞品对比或试点反馈数据，用事实增强痛点可信度",
    "建议将创新点拆分为技术创新、模式创新、应用场景创新三个层面分别表达",
    "建议优化页面信息层级，每页聚焦一个核心观点，降低阅读负担",
    "建议增加阶段性成果展示，用数据图表替代纯文字描述",
    "建议为商业模式补充简要的盈利测算或增长模型",
    "建议增加答辩预设问题的应对策略，提升路演准备充分度"
]

REPORT_SUGGESTIONS = [
    "建议补充目标市场的规模数据、增长趋势和细分市场占比分析",
    "建议完善商业模式章节，明确收入来源、成本结构和盈利预测",
    "建议增加阶段性里程碑的时间规划，用甘特图或时间轴展示推进节奏",
    "建议对主要竞争对手进行多维度对比分析，突出差异化优势",
    "建议补充财务预测的关键假设和测算逻辑，增强数据可信度",
    "建议将技术方案与用户价值直接关联，说明技术如何转化为商业优势"
]

PPT_NEXT_ACTIONS = [
    "优先优化痛点表达页面，补充用户调研数据和真实场景案例",
    "精简信息密度较高的页面，确保每页不超过一个核心观点",
    "完善商业模式板块，补充简要的盈利模型或增长逻辑",
    "增加答辩Q&A预设页面，提前准备评审可能关注的问题",
    "优化封面和目录页设计，给评委留下专业的第一印象"
]

REPORT_NEXT_ACTIONS = [
    "优先补充市场调研章节，加入量化数据和行业报告引用",
    "完善财务预测部分，补充关键假设和测算方法说明",
    "细化实施计划，为每个阶段设定可量化的目标和时间节点",
    "补充竞品分析深度，从技术、市场、团队等多个维度进行对比",
    "优化报告整体排版和图表呈现，提升专业度和可读性"
]

PPT_LEVELS = {"优秀": (90, 98), "良好": (80, 89), "待提升": (70, 79)}
REPORT_LEVELS = {"优秀": (90, 98), "良好": (80, 89), "待提升": (70, 79)}


def pick(arr, count):
    return random.sample(arr, min(count, len(arr)))


def get_level(score):
    if score >= 90:
        return "优秀"
    elif score >= 80:
        return "良好"
    return "待提升"


def generate_evaluation(evaluation_type, keyword_hits=0):
    if evaluation_type == "ppt":
        dimensions = PPT_DIMENSIONS
        sum_high = PPT_SUMMARIES_HIGH
        sum_mid = PPT_SUMMARIES_MID
        sum_low = PPT_SUMMARIES_LOW
        advantages = PPT_ADVANTAGES
        problems = PPT_PROBLEMS
        suggestions = PPT_SUGGESTIONS
        next_actions = PPT_NEXT_ACTIONS
    else:
        dimensions = REPORT_DIMENSIONS
        sum_high = REPORT_SUMMARIES_HIGH
        sum_mid = REPORT_SUMMARIES_MID
        sum_low = REPORT_SUMMARIES_LOW
        advantages = REPORT_ADVANTAGES
        problems = REPORT_PROBLEMS
        suggestions = REPORT_SUGGESTIONS
        next_actions = REPORT_NEXT_ACTIONS

    bonus = min(4, keyword_hits // 3) if keyword_hits > 0 else 0
    total_score = normal_score(mean=84 + random.uniform(-1, 1))
    total_score = min(98, total_score + bonus)

    dimension_scores = _generate_dimension_scores(total_score, dimensions, keyword_hits)
    level = get_level(total_score)

    if total_score >= 90:
        core_comment = random.choice(sum_high)
        adv_count, prob_count, sug_count, act_count = 4, 2, 4, 4
    elif total_score >= 80:
        core_comment = random.choice(sum_mid)
        adv_count, prob_count, sug_count, act_count = 3, 3, 5, 4
    else:
        core_comment = random.choice(sum_low)
        adv_count, prob_count, sug_count, act_count = 2, 4, 5, 5

    result = {
        "total_score": total_score,
        "level": level,
        "core_comment": core_comment,
        "dimension_scores": dimension_scores,
        "advantages": pick(advantages, adv_count),
        "problems": pick(problems, prob_count),
        "suggestions": pick(suggestions, sug_count),
        "next_actions": pick(next_actions, act_count)
    }
    return result