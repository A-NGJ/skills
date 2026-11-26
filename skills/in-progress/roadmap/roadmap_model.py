"""Roadmap input data and shared timeline calculations."""

from __future__ import annotations

import datetime as dt
import sys

WEEK = dt.timedelta(weeks=1)
LAYOUTS = ("band", "plain")


class Roadmap:
    def __init__(self, data: dict):
        self.title = data.get("title", "Roadmap")
        self.as_of = _date(data.get("as_of") or dt.date.today().isoformat(), "as_of")
        window = data.get("window") or {}
        start = _date(window.get("start") or (self.as_of - 2 * WEEK).isoformat(), "window.start")
        self.start = start - dt.timedelta(days=start.weekday())  # weeks start on Monday
        self.weeks = [self.start + i * WEEK for i in range(int(window.get("weeks", 12)))]
        self.end = self.weeks[-1] + dt.timedelta(days=6)
        self.milestones = []
        for i, m in enumerate(data.get("milestones", [])):
            where = f"milestones[{i}]"
            for key in ("theme", "name", "start", "finish"):
                if not m.get(key):
                    sys.exit(f"{where}: missing {key}")
            ms = {
                "theme": m["theme"],
                "name": m["name"],
                "start": _date(m["start"], f"{where}.start"),
                "finish": _date(m["finish"], f"{where}.finish"),
                "start_estimated": bool(m.get("start_estimated")),
                "finish_estimated": bool(m.get("finish_estimated")),
            }
            if ms["finish"] < ms["start"]:
                sys.exit(f"{where}: finish is before start")
            self.milestones.append(ms)
        self.milestones.sort(key=lambda m: (m["start"], m["finish"]))
        self.unscheduled = data.get("unscheduled", [])
        self.themes = list(dict.fromkeys(m["theme"] for m in self.milestones))
        self.visible = [m for m in self.milestones if m["finish"] >= self.start and m["start"] <= self.end]
        self.outside = [m for m in self.milestones if m not in self.visible]
        self.layout = data.get("layout", "band")
        if self.layout not in LAYOUTS:
            sys.exit(f"layout: expected one of {', '.join(LAYOUTS)}, got {self.layout!r}")
        self.logo = data.get("logo")  # None: empty slot; False: nothing; str: image path

    def col(self, day: dt.date) -> int:
        """Index of the week column holding `day`, clamped to the window."""
        return min(max((day - self.start).days // 7, 0), len(self.weeks) - 1)

    def span(self, m) -> tuple[int, int]:
        return self.col(m["start"]), self.col(m["finish"])

    def rows(self, theme: str) -> list[list[dict]]:
        """Pack a theme's visible milestones into rows so overlapping ones stack."""
        rows: list[list[dict]] = []
        for m in (m for m in self.visible if m["theme"] == theme):
            for row in rows:
                if self.span(row[-1])[1] < self.span(m)[0]:
                    row.append(m)
                    break
            else:
                rows.append([m])
        return rows

    def lanes(self):
        return [(t, self.rows(t)) for t in self.themes if self.rows(t)]

    def today_offset(self) -> float | None:
        """Position of as_of across the window as a fraction, or None when outside it."""
        if not self.start <= self.as_of <= self.end:
            return None
        return (self.as_of - self.start).days / (7 * len(self.weeks))

    def has_estimates(self) -> bool:
        return any(estimated(m) for m in self.milestones)

    def legend(self) -> list[bool]:
        """Bar states drawn on the timeline, as `estimated` flags: estimated first, then firm."""
        states = {estimated(m) for m in self.visible}
        return [s for s in (True, False) if s in states]


def _date(value: str, where: str) -> dt.date:
    try:
        return dt.date.fromisoformat(value)
    except (TypeError, ValueError):
        sys.exit(f"{where}: expected YYYY-MM-DD, got {value!r}")


def short(day: dt.date) -> str:
    return f"{day.day} {day:%b}"


def dates(m) -> str:
    s = ("~" if m["start_estimated"] else "") + short(m["start"])
    f = ("~" if m["finish_estimated"] else "") + short(m["finish"])
    return f"{s} – {f}"


def estimated(m) -> bool:
    return m["start_estimated"] or m["finish_estimated"]


def as_of_line(r: Roadmap) -> str:
    return f"As of {short(r.as_of)} {r.as_of.year}. Weeks start on Monday. ~ marks an estimated date."


def subtitle(r: Roadmap) -> str:
    """Slide and HTML subtitle; bar styles are left to the legend."""
    parts = [f"As of {short(r.as_of)} {r.as_of.year}", "weeks start on Monday"]
    return " · ".join(parts + (["~ marks an estimated date"] if r.has_estimates() else []))


def unscheduled_lines(r: Roadmap) -> list[str]:
    return [f"{u.get('name', '?')}" + (f" ({u['theme']})" if u.get("theme") else "") for u in r.unscheduled]


LEGEND_LABEL = {True: "Estimated date", False: "Firm dates"}
LOGO_SLOT_TEXT = ("Logo", "(paste official file)")
