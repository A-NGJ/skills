"""Markdown and HTML roadmap renderers."""

from __future__ import annotations

import base64
import html
import mimetypes
from pathlib import Path

from roadmap_model import (
    LEGEND_LABEL,
    LOGO_SLOT_TEXT,
    Roadmap,
    as_of_line,
    dates,
    estimated,
    short,
    subtitle,
    unscheduled_lines,
)
from roadmap_theme import BAND, GRID, LABEL_RULE, PLAIN_LANE, STRONG, css_font_stack, mix, roles


# --- Markdown --------------------------------------------------------------------------


def _md_escape(text: str) -> str:
    return text.replace("|", "\\|")


def render_md(r: Roadmap) -> str:
    out = [f"# {r.title}", "", f"_{as_of_line(r)}_", ""]
    out.append("| Theme | " + " | ".join(short(w) for w in r.weeks) + " |")
    out.append("|---|" + "---|" * len(r.weeks))
    for theme, rows in r.lanes():
        for i, row in enumerate(rows):
            cells = [""] * len(r.weeks)
            for m in row:
                a, b = r.span(m)
                cells[a] = f"**{_md_escape(m['name'])}**"
                for j in range(a + 1, b + 1):
                    cells[j] = "▬"
            out.append(f"| {_md_escape(theme) if i == 0 else ''} | " + " | ".join(cells) + " |")
    out += ["", "## Milestones", ""]
    for theme, _ in r.lanes():
        out += [f"**{theme}**", ""]
        out += [f"- {m['name']}: {dates(m)}" for m in r.visible if m["theme"] == theme]
        out.append("")
    if r.outside:
        out += ["## Outside this window", ""]
        out += [f"- {m['name']} ({m['theme']}): {dates(m)}" for m in r.outside]
        out.append("")
    if r.unscheduled:
        out += ["## Unscheduled", ""]
        out += [f"- {line}" for line in unscheduled_lines(r)]
        out.append("")
    return "\n".join(out)


# --- HTML ------------------------------------------------------------------------------

CSS = """
:root{--grid:color-mix(in srgb,var(--accent) 11%,var(--paper));--band:color-mix(in srgb,var(--accent) 4%,var(--paper));
  --strong:color-mix(in srgb,var(--accent) 32%,var(--paper));--muted:color-mix(in srgb,var(--ink) 65%,var(--paper))}
*{box-sizing:border-box}
body{font:14px/1.3 var(--font-body);margin:0;color:var(--ink);background:var(--paper)}
header{position:relative;padding:26px 48px 22px}
h1{margin:0 0 6px;font-family:var(--font-heading);font-size:30px;font-weight:400;padding-right:150px} h2{font-size:16px;margin:24px 0 8px}
.sub{font-size:14px;color:var(--muted)}
.band header{background:var(--accent);color:var(--on-accent)} .band .sub{color:inherit}
.band header::after{content:"";position:absolute;left:48px;bottom:0;width:64px;height:4px;background:var(--stripe)}
.logo{position:absolute;right:48px;top:34px;width:120px;height:40px;display:grid;place-items:center;text-align:center;
  font-size:10px;line-height:1.2;border:1.34px dashed currentColor}
.logo.img{border:0} .logo img{max-width:100%;max-height:100%}
main{padding:24px 48px 16px}
.sl{position:relative;display:grid;grid-template-columns:180px repeat(var(--n),1fr)}
.sl-h{font-size:12px;font-weight:600;color:var(--accent-ink);padding:0 0 6px 6px}
.sl-lane{grid-column:1;font-weight:600;font-size:15px;padding:0 10px 0 14px;display:flex;align-items:center;
  background:var(--lane-bg);color:var(--lane-ink);border-top:1.34px solid var(--lane-rule)}
.sl-lane.first{border-top-color:transparent}
.sl-row{display:grid;grid-template-columns:repeat(var(--n),1fr);align-items:center;min-height:62px;padding:5px 0;
  border-top:1.34px solid var(--grid)}
.sl-row.lane-top{border-top-color:var(--strong)} .sl-row.alt{background:var(--band)}
.cols{grid-column:2 / -1;display:grid;grid-template-columns:repeat(var(--n),1fr);z-index:1;pointer-events:none}
.cols i{border-left:1.34px solid var(--grid)} .cols i:last-child{border-right:1.34px solid var(--grid)}
.sl-row.last{border-bottom:1.34px solid var(--strong)}
.band .sl-lane.first+.sl-row.lane-top{border-top-color:var(--grid)}
.bar{position:relative;z-index:3;margin:0 3px;padding:3px 9px;min-height:52px;border-radius:6px;display:flex;
  flex-direction:column;justify-content:center;background:var(--accent);color:var(--on-accent)}
.bar b{font-size:12.5px;line-height:1.2} .bar span{font-size:10.5px}
.bar.est{background:var(--paper);color:var(--accent-ink);border:1.5px dashed var(--accent)}
.today{position:absolute;top:var(--head);bottom:0;width:2px;margin-left:-1px;background:var(--accent);z-index:2}
.today i{position:absolute;top:calc(100% + 8px);left:50%;transform:translateX(-50%);font:600 10px/1 var(--font-body);
  padding:3px 7px;border-radius:9px;background:var(--accent);color:var(--on-accent);font-style:normal}
.legend{display:flex;gap:18px;font-size:11px;margin-top:40px;color:var(--accent-ink)}
.legend s{display:inline-block;width:22px;height:12px;border-radius:3px;margin-right:6px;vertical-align:-2px;
  background:var(--accent)}
.legend s.est{background:var(--paper);border:1.5px dashed var(--accent)}
@media print{.sl{break-inside:avoid}}
"""


def _logo_html(r: Roadmap, logo: Path | None) -> str:
    if r.logo is False:
        return ""
    if logo is not None and logo.is_file():
        mime = mimetypes.guess_type(logo.name)[0] or "image/png"
        data = base64.b64encode(logo.read_bytes()).decode()
        return f'<div class="logo img"><img alt="Logo" src="data:{mime};base64,{data}"></div>'
    return f'<div class="logo">{LOGO_SLOT_TEXT[0]}<br>{LOGO_SLOT_TEXT[1]}</div>'


def render_html(r: Roadmap, colors: dict[str, str], logo: Path | None = None,
                fonts: dict[str, str] | None = None) -> str:
    e = html.escape
    n = len(r.weeks)
    role = roles(colors)
    band = r.layout == "band"
    css_vars = {
        "--accent": colors["accent1"], "--ink": colors["dk1"], "--paper": colors["lt1"],
        "--on-accent": colors[role["on_accent"]], "--accent-ink": colors[role["accent_ink"]],
        "--stripe": colors[role["stripe"]],
        "--lane-bg": colors["accent1"] if band else mix(colors["accent1"], colors["lt1"], PLAIN_LANE),
        "--lane-ink": colors[role["on_accent"]] if band else colors["dk1"],
        "--lane-rule": mix(colors["lt1"], colors["accent1"], LABEL_RULE) if band
        else mix(colors["accent1"], colors["lt1"], STRONG),
    }
    fonts = fonts or {}
    root = ";".join(f"{k}:#{v}" for k, v in css_vars.items())
    root += f";--font-heading:{css_font_stack(fonts.get('major') or fonts.get('minor'))}"
    root += f";--font-body:{css_font_stack(fonts.get('minor') or fonts.get('major'))}"
    grid = [f'<div class="sl" style="--n:{n};--head:24px">', '<div class="sl-h"></div>']
    grid += [f'<div class="sl-h">{short(w)}</div>' for w in r.weeks]
    lanes = r.lanes()
    top = 2  # grid row of the current lane; explicit rows keep a multi-row lane label spanning its rows
    for k, (theme, rows) in enumerate(lanes):
        first = " first" if k == 0 else ""
        grid.append(f'<div class="sl-lane{first}" style="grid-row:{top} / span {len(rows)}">{e(theme)}</div>')
        for j, row in enumerate(rows):
            cls = ["sl-row"] + (["lane-top"] if j == 0 else []) + (["alt"] if k % 2 else [])
            cls += ["last"] if k == len(lanes) - 1 and j == len(rows) - 1 else []
            grid.append(f'<div class="{" ".join(cls)}" style="grid-row:{top + j};grid-column:2 / span {n}">')
            for m in row:
                a, b = r.span(m)
                bar = "bar est" if estimated(m) else "bar"
                grid.append(
                    f'<div class="{bar}" style="grid-column:{a + 1} / {b + 2}" title="{e(m["name"])}: {dates(m)}">'
                    f"<b>{e(m['name'])}</b><span>{dates(m)}</span></div>"
                )
            grid.append("</div>")
        top += len(rows)
    body_rows = sum(len(rows) for _, rows in lanes)
    grid.append(f'<div class="cols" style="grid-row:2 / span {body_rows}">' + "<i></i>" * n + "</div>")
    offset = r.today_offset()
    if offset is not None:
        grid.append(f'<div class="today" title="{short(r.as_of)}" '
                    f'style="left:calc(180px + (100% - 180px) * {offset:.4f})"><i>Today</i></div>')
    grid.append("</div>")
    legend = ['<div class="legend">']
    legend += [f'<span><s class="{"est" if s else ""}"></s>{LEGEND_LABEL[s]}</span>' for s in r.legend()]
    legend.append("</div>")
    extra = []
    if r.outside:
        extra.append("<h2>Outside this window</h2><ul>")
        extra += [f"<li>{e(m['name'])} ({e(m['theme'])}): {dates(m)}</li>" for m in r.outside]
        extra.append("</ul>")
    if r.unscheduled:
        extra.append("<h2>Unscheduled</h2><ul>")
        extra += [f"<li>{e(line)}</li>" for line in unscheduled_lines(r)]
        extra.append("</ul>")
    return (
        f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{e(r.title)}</title>'
        f"<style>:root{{{root}}}{CSS}</style></head><body class=\"{r.layout}\"><header><h1>{e(r.title)}</h1>"
        f'<div class="sub">{e(subtitle(r))}</div>{_logo_html(r, logo)}</header><main>'
        + "\n".join(grid + legend + extra)
        + "</main></body></html>\n"
    )
