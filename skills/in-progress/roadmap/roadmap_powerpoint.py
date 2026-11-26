"""PowerPoint roadmap rendering and template creation."""

from __future__ import annotations

import math
from pathlib import Path

from roadmap_model import (
    LEGEND_LABEL,
    LOGO_SLOT_TEXT,
    Roadmap,
    dates,
    estimated,
    short,
    subtitle,
    unscheduled_lines,
)
from roadmap_theme import BAND, GRID, LABEL_RULE, PLAIN_LANE, STRONG, mix, roles, theme_colors


# --- text fitting ----------------------------------------------------------------------

# Conservative average advances for a bold theme font, in em. PowerPoint wraps wider than the
# QuickLook preview, so these are calibrated against a PowerPoint PDF export, not the thumbnail.
CHAR_EM, SPACE_EM, LINE_EM = 0.62, 0.3, 1.25


def wrap(value: str, width: float, size: float) -> tuple[int, bool]:
    """Greedy word wrap: (line count, whether every word fits the width on its own)."""
    lines, used, words_fit = 0, 0.0, True
    for word in value.split():
        w = len(word) * size * CHAR_EM
        words_fit &= w <= width
        if lines == 0 or used + size * SPACE_EM + w > width:
            lines, used = lines + 1, w
        else:
            used += size * SPACE_EM + w
    return lines, words_fit


def fits(paragraphs: list[tuple[str, float]], width: float, height: float) -> bool:
    total, ok = 0.0, True
    for value, size in paragraphs:
        n, words_fit = wrap(value, width, size)
        total, ok = total + n * size * LINE_EM, ok and words_fit
    return ok and total <= height


# --- PowerPoint ------------------------------------------------------------------------

# Geometry in a 1280x720 px design space scaled to the slide width (1 px = 9525 EMU on 13.333 in).
LEFT, RIGHT, LANE_W, HEAD_H, HEADER_H, CHART_TOP = 48, 1232, 180, 22, 128, 168
RULE = 1.34  # px; 1 pt on a 13.333 in slide. Rules never go below MIN_LINE on smaller slides.
MIN_LINE = 12700  # EMU; 1 pt, the thinnest line QuickLook still draws
NAME_PX, DATES_PX, LANE_PX = (12.5, 11.5), 10.5, 15  # a bar name shrinks one step before it warns
BAR_PAD = (9, 3, 9, 3)  # left, top, right, bottom text margins inside a bar
LANE_PAD = (14, 0, 10, 0)
LOGO_BOX = (1112, 34, 120, 40)
LOGO_TINT = 0.12  # slot fill, so the slot shows where a viewer drops the dashed line


def render_pptx(r: Roadmap, path: Path, template: Path | None, logo: Path | None = None) -> list[str]:
    """Write the slides; return one overflow warning per lane label or bar that won't fit."""
    from pptx import Presentation
    from pptx.enum.dml import MSO_LINE_DASH_STYLE, MSO_THEME_COLOR
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
    from pptx.oxml.ns import qn
    from pptx.util import Emu, Pt

    prs = Presentation(str(template)) if template else Presentation()
    if template:  # keep the masters and layouts, drop the template's own slides
        ids = prs.slides._sldIdLst
        for sld in list(ids):
            prs.part.drop_rel(sld.rId)
            ids.remove(sld)
    else:
        prs.slide_width, prs.slide_height = Emu(1280 * 9525), Emu(720 * 9525)
    colors = theme_colors(prs)
    role = roles(colors)
    band = r.layout == "band"
    unit = prs.slide_width / 1280
    # Text scales with the slide; rounded so a nominal 13.333 in template keeps exact sizes.
    text_scale = round(unit / 9525, 3)
    warnings: list[str] = []

    def px(v: float) -> Emu:
        return Emu(int(round(v * unit)))

    def fpt(v: float) -> Pt:
        """Design px to points. Text scales with the slide like the geometry, so text fitting
        in design px holds for any slide width."""
        return Pt(v * 0.75 * text_scale)

    def thin(v: float) -> float:
        """A rule thickness in design px, raised so it lands at MIN_LINE EMU or more."""
        return max(v, math.ceil(MIN_LINE / unit * 1000) / 1000)

    rule = thin(RULE)

    def paint(fmt, slot: str, alpha: float | None = None, brightness: float = 0.0):
        """Theme colour, optionally lightened (brightness) or made translucent (alpha)."""
        # Slides reference dk1/lt1/dk2/lt2 through the master's colour map (tx1/bg1/tx2/bg2).
        fmt.theme_color = getattr(MSO_THEME_COLOR, {"dk1": "TEXT_1", "lt1": "BACKGROUND_1", "dk2": "TEXT_2",
                                                     "lt2": "BACKGROUND_2"}.get(slot, slot.upper().replace("ACCENT", "ACCENT_")))
        if brightness:
            fmt.brightness = brightness
        if alpha is not None:
            el = fmt._color._xClr
            for old in el.findall(qn("a:alpha")):
                el.remove(old)
            el.append(el.makeelement(qn("a:alpha"), {"val": str(int(alpha * 100000))}))

    def shape(slide, x, y, w, h, fill=None, alpha=None, kind=MSO_SHAPE.RECTANGLE):
        s = slide.shapes.add_shape(kind, px(x), px(y), px(w), px(h))
        s.shadow.inherit = False
        if fill is None:
            s.fill.background()
        else:
            s.fill.solid()
            paint(s.fill.fore_color, fill, alpha)
        s.line.fill.background()
        return s

    def outline(s, slot, width=1.5, dashed=True):
        # A theme reference, like every other colour. QuickLook draws theme-coloured lines black
        # (PowerPoint draws them right), so a line that must show on a dark fill also gets a tint.
        paint(s.line.color, slot)
        s.line.width = Emu(max(MIN_LINE, px(width)))
        if dashed:
            s.line.dash_style = MSO_LINE_DASH_STYLE.DASH

    def write(target, paras, anchor=MSO_ANCHOR.TOP, align=PP_ALIGN.LEFT, margins=(0, 0, 0, 0)):
        """paras: (text, size_px, bold, ink) per paragraph. ink is a slot or (slot, brightness);
        a size or ink of None inherits from the placeholder. Fonts always come from the theme."""
        tf = target.text_frame
        tf.word_wrap, tf.vertical_anchor = True, anchor
        tf.margin_left, tf.margin_top, tf.margin_right, tf.margin_bottom = (px(m) for m in margins)
        tf.clear()
        for i, (value, size, bold, ink) in enumerate(paras):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.alignment = align
            run = p.add_run()
            run.text = value
            run.font.bold = bold
            if size is not None:
                run.font.size = fpt(size)
            if ink is not None:
                slot, light = ink if isinstance(ink, tuple) else (ink, 0.0)
                paint(run.font.color, slot, brightness=light)
        return target

    def text(slide, x, y, w, h, paras, **kw):
        return write(slide.shapes.add_textbox(px(x), px(y), px(w), px(h)), paras, **kw)

    def to_back(slide, s):
        tree = slide.shapes._spTree
        tree.remove(s._element)
        tree.insert(2, s._element)

    def layout():
        by_name = {l.name.lower(): l for l in prs.slide_layouts}
        return by_name.get("title only") or min(prs.slide_layouts, key=lambda l: len(l.placeholders))

    def header(title: str):
        slide = prs.slides.add_slide(layout())
        if band:
            to_back(slide, shape(slide, 0, 0, 1280, HEADER_H, "accent1"))
            shape(slide, LEFT, HEADER_H - 4, 64, 4, role["stripe"])
        title_w = (LOGO_BOX[0] - 16 if r.logo is not False else RIGHT) - LEFT
        t = slide.shapes.title or slide.shapes.add_textbox(0, 0, 0, 0)
        t.left, t.top, t.width, t.height = px(LEFT), px(26), px(title_w), px(52)
        if band:
            line = (title, 40, False, role["on_accent"])
        elif template:  # plain on a template: its own title size and colour
            line = (title, None, None, None)
        else:
            line = (title, 37, False, "dk1")
        write(t, [line], anchor=MSO_ANCHOR.TOP)
        sub_ink = role["on_accent"] if band else ("dk1", 0.35)
        text(slide, LEFT, 82, title_w, 22, [(subtitle(r), 14, False, sub_ink)])
        draw_logo(slide)
        return slide

    def draw_logo(slide):
        if r.logo is False:
            return
        x, y, w, h = LOGO_BOX
        if logo is not None and logo.is_file():
            pic = slide.shapes.add_picture(str(logo), px(x), px(y))
            scale = min(px(w) / pic.width, px(h) / pic.height)
            pic.width, pic.height = int(pic.width * scale), int(pic.height * scale)
            pic.left, pic.top = px(x + w) - pic.width, px(y)
            return
        ink = role["on_accent"] if band else "accent1"
        slot = shape(slide, x, y, w, h, ink, LOGO_TINT)
        outline(slot, ink, RULE)
        write(slot, [(line, 10, False, ink) for line in LOGO_SLOT_TEXT], anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)

    # --- timeline slide ---------------------------------------------------------------
    slide = header(r.title)
    grid_x = LEFT + LANE_W
    grid_w = RIGHT - grid_x
    n = len(r.weeks)
    col_w = grid_w / n
    lanes = r.lanes()
    total_rows = sum(len(rows) for _, rows in lanes) or 1
    row_h = min(62, 470 // total_rows)
    body_top = CHART_TOP + HEAD_H
    body_bottom = body_top + row_h * total_rows

    for i, week in enumerate(r.weeks):
        text(slide, grid_x + col_w * i + 6, CHART_TOP, col_w - 6, HEAD_H, [(short(week), 12, True, role["accent_ink"])])

    y = body_top
    spans = []
    for k, (theme, rows) in enumerate(lanes):
        h = row_h * len(rows)
        if k % 2:
            shape(slide, grid_x, y, grid_w, h, "accent1", BAND)
        label = shape(slide, LEFT, y, LANE_W, h, "accent1", None if band else PLAIN_LANE)
        write(label, [(theme, LANE_PX, True, role["on_accent"] if band else "dk1")],
              anchor=MSO_ANCHOR.MIDDLE, margins=LANE_PAD)
        if not fits([(theme, LANE_PX)], LANE_W - LANE_PAD[0] - LANE_PAD[2], h):
            warnings.append(f'{r.layout}: lane label "{theme}" overflows its {LANE_W}px label cell')
        spans.append((y, h, rows))
        y += h

    for ly, h, rows in spans:  # rules between rows inside a lane
        for j in range(1, len(rows)):
            shape(slide, grid_x, ly + row_h * j - rule / 2, grid_w, rule, "accent1", GRID)
    for i in range(n + 1):  # a rule at every week boundary, including the right edge
        x = grid_x + col_w * i - (rule if i == n else 0)
        shape(slide, x, body_top, rule, body_bottom - body_top, "accent1", GRID)
    for k, (ly, h, _) in enumerate(spans):  # stronger rules between lanes, across the label column
        edge = ly + h - (rule if k == len(spans) - 1 else rule / 2)
        shape(slide, grid_x, edge, grid_w, rule, "accent1", STRONG)
        if k < len(spans) - 1:
            if band:
                shape(slide, LEFT, edge, LANE_W, rule, "lt1", LABEL_RULE)
            else:
                shape(slide, LEFT, edge, LANE_W, rule, "accent1", STRONG)

    offset = r.today_offset()  # drawn before the bars so it sits behind them
    if offset is not None:
        tx = grid_x + grid_w * offset
        today_w = thin(2)
        shape(slide, tx - today_w / 2, body_top, today_w, body_bottom - body_top, "accent1")

    for ly, _, rows in spans:
        for j, row in enumerate(rows):
            for m in row:
                a, b = r.span(m)
                x, w, h = grid_x + col_w * a + 3, col_w * (b - a + 1) - 6, row_h - 10
                firm = not estimated(m)
                bar = shape(slide, x, ly + row_h * j + 5, w, h, "accent1" if firm else "lt1",
                            kind=MSO_SHAPE.ROUNDED_RECTANGLE)
                bar.adjustments[0] = min(0.5, 6 / min(w, h))
                if not firm:
                    outline(bar, "accent1")
                ink = role["on_accent"] if firm else role["accent_ink"]
                inner_w, inner_h = w - BAR_PAD[0] - BAR_PAD[2], h - BAR_PAD[1] - BAR_PAD[3]
                size = next((s for s in NAME_PX if fits([(m["name"], s), (dates(m), DATES_PX)], inner_w, inner_h)), None)
                if size is None:
                    size = NAME_PX[-1]
                    warnings.append(f'{r.layout}: bar "{m["name"]}" ({m["theme"]}) overflows its {b - a + 1}-week bar')
                paras = [(m["name"], size, True, ink), (dates(m), DATES_PX, False, ink)]
                write(bar, paras, anchor=MSO_ANCHOR.MIDDLE, margins=BAR_PAD)

    if offset is not None:
        pill = shape(slide, tx - 21, body_bottom + 8, 42, 15, "accent1", kind=MSO_SHAPE.ROUNDED_RECTANGLE)
        pill.adjustments[0] = 0.5
        write(pill, [("Today", 10, True, role["on_accent"])], anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)

    lx = LEFT
    for state in r.legend():
        key = shape(slide, lx, 688, 22, 12, "lt1" if state else "accent1", kind=MSO_SHAPE.ROUNDED_RECTANGLE)
        if state:
            outline(key, "accent1")
        text(slide, lx + 28, 686, 110, 16, [(LEGEND_LABEL[state], 11, False, role["accent_ink"])])
        lx += 140

    # --- not-on-the-timeline slide ------------------------------------------------------
    sections = [
        ("Outside this window", [f"{m['name']} ({m['theme']}): {dates(m)}" for m in r.outside]),
        ("Unscheduled", unscheduled_lines(r)),
    ]
    sections = [(t, lines) for t, lines in sections if lines]
    if sections:
        slide = header(f"{r.title}: not on the timeline")
        paras = []
        for heading, lines in sections:
            paras.append((heading, 20, True, "dk1"))
            paras += [(f"•  {line}", 16, False, "dk1") for line in lines]
        box = text(slide, LEFT, 176, RIGHT - LEFT, 480, paras)
        for p in box.text_frame.paragraphs:
            p.space_after = Pt(8)

    prs.save(str(path))
    return warnings


# --- template builder ------------------------------------------------------------------


def make_template(path: Path, colors: dict[str, str], font: str | None) -> None:
    """Write a minimal 16:9 template: theme colour slots, theme typeface, and a title placed for 16:9."""
    from lxml import etree
    from pptx import Presentation
    from pptx.opc.constants import RELATIONSHIP_TYPE as RT
    from pptx.util import Emu

    a = "http://schemas.openxmlformats.org/drawingml/2006/main"
    p = "http://schemas.openxmlformats.org/presentationml/2006/main"
    prs = Presentation()
    prs.slide_width, prs.slide_height = Emu(1280 * 9525), Emu(720 * 9525)
    master = prs.slide_masters[0]
    theme_part = master.part.part_related_by(RT.THEME)
    theme = etree.fromstring(theme_part.blob)
    scheme = theme.find(f".//{{{a}}}clrScheme")
    scheme.set("name", "Custom")
    for name, hex_ in colors.items():
        slot = scheme.find(f"{{{a}}}{name}")
        for child in list(slot):
            slot.remove(child)
        etree.SubElement(slot, f"{{{a}}}srgbClr", val=hex_)
    if font:
        for kind in ("majorFont", "minorFont"):
            theme.find(f".//{{{a}}}{kind}/{{{a}}}latin").set("typeface", font)
    theme_part._blob = etree.tostring(theme, xml_declaration=True, encoding="UTF-8", standalone=True)

    title_style = master._element.find(f".//{{{p}}}titleStyle/{{{a}}}lvl1pPr/{{{a}}}defRPr")
    title_style.set("sz", "2800")
    title_style.set("b", "1")
    for fill in title_style.findall(f"{{{a}}}solidFill"):
        title_style.remove(fill)
    fill = etree.Element(f"{{{a}}}solidFill")
    etree.SubElement(fill, f"{{{a}}}schemeClr", val="accent1")
    title_style.insert(0, fill)
    unit = 9525
    for placeholders in [master.placeholders] + [l.placeholders for l in master.slide_layouts]:
        for ph in placeholders:
            if "TITLE" in str(ph.placeholder_format.type) and "SUB" not in str(ph.placeholder_format.type):
                ph.left, ph.top, ph.width, ph.height = Emu(38 * unit), Emu(29 * unit), Emu(1204 * unit), Emu(77 * unit)
                ph.text_frame.word_wrap = True
    prs.save(str(path))
