"""Shared theme colors, fonts, and contrast calculations."""

from __future__ import annotations

import re

SLOTS = ("dk1", "lt1", "dk2", "lt2", "accent1", "accent2", "accent3", "accent4", "accent5", "accent6")
# python-pptx's default theme, used when no template is given or its theme can't be read.
DEFAULT_THEME = {
    "dk1": "000000", "lt1": "FFFFFF", "dk2": "1F497D", "lt2": "EEECE1", "accent1": "4F81BD",
    "accent2": "C0504D", "accent3": "9BBB59", "accent4": "8064A2", "accent5": "4BACC6", "accent6": "F79646",
}


def theme_colors(prs=None) -> dict[str, str]:
    """RGB hex per theme slot, read from the presentation's first master theme."""
    colors = dict(DEFAULT_THEME)
    if prs is None:
        return colors
    from lxml import etree
    from pptx.opc.constants import RELATIONSHIP_TYPE as RT

    try:
        theme = etree.fromstring(prs.slide_masters[0].part.part_related_by(RT.THEME).blob)
    except (KeyError, IndexError, etree.XMLSyntaxError):
        return colors
    ns = {"a": "http://schemas.openxmlformats.org/drawingml/2006/main"}
    for slot in SLOTS:
        el = theme.find(f".//a:clrScheme/a:{slot}/*", ns)
        if el is not None:
            value = el.get("val") if el.tag.endswith("srgbClr") else el.get("lastClr")
            if value and re.fullmatch(r"[0-9A-Fa-f]{6}", value):
                colors[slot] = value.upper()
    return colors


FONT_FALLBACK = 'system-ui,-apple-system,"Segoe UI",sans-serif'


def theme_fonts(prs=None) -> dict[str, str]:
    """Major (headings) and minor (body) Latin typeface names, read from the first master theme.

    A typeface that names the other slot (+mj-lt, +mn-lt) resolves to it; an empty or
    unresolvable one is dropped, so the HTML falls back to the system stack.
    """
    if prs is None:
        return {}
    from lxml import etree
    from pptx.opc.constants import RELATIONSHIP_TYPE as RT

    try:
        theme = etree.fromstring(prs.slide_masters[0].part.part_related_by(RT.THEME).blob)
    except (KeyError, IndexError, etree.XMLSyntaxError):
        return {}
    ns = {"a": "http://schemas.openxmlformats.org/drawingml/2006/main"}
    raw = {}
    for kind, key in (("majorFont", "major"), ("minorFont", "minor")):
        el = theme.find(f".//a:fontScheme/a:{kind}/a:latin", ns)
        raw[key] = (el.get("typeface") or "").strip() if el is not None else ""
    refs = {"+mj-lt": "major", "+mn-lt": "minor"}
    fonts = {}
    for key, value in raw.items():
        value = raw.get(refs[value], "") if value in refs else value
        if value and not value.startswith("+"):
            fonts[key] = value
    return fonts


def css_font_stack(name: str | None) -> str:
    """A CSS font-family list: the theme typeface, quoted, ahead of the system fallback."""
    if not name:
        return FONT_FALLBACK
    clean = re.sub(r'[\\"<>;{}]', "", name)
    return f'"{clean}",{FONT_FALLBACK}'


def _luminance(hex_: str) -> float:
    def channel(c: float) -> float:
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

    r, g, b = (channel(int(hex_[i:i + 2], 16) / 255) for i in (0, 2, 4))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a: str, b: str) -> float:
    """WCAG contrast ratio between two RGB hex colours."""
    la, lb = sorted((_luminance(a), _luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def roles(c: dict[str, str]) -> dict[str, str]:
    """Theme slot for each drawing role, chosen by contrast against the fill it sits on."""
    on_accent = max(("lt1", "dk1"), key=lambda s: contrast(c[s], c["accent1"]))
    return {
        "on_accent": on_accent,  # text on an Accent 1 fill
        "accent_ink": "accent1" if contrast(c["accent1"], c["lt1"]) >= 4.5 else "dk1",  # text on white
        "stripe": "accent2" if contrast(c["accent2"], c["accent1"]) >= 3 else on_accent,
    }


def mix(fg: str, bg: str, amount: float) -> str:
    """`fg` at `amount` opacity over `bg`, as RGB hex."""
    return "".join(
        f"{round(int(fg[i:i + 2], 16) * amount + int(bg[i:i + 2], 16) * (1 - amount)):02X}" for i in (0, 2, 4)
    )


# Tints are Accent 1 (or Light 1 over Accent 1) at a fixed opacity.
GRID, BAND, STRONG, PLAIN_LANE, LABEL_RULE = 0.11, 0.04, 0.32, 0.08, 0.25
