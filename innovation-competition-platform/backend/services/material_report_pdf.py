import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus.flowables import KeepTogether

FONT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "fonts")

try:
    pdfmetrics.registerFont(TTFont("SourceHanSans", os.path.join(FONT_DIR, "SourceHanSansSC-Regular.otf")))
    pdfmetrics.registerFont(TTFont("SourceHanSansBold", os.path.join(FONT_DIR, "SourceHanSansSC-Bold.otf")))
    _font_registered = True
except:
    try:
        from reportlab.pdfbase.cidfonts import UnicodeCIDFont
        pdfmetrics.registerFont(UnicodeCIDFont("STSong-Light"))
        _font_name = "STSong-Light"
        _font_bold = "STSong-Light"
        _font_registered = True
    except:
        _font_registered = False
        _font_name = "Helvetica"
        _font_bold = "Helvetica-Bold"

if _font_registered:
    try:
        _font_name = "SourceHanSans"
        _font_bold = "SourceHanSansBold"
    except:
        pass

PRIMARY_COLOR = HexColor("#2563eb")
SECONDARY_COLOR = HexColor("#7c3aed")
DARK_COLOR = HexColor("#1e293b")
MUTED_COLOR = HexColor("#64748b")
LIGHT_BG = HexColor("#f8fafc")
CARD_BG = HexColor("#ffffff")
BORDER_COLOR = HexColor("#e2e8f0")
GOOD_COLOR = HexColor("#10b981")
WARN_COLOR = HexColor("#f59e0b")
ACCENT_COLOR = HexColor("#3b82f6")
DANGER_COLOR = HexColor("#ef4444")


def _get_styles():
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        "CNTitle", fontName=_font_bold, fontSize=22, leading=30,
        textColor=DARK_COLOR, alignment=TA_CENTER, spaceAfter=6
    ))
    styles.add(ParagraphStyle(
        "CNSubtitle", fontName=_font_name, fontSize=10, leading=14,
        textColor=MUTED_COLOR, alignment=TA_CENTER, spaceAfter=20
    ))
    styles.add(ParagraphStyle(
        "CNH2", fontName=_font_bold, fontSize=14, leading=20,
        textColor=DARK_COLOR, spaceAfter=10, spaceBefore=16
    ))
    styles.add(ParagraphStyle(
        "CNH3", fontName=_font_bold, fontSize=12, leading=18,
        textColor=DARK_COLOR, spaceAfter=8, spaceBefore=12
    ))
    styles.add(ParagraphStyle(
        "CNBody", fontName=_font_name, fontSize=10, leading=16,
        textColor=DARK_COLOR, alignment=TA_JUSTIFY, spaceAfter=8
    ))
    styles.add(ParagraphStyle(
        "CNSmall", fontName=_font_name, fontSize=9, leading=13,
        textColor=MUTED_COLOR, spaceAfter=4
    ))
    styles.add(ParagraphStyle(
        "CNTableCell", fontName=_font_name, fontSize=9, leading=13,
        textColor=DARK_COLOR
    ))
    styles.add(ParagraphStyle(
        "CNTableHeader", fontName=_font_bold, fontSize=9, leading=13,
        textColor=HexColor("#ffffff")
    ))
    styles.add(ParagraphStyle(
        "CNScoreLarge", fontName=_font_bold, fontSize=48, leading=54,
        textColor=PRIMARY_COLOR, alignment=TA_CENTER
    ))
    styles.add(ParagraphStyle(
        "CNLevelTag", fontName=_font_bold, fontSize=13, leading=18,
        textColor=HexColor("#ffffff"), alignment=TA_CENTER
    ))
    styles.add(ParagraphStyle(
        "CNListItem", fontName=_font_name, fontSize=10, leading=16,
        textColor=DARK_COLOR, leftIndent=16, spaceAfter=4, bulletIndent=8
    ))
    return styles


def generate_report_pdf(evaluation, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    filename = f"evaluation_report_{evaluation.id}_{timestamp}.pdf"
    filepath = os.path.join(output_dir, filename)

    doc = SimpleDocTemplate(filepath, pagesize=A4,
                           leftMargin=20*mm, rightMargin=20*mm,
                           topMargin=20*mm, bottomMargin=20*mm)
    styles = _get_styles()
    story = []

    type_label = "路演PPT评估报告" if evaluation.evaluation_type == "ppt" else "项目报告评估报告"
    story.append(Paragraph(type_label, styles["CNTitle"]))
    story.append(Paragraph("数据驱动 · 智能分析 · 精准优化", styles["CNSubtitle"]))
    story.append(HRFlowable(width="100%", thickness=1, color=BORDER_COLOR, spaceAfter=12))

    meta_data = [
        [Paragraph("文件名", styles["CNSmall"]), Paragraph(evaluation.file_name, styles["CNSmall"])],
        [Paragraph("评估类型", styles["CNSmall"]), Paragraph("PPT评估" if evaluation.evaluation_type == "ppt" else "报告评估", styles["CNSmall"])],
        [Paragraph("生成时间", styles["CNSmall"]), Paragraph(datetime.utcnow().strftime("%Y-%m-%d %H:%M"), styles["CNSmall"])]
    ]
    meta_table = Table(meta_data, colWidths=[60*mm, 100*mm])
    meta_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 16*mm))

    score_container = []
    score_container.append(Paragraph(str(evaluation.total_score), styles["CNScoreLarge"]))
    level_color = GOOD_COLOR if evaluation.total_score >= 80 else WARN_COLOR
    level_text = evaluation.level or "良好"
    story.append(KeepTogether([
        Paragraph(str(evaluation.total_score), styles["CNScoreLarge"]),
        Spacer(1, 4*mm),
        Paragraph(f"<font color='{level_color}' size='13'><b>{level_text}</b></font>", ParagraphStyle("LevelCenter", parent=styles["CNBody"], alignment=TA_CENTER)),
        Spacer(1, 12*mm)
    ]))

    story.append(Paragraph("评分维度", styles["CNH2"]))
    import json
    dim_scores = json.loads(evaluation.dimension_scores_json) if evaluation.dimension_scores_json else []
    if dim_scores:
        dim_data = [[
            Paragraph("评分维度", styles["CNTableHeader"]),
            Paragraph("得分", styles["CNTableHeader"]),
            Paragraph("满分", styles["CNTableHeader"]),
            Paragraph("评估说明", styles["CNTableHeader"])
        ]]
        for ds in dim_scores:
            score_color = GOOD_COLOR if ds["score"] >= ds["max_score"] * 0.8 else (WARN_COLOR if ds["score"] >= ds["max_score"] * 0.6 else DANGER_COLOR)
            dim_data.append([
                Paragraph(ds["name"], styles["CNTableCell"]),
                Paragraph(f"<font color='{score_color}'><b>{ds['score']}</b></font>", ParagraphStyle("ScoreCell", parent=styles["CNTableCell"], alignment=TA_CENTER)),
                Paragraph(str(ds["max_score"]), ParagraphStyle("MaxCell", parent=styles["CNTableCell"], alignment=TA_CENTER)),
                Paragraph(ds.get("comment", ""), styles["CNTableCell"])
            ])
        dim_table = Table(dim_data, colWidths=[35*mm, 16*mm, 16*mm, 93*mm])
        dim_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), PRIMARY_COLOR),
            ("TEXTCOLOR", (0, 0), (-1, 0), HexColor("#ffffff")),
            ("ALIGN", (1, 0), (2, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("GRID", (0, 0), (-1, -1), 0.5, BORDER_COLOR),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [CARD_BG, LIGHT_BG]),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ]))
        story.append(dim_table)
        story.append(Spacer(1, 12*mm))

    story.append(Paragraph("核心评价", styles["CNH2"]))
    story.append(Paragraph(evaluation.core_comment or "", styles["CNBody"]))
    story.append(Spacer(1, 8*mm))

    advantages = json.loads(evaluation.advantages_json) if evaluation.advantages_json else []
    if advantages:
        story.append(Paragraph("主要优势", styles["CNH2"]))
        for adv in advantages:
            story.append(Paragraph(f"• {adv}", styles["CNListItem"]))

    problems = json.loads(evaluation.problems_json) if evaluation.problems_json else []
    if problems:
        story.append(Spacer(1, 4*mm))
        story.append(Paragraph("关键问题", styles["CNH2"]))
        for prob in problems:
            story.append(Paragraph(f"• {prob}", styles["CNListItem"]))

    suggestions = json.loads(evaluation.suggestions_json) if evaluation.suggestions_json else []
    if suggestions:
        story.append(Spacer(1, 4*mm))
        story.append(Paragraph("优化建议", styles["CNH2"]))
        for sug in suggestions:
            story.append(Paragraph(f"• {sug}", styles["CNListItem"]))

    next_actions = json.loads(evaluation.next_actions_json) if evaluation.next_actions_json else []
    if next_actions:
        story.append(Spacer(1, 4*mm))
        story.append(Paragraph("下一步行动", styles["CNH2"]))
        for i, act in enumerate(next_actions, 1):
            story.append(Paragraph(f"{i}. {act}", styles["CNListItem"]))

    story.append(Spacer(1, 16*mm))
    story.append(HRFlowable(width="100%", thickness=1, color=BORDER_COLOR, spaceAfter=6))
    story.append(Paragraph("本报告由火花智创 SparkAI Innovate AI材料评估系统生成，仅供学习参考。", styles["CNSmall"]))

    doc.build(story)
    return filepath