# /// script
# requires-python = ">=3.9"
# dependencies = ["python-pptx>=1.0"]
# ///
"""Render a roadmap data file into Markdown, HTML, and PowerPoint.

Usage:
  uv run render.py roadmap.json --out DIR [--format md,html,pptx] [--template corp.pptx] [--layout band|plain]
  uv run render.py --make-template out.pptx [--colors accent1=RRGGBB,dk1=RRGGBB,...] [--font "Typeface"]

--layout overrides the data file's "layout" key (default band). The PowerPoint render prints one
stderr line per lane label or bar whose text won't fit its box; the exit code stays 0.
--make-template writes a minimal 16:9 template: the given theme colour slots (dk1, lt1, dk2, lt2,
accent1..accent6) and theme typeface. Slots left out keep the python-pptx default theme.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from roadmap_model import LAYOUTS, Roadmap
from roadmap_powerpoint import make_template, render_pptx
from roadmap_text import render_html, render_md
from roadmap_theme import DEFAULT_THEME, SLOTS, theme_colors, theme_fonts


def parse_colors(spec: str) -> dict[str, str]:
    colors = {}
    for item in filter(None, (s.strip() for s in spec.split(","))):
        slot, _, value = item.partition("=")
        slot, value = slot.strip(), value.strip().lstrip("#").upper()
        if slot not in SLOTS:
            sys.exit(f"--colors: unknown slot {slot!r}; expected one of {', '.join(SLOTS)}")
        if not re.fullmatch(r"[0-9A-F]{6}", value):
            sys.exit(f"--colors: {slot} expects RRGGBB, got {value!r}")
        colors[slot] = value
    return colors


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("data", type=Path, nargs="?", help="roadmap data file (JSON)")
    ap.add_argument("--out", type=Path, help="output directory")
    ap.add_argument("--format", default="md", help="comma-separated: md, html, pptx (default md)")
    ap.add_argument("--template", type=Path, help="corporate .pptx whose masters and theme to use")
    ap.add_argument("--layout", choices=LAYOUTS, help="band or plain; overrides the data file's layout")
    ap.add_argument("--make-template", type=Path, metavar="OUT", help="write a minimal template and exit")
    ap.add_argument("--colors", default="", help="with --make-template: slot=RRGGBB,... (dk1, lt1, dk2, lt2, accent1..6)")
    ap.add_argument("--font", help="with --make-template: theme typeface for headings and body")
    args = ap.parse_args(argv)

    if args.make_template:
        make_template(args.make_template, parse_colors(args.colors), args.font)
        print(args.make_template)
        return 0
    if args.data is None or args.out is None:
        ap.error("data and --out are required unless --make-template is given")
    formats = [f.strip() for f in args.format.split(",") if f.strip()]
    unknown = set(formats) - {"md", "html", "pptx"}
    if unknown:
        ap.error(f"unknown format(s): {', '.join(sorted(unknown))}")
    r = Roadmap(json.loads(args.data.read_text()))
    if not r.milestones:
        sys.exit("no scheduled milestones; nothing to draw")
    if args.layout:
        r.layout = args.layout
    logo = None
    if isinstance(r.logo, str):
        logo = (args.data.parent / r.logo).resolve()
        if not logo.is_file():
            print(f"logo: {logo} not found; drawing the empty logo slot", file=sys.stderr)
    args.out.mkdir(parents=True, exist_ok=True)
    stem = args.data.stem
    written = []
    if "md" in formats:
        written.append(args.out / f"{stem}.md")
        written[-1].write_text(render_md(r))
    if "html" in formats:
        colors, fonts = DEFAULT_THEME, {}
        if args.template:
            from pptx import Presentation

            deck = Presentation(str(args.template))
            colors, fonts = theme_colors(deck), theme_fonts(deck)
        written.append(args.out / f"{stem}.html")
        written[-1].write_text(render_html(r, colors, logo, fonts))
    if "pptx" in formats:
        written.append(args.out / f"{stem}.pptx")
        for warning in render_pptx(r, written[-1], args.template, logo):
            print(f"overflow: {warning}", file=sys.stderr)
    for path in written:
        print(path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
