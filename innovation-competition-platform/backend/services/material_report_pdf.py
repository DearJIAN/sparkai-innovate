import os
import json
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_RIGHT, TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, PageBreak, KeepTogether
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
ACCENT = HexColor("#2563EB")
SLATE = HexColor("#334155")
MUTED = HexColor("#94A3B8")
LIGHT_BG = HexColor("#F8FAFC")
WHITE = HexColor("#FFFFFF")
BORDER = HexColor("#E2E8F0")
GREEN = HexColor("#10B981")
ORANGE = HexColor("#F59E0B")
RED = HexColor("#EF4444")
PURPLE = HexColor("#6366F1")
LIGHT_PURPLE = HexColor("#A78BFA")
DARK_BG = HexColor("#1E293B")

COVER_BG = HexColor("#FFFFFF")
COVER_TEXT_PRIMARY = HexColor("#1E293B")
COVER_TEXT_SECONDARY = HexColor("#475569")
COVER_TEXT_TERTIARY = HexColor("#64748B")
COVER_ACCENT = HexColor("#2563EB")
COVER_CARD_BG = HexColor("#F8FAFC")
COVER_CARD_BORDER = HexColor("#E2E8F0")
COVER_TOP_BAR = HexColor("#2563EB")
COVER_SCORE_BG = HexColor("#EFF6FF")
COVER_SCORE_BORDER = HexColor("#BFDBFE")


class CoverFlowable(Flowable):
    def __init__(self, width, evaluation):
        Flowable.__init__(self)
        self.width = width
        self.height = A4[1] - 68*mm
        self._e = evaluation

    def _draw_spark_logo(self, c, cx, y):
        c.setFillColor(COVER_ACCENT)
        p = c.beginPath()
        p.moveTo(cx, y + 7)
        p.lineTo(cx + 3, y + 2)
        p.lineTo(cx + 8, y)
        p.lineTo(cx + 3, y - 2)
        p.lineTo(cx, y - 7)
        p.lineTo(cx - 3, y - 2)
        p.lineTo(cx - 8, y)
        p.lineTo(cx - 3, y + 2)
        p.close()
        c.drawPath(p, fill=1, stroke=0)

    def _draw_accent_line(self, c, cx, y, w):
        c.setStrokeColor(COVER_ACCENT)
        c.setLineWidth(2)
        c.line(cx - w/2, y, cx + w/2, y)

    def _draw_dotted_line(self, c, x1, y, x2):
        c.setStrokeColor(COVER_CARD_BORDER)
        c.setLineWidth(0.5)
        c.setDash([3, 3])
        c.line(x1, y, x2, y)
        c.setDash([])

    def draw(self):
        c = self.canv
        w = self.width
        h = self.height

        c.setFillColor(COVER_BG)
        c.rect(0, 0, w, h, fill=1, stroke=0)
        cx = w / 2

        score_value = self._e.total_score or 0
        advantages = json.loads(self._e.advantages_json) if self._e.advantages_json else []
        problems = json.loads(self._e.problems_json) if self._e.problems_json else []
        suggestions = json.loads(self._e.suggestions_json) if self._e.suggestions_json else []
        lvl = self._e.level or _level_text(score_value)

        cur = h

        # === TOP BLUE BAR (6pt) ===
        cur -= 6
        c.setFillColor(COVER_TOP_BAR)
        c.rect(0, cur, w, 6, fill=1, stroke=0)

        # === SPARK LOGO ===
        cur -= 22
        self._draw_spark_logo(c, cx, cur)

        # === BRAND NAME (10pt) ===
        cur -= 16
        c.setFillColor(COVER_TEXT_SECONDARY)
        c.setFont(_font_bold, 10)
        c.drawCentredString(cx, cur, "火花智创  SparkAI Innovate")

        # === ACCENT LINE ===
        cur -= 12
        self._draw_accent_line(c, cx, cur, 60)

        # === REPORT TYPE (26pt) ===
        cur -= 34
        type_label = "路演PPT评估报告" if self._e.evaluation_type == "ppt" else "项目报告评估报告"
        c.setFillColor(COVER_TEXT_PRIMARY)
        c.setFont(_font_bold, 26)
        c.drawCentredString(cx, cur, type_label)

        # === SUBTITLE (10pt) ===
        cur -= 20
        c.setFont(_font_name, 10)
        c.setFillColor(COVER_TEXT_TERTIARY)
        c.drawCentredString(cx, cur, "数据驱动  ·  智能分析  ·  精准优化")

        # === SCORE CARD (light blue background with subtle shadow) ===
        score_card_h = 100
        score_card_w = 180
        box_bottom = cur - 16 - score_card_h
        # Shadow
        c.setFillColor(HexColor("#E2E8F0"))
        c.roundRect(cx - score_card_w / 2 + 2, box_bottom - 2, score_card_w, score_card_h, 12, fill=1, stroke=0)
        c.setFillColor(COVER_SCORE_BG)
        c.roundRect(cx - score_card_w / 2, box_bottom, score_card_w, score_card_h, 12, fill=1, stroke=0)
        c.setStrokeColor(COVER_SCORE_BORDER)
        c.setLineWidth(1)
        c.roundRect(cx - score_card_w / 2, box_bottom, score_card_w, score_card_h, 12, fill=0, stroke=1)

        # Score number (48pt)
        score_cy = box_bottom + 58
        c.setFont(_font_bold, 48)
        c.setFillColor(COVER_ACCENT)
        c.drawCentredString(cx, score_cy, str(score_value))

        # Score label (10pt)
        c.setFont(_font_name, 10)
        c.setFillColor(COVER_TEXT_TERTIARY)
        c.drawCentredString(cx, score_cy - 22, "综合评分")

        # Level badge
        lvl_color = _level_color(score_value)
        badge_w = 56
        badge_h_val = 20
        badge_y = box_bottom - badge_h_val - 8
        c.setFillColor(lvl_color)
        c.roundRect(cx - badge_w / 2, badge_y, badge_w, badge_h_val, 6, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont(_font_bold, 10)
        c.drawCentredString(cx, badge_y + 4, lvl)

        # === META INFO (9pt) ===
        cur = badge_y - 20
        c.setFont(_font_name, 9)
        c.setFillColor(COVER_TEXT_TERTIARY)
        meta_lines = [
            f"文件：{self._e.file_name or '未知'}",
            f"评估类型：{'PPT评估' if self._e.evaluation_type == 'ppt' else '报告评估'}",
            f"生成时间：{datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}",
            f"报告编号：REP-{self._e.id}-{datetime.utcnow().strftime('%Y%m')}"
        ]
        for i, line in enumerate(meta_lines):
            c.drawCentredString(cx, cur - i * 13, line)

        # === DOTTED SEPARATOR ===
        cur = cur - 4 * 13 - 14
        self._draw_dotted_line(c, cx - 120, cur, cx + 120)

        # === 综合评价 ===
        cur -= 20
        c.setFont(_font_bold, 12)
        c.setFillColor(COVER_TEXT_PRIMARY)
        c.drawCentredString(cx, cur, "综 合 评 价")
        one_liner = _get_one_liner(score_value)
        cur -= 18
        c.setFont(_font_name, 10)
        c.setFillColor(COVER_TEXT_SECONDARY)
        c.drawCentredString(cx, cur, one_liner)

        # === THREE INFO CARDS (vertical full-width layout) ===
        cur -= 18
        card_w = w - 32
        card_x = cx - card_w / 2
        card_gap = 10
        card_data = [
            (GREEN, "核 心 优 势", advantages[:2]),
            (ORANGE, "主 要 风 险", problems[:2]),
            (ACCENT, "优 化 方 向", suggestions[:2])
        ]

        for idx, (color, label, items) in enumerate(card_data):
            item_count = len(items) if items else 0
            card_h = 36 + item_count * 18 if item_count > 0 else 36
            card_y = cur - card_h

            # Card shadow
            c.setFillColor(HexColor("#E2E8F0"))
            c.roundRect(card_x + 1, card_y - 1, card_w, card_h, 8, fill=1, stroke=0)
            c.setFillColor(COVER_CARD_BG)
            c.roundRect(card_x, card_y, card_w, card_h, 8, fill=1, stroke=0)
            c.setStrokeColor(COVER_CARD_BORDER)
            c.setLineWidth(0.5)
            c.roundRect(card_x, card_y, card_w, card_h, 8, fill=0, stroke=1)

            # Color indicator bar at left
            c.setFillColor(color)
            c.roundRect(card_x, card_y, 4, card_h, 0, fill=1, stroke=0)

            # Label
            c.setFont(_font_bold, 10)
            c.setFillColor(color)
            c.drawString(card_x + 14, card_y + card_h - 18, label)

            # Content items
            c.setFont(_font_name, 9)
            c.setFillColor(COVER_TEXT_SECONDARY)
            if items:
                for di, item in enumerate(items[:3]):
                    item_text = item[:80] + "..." if len(item) > 80 else item
                    c.drawString(card_x + 14, card_y + card_h - 36 - di * 16, f"• {item_text}")
            else:
                c.drawString(card_x + 14, card_y + card_h - 36, "暂无数据")

            cur = card_y - card_gap

        # === FOOTER ===
        cur -= 16
        c.setFont(_font_name, 8)
        c.setFillColor(COVER_TEXT_TERTIARY)
        c.drawCentredString(cx, cur, "本报告由火花智创 SparkAI Innovate · AI材料评估系统自动生成")
        cur -= 12
        c.drawCentredString(cx, cur, "报告仅供学习和参赛参考，不构成任何形式的法律或专业建议")


def _get_one_liner(score):
    if score >= 90:
        return "该材料整体表现优秀，在多个维度上达到了较高水准"
    elif score >= 80:
        return "该材料整体表现良好，具备较强的参赛展示基础"
    elif score >= 70:
        return "该材料具备较完整的表达基础，核心逻辑较为清晰"
    else:
        return "该材料具备基础框架，但在深度、细节或表达完整性上仍有提升空间"


def _get_styles():
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        "SectionH2", fontName=_font_bold, fontSize=14, leading=20,
        textColor=NAVY, spaceBefore=10, spaceAfter=6
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
        "TableCell", fontName=_font_name, fontSize=9, leading=14,
        textColor=NAVY
    ))
    styles.add(ParagraphStyle(
        "TableHeader", fontName=_font_bold, fontSize=9, leading=14,
        textColor=WHITE
    ))
    styles.add(ParagraphStyle(
        "TableScore", fontName=_font_bold, fontSize=10, leading=14,
        textColor=NAVY, alignment=TA_CENTER
    ))
    styles.add(ParagraphStyle(
        "BulletItem", fontName=_font_name, fontSize=10, leading=16,
        textColor=NAVY, leftIndent=14, spaceAfter=4, bulletIndent=0
    ))
    styles.add(ParagraphStyle(
        "ActionItem", fontName=_font_name, fontSize=10, leading=16,
        textColor=NAVY, leftIndent=14, spaceAfter=5, bulletIndent=0
    ))
    styles.add(ParagraphStyle(
        "SectionTitle", fontName=_font_bold, fontSize=16, leading=22,
        textColor=NAVY, spaceBefore=4, spaceAfter=8
    ))
    styles.add(ParagraphStyle(
        "PageHeader", fontName=_font_bold, fontSize=10, leading=14,
        textColor=WHITE, spaceBefore=0, spaceAfter=0
    ))
    styles.add(ParagraphStyle(
        "Guide", fontName=_font_name, fontSize=9, leading=14,
        textColor=MUTED, spaceAfter=8
    ))
    return styles


def _build_section_header(text, styles):
    accent_hr = HRFlowable(width=14*mm, thickness=3, color=PURPLE, spaceAfter=2, spaceBefore=8)
    title = Paragraph(text, styles["SectionH2"])
    return [accent_hr, title]


def _build_bullet(text, color_hex):
    return Paragraph(
        f"<font color='#{color_hex}' size='10'>\u25cf</font>  {text}",
        ParagraphStyle(
            "Bullet", fontName=_font_name, fontSize=10, leading=16,
            textColor=NAVY, leftIndent=14, spaceAfter=4
        )
    )


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


def _build_dimension_table(dim_scores, page_w, styles):
    if not dim_scores:
        return Paragraph("暂无可用的评分维度数据", styles["Body"])

    dim_data = [[
        Paragraph("评分维度", styles["TableHeader"]),
        Paragraph("得分", styles["TableHeader"]),
        Paragraph("得分率", styles["TableHeader"]),
        Paragraph("评估说明", styles["TableHeader"])
    ]]

    for ds in dim_scores:
        name = ds["name"]
        sc = ds["score"]
        mx = ds["max_score"]
        ratio = sc / mx if mx > 0 else 0
        pct = f"{round(ratio * 100)}%"
        sc_color = _score_color(sc, mx)

        bar_count = max(1, round(ratio * 12))
        bar_chars = "\u2588" * bar_count + "\u2591" * (12 - bar_count)
        bar_html = f"<font color='#{sc_color.hexval()[:6]}'>{bar_chars}</font>"

        dim_data.append([
            Paragraph(f"<b>{name}</b>", styles["TableCell"]),
            Paragraph(
                f"<font color='#{sc_color.hexval()[:6]}'><b>{sc}</b></font> / {mx}",
                styles["TableScore"]
            ),
            Paragraph(
                f"{bar_html}<br/><font size='7' color='#64748b'>{pct}</font>",
                ParagraphStyle("BarCell", parent=styles["TableCell"], alignment=TA_CENTER)
            ),
            Paragraph(ds.get("comment", ""), styles["TableCell"])
        ])

    col_widths = [28*mm, 22*mm, 34*mm, page_w - 84*mm]
    dim_table = Table(dim_data, colWidths=col_widths, repeatRows=1)
    dim_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PURPLE),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("ALIGN", (1, 0), (2, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, LIGHT_BG]),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ]))
    return dim_table


def generate_report_pdf(evaluation, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    filename = f"evaluation_report_{evaluation.id}_{timestamp}.pdf"
    filepath = os.path.join(output_dir, filename)

    doc = SimpleDocTemplate(filepath, pagesize=A4,
                            leftMargin=20*mm, rightMargin=20*mm,
                            topMargin=18*mm, bottomMargin=20*mm)

    PAGE_W = A4[0] - 40*mm

    styles = _get_styles()
    story = []

    story.append(CoverFlowable(PAGE_W, evaluation))
    story.append(PageBreak())

    dim_scores = json.loads(evaluation.dimension_scores_json) if evaluation.dimension_scores_json else []

    sec_header = _build_section_header("评分维度总览", styles)
    for s in sec_header:
        story.append(s)

    story.append(Paragraph(
        "以下表格展示了各评估维度的得分情况与详细评估说明。得分率以进度条直观呈现，"
        + ("PPT评估维度侧重路演表达的完整性、逻辑性和说服力。"
           if evaluation.evaluation_type == "ppt"
           else "报告评估维度侧重材料内容的论证深度、数据支撑和商业可行性。"),
        styles["Guide"]
    ))
    story.append(_build_dimension_table(dim_scores, PAGE_W, styles))
    story.append(Spacer(1, 6*mm))

    story.append(HRFlowable(width="100%", thickness=0.5, color=BORDER, spaceAfter=4, spaceBefore=4))

    sec_header2 = _build_section_header("核心评价", styles)
    for s in sec_header2:
        story.append(s)

    core_text = evaluation.core_comment or "暂无核心评价内容。"
    core_p = Paragraph(core_text, styles["Body"])
    story.append(core_p)

    story.append(Spacer(1, 6*mm))
    story.append(HRFlowable(width="100%", thickness=0.5, color=BORDER, spaceAfter=4, spaceBefore=2))

    advantages = json.loads(evaluation.advantages_json) if evaluation.advantages_json else []
    problems = json.loads(evaluation.problems_json) if evaluation.problems_json else []
    suggestions = json.loads(evaluation.suggestions_json) if evaluation.suggestions_json else []
    next_actions = json.loads(evaluation.next_actions_json) if evaluation.next_actions_json else []

    has_extra_content = bool(advantages) or bool(problems) or bool(suggestions)
    if has_extra_content:
        story.append(PageBreak())

    if advantages:
        sec_header3 = _build_section_header("主要优势", styles)
        for s in sec_header3:
            story.append(s)
        for item in advantages:
            story.append(_build_bullet(item, "10B981"))

    if problems:
        story.append(Spacer(1, 3*mm))
        sec_header4 = _build_section_header("待改进项", styles)
        for s in sec_header4:
            story.append(s)
        for item in problems:
            story.append(_build_bullet(item, "F59E0B"))

    if suggestions:
        story.append(Spacer(1, 3*mm))
        sec_header5 = _build_section_header("优化建议", styles)
        for s in sec_header5:
            story.append(s)
        for item in suggestions:
            story.append(_build_bullet(item, "2563EB"))

    if next_actions:
        story.append(Spacer(1, 6*mm))
        story.append(HRFlowable(width="100%", thickness=0.5, color=BORDER, spaceAfter=4, spaceBefore=2))

        sec_header6 = _build_section_header("下一步行动", styles)
        for s in sec_header6:
            story.append(s)
        for i, item in enumerate(next_actions, 1):
            story.append(Paragraph(
                f"<font color='#6366F1'><b>{i}.</b></font>  {item}",
                styles["ActionItem"]
            ))

    story.append(Spacer(1, 20*mm))
    story.append(HRFlowable(width="100%", thickness=0.5, color=BORDER, spaceAfter=4))
    story.append(Paragraph(
        "本报告由火花智创 SparkAI Innovate \u00b7 AI材料评估系统自动生成，仅供学习参考。",
        styles["Small"]
    ))

    doc.build(story)
    return filepath