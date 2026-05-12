import os
import json
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_RIGHT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.platypus.flowables import Flowable

FONT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "fonts")

_font_name = "Helvetica"
_font_bold = "Helvetica-Bold"

try:
    if os.path.isdir(FONT_DIR):
        from reportlab.pdfbase.ttfonts import TTFont
        regular_path = os.path.join(FONT_DIR, "SourceHanSansSC-Regular.otf")
        bold_path = os.path.join(FONT_DIR, "SourceHanSansSC-Bold.otf")
        if os.path.exists(regular_path) and os.path.exists(bold_path):
            pdfmetrics.registerFont(TTFont("SourceHanSans", regular_path))
            pdfmetrics.registerFont(TTFont("SourceHanSansBold", bold_path))
            _font_name = "SourceHanSans"
            _font_bold = "SourceHanSansBold"
        else:
            raise FileNotFoundError("Font files not found")
    else:
        raise FileNotFoundError("Fonts directory not found")
except Exception:
    try:
        pdfmetrics.registerFont(UnicodeCIDFont("STSong-Light"))
        _font_name = "STSong-Light"
        _font_bold = "STSong-Light"
    except Exception:
        _font_name = "Helvetica"
        _font_bold = "Helvetica-Bold"

NAVY = HexColor("#0F172A")
ACCENT = HexColor("#0369A1")
SLATE = HexColor("#334155")
MUTED = HexColor("#94A3B8")
LIGHT_BG = HexColor("#F8FAFC")
WHITE = HexColor("#FFFFFF")
BORDER = HexColor("#E2E8F0")
GREEN = HexColor("#10B981")
ORANGE = HexColor("#F59E0B")
RED = HexColor("#EF4444")
PURPLE = HexColor("#863bff")
LIGHT_PURPLE = HexColor("#A78BFA")

COVER_H = 240


class CoverFlowable(Flowable):
    def __init__(self, width, evaluation):
        Flowable.__init__(self)
        self.width = width
        self.height = COVER_H
        self._e = evaluation

    def draw(self):
        c = self.canv
        w = self.width
        h = self.height

        c.setFillColor(NAVY)
        c.rect(0, 0, w, h, fill=1, stroke=0)

        cx = w / 2

        c.setFillColor(LIGHT_PURPLE)
        p = c.beginPath()
        sp_y = h - 22
        p.moveTo(cx, sp_y + 7)
        p.lineTo(cx + 3, sp_y + 2)
        p.lineTo(cx + 8, sp_y)
        p.lineTo(cx + 3, sp_y - 2)
        p.lineTo(cx, sp_y - 7)
        p.lineTo(cx - 3, sp_y - 2)
        p.lineTo(cx - 8, sp_y)
        p.lineTo(cx - 3, sp_y + 2)
        p.close()
        c.drawPath(p, fill=1, stroke=0)

        type_label = "路演PPT评估报告" if self._e.evaluation_type == "ppt" else "项目报告评估报告"
        c.setFillColor(WHITE)
        c.setFont(_font_bold, 24)
        c.drawCentredString(cx, h - 42, type_label)

        c.setFont(_font_name, 10)
        c.setFillColor(HexColor("#CBD5E1"))
        c.drawCentredString(cx, h - 58, "数据驱动 \u00b7 智能分析 \u00b7 精准优化")

        score_value = self._e.total_score or 0
        c.setFont(_font_bold, 52)
        c.setFillColor(WHITE)
        c.drawCentredString(cx, h - 110, str(score_value))

        lvl = self._e.level or _level_text(score_value)
        lvl_color = _level_color(score_value)
        c.setFillColor(lvl_color)
        badge_w, badge_h = 48, 18
        c.roundRect(cx - badge_w / 2, h - 132, badge_w, badge_h, 4, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont(_font_bold, 9)
        c.drawCentredString(cx, h - 128, lvl)

        c.setFont(_font_name, 8)
        c.setFillColor(MUTED)
        meta_lines = [
            f"文件名：{self._e.file_name}",
            f"评估类型：{'PPT评估' if self._e.evaluation_type == 'ppt' else '报告评估'}",
            f"生成时间：{datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}"
        ]
        for i, line in enumerate(meta_lines):
            c.drawCentredString(cx, h - 155 - i * 11, line)

        c.setStrokeColor(HexColor("#334155"))
        c.setLineWidth(0.5)
        sep_y = h - 195
        c.line(cx - 90, sep_y, cx + 90, sep_y)

        c.setFont(_font_name, 8)
        c.setFillColor(MUTED)
        c.drawCentredString(cx, sep_y - 12, "火花智创 SparkAI \u00b7 AI材料评估系统")


def _get_styles():
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        "SectionH2", fontName=_font_bold, fontSize=14, leading=20,
        textColor=NAVY, spaceBefore=16, spaceAfter=8
    ))
    styles.add(ParagraphStyle(
        "SectionH3", fontName=_font_bold, fontSize=11, leading=16,
        textColor=SLATE, spaceBefore=10, spaceAfter=4
    ))
    styles.add(ParagraphStyle(
        "Body", fontName=_font_name, fontSize=10, leading=16,
        textColor=NAVY, alignment=TA_JUSTIFY, spaceAfter=6
    ))
    styles.add(ParagraphStyle(
        "Small", fontName=_font_name, fontSize=8, leading=12,
        textColor=MUTED, spaceAfter=2
    ))
    styles.add(ParagraphStyle(
        "TableCell", fontName=_font_name, fontSize=9, leading=13,
        textColor=NAVY
    ))
    styles.add(ParagraphStyle(
        "TableHeader", fontName=_font_bold, fontSize=9, leading=13,
        textColor=WHITE
    ))
    styles.add(ParagraphStyle(
        "BulletGreen", fontName=_font_name, fontSize=10, leading=16,
        textColor=NAVY, leftIndent=14, spaceAfter=3, bulletIndent=0
    ))
    styles.add(ParagraphStyle(
        "BulletOrange", fontName=_font_name, fontSize=10, leading=16,
        textColor=NAVY, leftIndent=14, spaceAfter=3, bulletIndent=0
    ))
    styles.add(ParagraphStyle(
        "BulletBlue", fontName=_font_name, fontSize=10, leading=16,
        textColor=NAVY, leftIndent=14, spaceAfter=3, bulletIndent=0
    ))
    styles.add(ParagraphStyle(
        "ActionNum", fontName=_font_name, fontSize=10, leading=16,
        textColor=NAVY, leftIndent=14, spaceAfter=3, bulletIndent=0
    ))
    return styles


def _build_section_header(text, styles):
    accent_hr = HRFlowable(width=18*mm, thickness=3, color=ACCENT, spaceAfter=2)
    title = Paragraph(text, styles["SectionH2"])
    return [accent_hr, title]


def _build_bullet(text, style, color):
    dot_color = f"<font color='#{color}' size='12'>\u25cf</font>"
    return Paragraph(f"{dot_color}  {text}", style)


def _score_color(score, max_score):
    ratio = score / max_score if max_score > 0 else 0
    if ratio >= 0.8:
        return GREEN
    elif ratio >= 0.6:
        return ORANGE
    return RED


def _level_color(score):
    if score >= 80:
        return GREEN
    elif score >= 60:
        return ORANGE
    return RED


def _level_text(score):
    if score >= 90:
        return "优秀"
    elif score >= 80:
        return "良好"
    elif score >= 70:
        return "中等"
    elif score >= 60:
        return "一般"
    return "待改进"


def generate_report_pdf(evaluation, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    filename = f"evaluation_report_{evaluation.id}_{timestamp}.pdf"
    filepath = os.path.join(output_dir, filename)

    doc = SimpleDocTemplate(filepath, pagesize=A4,
                            leftMargin=18*mm, rightMargin=18*mm,
                            topMargin=18*mm, bottomMargin=18*mm)

    PAGE_W = A4[0] - 36*mm
    PAGE_H_CONTENT = A4[1] - 36*mm

    styles = _get_styles()
    story = []

    story.append(CoverFlowable(PAGE_W, evaluation))
    story.append(Spacer(1, 8*mm))

    page_line = HRFlowable(width="100%", thickness=0.5, color=BORDER, spaceAfter=8)
    story.append(page_line)

    dim_scores = json.loads(evaluation.dimension_scores_json) if evaluation.dimension_scores_json else []

    sec_header = _build_section_header("评分维度", styles)
    for s in sec_header:
        story.append(s)

    if dim_scores:
        dim_data = [[
            Paragraph("评分维度", styles["TableHeader"]),
            Paragraph("得分", styles["TableHeader"]),
            Paragraph("满分", styles["TableHeader"]),
            Paragraph("评估说明", styles["TableHeader"])
        ]]
        for ds in dim_scores:
            sc = _score_color(ds["score"], ds["max_score"])
            dim_data.append([
                Paragraph(ds["name"], styles["TableCell"]),
                Paragraph(
                    f"<font color='#{sc.hexval()[:6]}'><b>{ds['score']}</b></font>",
                    ParagraphStyle("SC", parent=styles["TableCell"], alignment=TA_CENTER)
                ),
                Paragraph(str(ds["max_score"]),
                          ParagraphStyle("MC", parent=styles["TableCell"], alignment=TA_CENTER)),
                Paragraph(ds.get("comment", ""), styles["TableCell"])
            ])

        col_widths = [35*mm, 16*mm, 16*mm, PAGE_W - 67*mm]
        dim_table = Table(dim_data, colWidths=col_widths, repeatRows=1)
        dim_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), ACCENT),
            ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
            ("ALIGN", (1, 0), (2, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("GRID", (0, 0), (-1, -1), 0.5, BORDER),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, LIGHT_BG]),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ]))
        story.append(dim_table)
    else:
        story.append(Paragraph("暂无可用的评分维度数据", styles["Body"]))

    story.append(Spacer(1, 8*mm))
    story.append(page_line)

    sec_header2 = _build_section_header("核心评价", styles)
    for s in sec_header2:
        story.append(s)

    core_text = evaluation.core_comment or "暂无核心评价内容。"
    core_p = Paragraph(core_text, styles["Body"])
    core_card = Table([[core_p]], colWidths=[PAGE_W])
    core_card.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), LIGHT_BG),
        ("BOX", (0, 0), (-1, -1), 1, ACCENT),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ]))
    story.append(core_card)

    story.append(Spacer(1, 4*mm))
    story.append(page_line)

    advantages = json.loads(evaluation.advantages_json) if evaluation.advantages_json else []
    if advantages:
        sec_header3 = _build_section_header("主要优势", styles)
        for s in sec_header3:
            story.append(s)
        for adv in advantages:
            story.append(_build_bullet(adv, styles["BulletGreen"], "10B981"))

    problems = json.loads(evaluation.problems_json) if evaluation.problems_json else []
    if problems:
        story.append(Spacer(1, 2*mm))
        sec_header4 = _build_section_header("待改进项", styles)
        for s in sec_header4:
            story.append(s)
        for prob in problems:
            story.append(_build_bullet(prob, styles["BulletOrange"], "F59E0B"))

    suggestions = json.loads(evaluation.suggestions_json) if evaluation.suggestions_json else []
    if suggestions:
        story.append(Spacer(1, 2*mm))
        sec_header5 = _build_section_header("优化建议", styles)
        for s in sec_header5:
            story.append(s)
        for sug in suggestions:
            story.append(_build_bullet(sug, styles["BulletBlue"], "0369A1"))

    next_actions = json.loads(evaluation.next_actions_json) if evaluation.next_actions_json else []
    if next_actions:
        story.append(Spacer(1, 2*mm))
        sec_header6 = _build_section_header("下一步行动", styles)
        for s in sec_header6:
            story.append(s)
        for i, act in enumerate(next_actions, 1):
            story.append(Paragraph(
                f"<font color='#0369A1'><b>{i}.</b></font>  {act}",
                styles["ActionNum"]
            ))

    story.append(Spacer(1, 12*mm))
    story.append(HRFlowable(width="100%", thickness=0.5, color=BORDER, spaceAfter=4))
    story.append(Paragraph(
        "本报告由火花智创 SparkAI Innovate \u00b7 AI材料评估系统自动生成，仅供学习参考。",
        styles["Small"]
    ))
    story.append(Paragraph("第 1 页", ParagraphStyle(
        "PageNum", parent=styles["Small"], alignment=TA_RIGHT
    )))

    doc.build(story)
    return filepath