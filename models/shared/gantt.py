"""Build the Part 2 roadmap Gantt as matching draw.io, SVG and PNG exports.

Dates follow the Part 1 six-iteration roadmap and the locked Part 2 plan.
Grey marks are dated Git changes only; they do not imply elapsed work.
"""
from __future__ import annotations

from datetime import date, timedelta
from html import escape
from pathlib import Path
import xml.etree.ElementTree as ET

from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent
D0 = date(2026, 10, 17)
D1 = date(2026, 11, 30)
ROWS = [
    {"label": "I1 Persisted COD order", "type": "iteration", "start": date(2026, 10, 17), "end": date(2026, 10, 22), "actual": [date(2026, 10, 19), date(2026, 10, 20)]},
    {"label": "Part 1 packaging / eLearning", "type": "task", "start": date(2026, 10, 23), "end": date(2026, 10, 25), "milestones": [date(2026, 10, 25)], "actual": [date(2026, 10, 23)]},
    {"label": "Part 1 live presentation", "type": "milestone", "date": date(2026, 10, 26)},
    {"label": "I2 Hubs, capacity, kitchen board", "type": "iteration", "start": date(2026, 10, 27), "end": date(2026, 10, 31)},
    {"label": "P1 Report I and G1 draft", "type": "task", "start": date(2026, 10, 27), "end": date(2026, 10, 29)},
    {"label": "31/10 replan checkpoint", "type": "milestone", "date": date(2026, 10, 31)},
    {"label": "I3 Full ordering, delivery, menus", "type": "iteration", "start": date(2026, 11, 1), "end": date(2026, 11, 5)},
    {"label": "I4 Reports, integration, Figma", "type": "iteration", "start": date(2026, 11, 6), "end": date(2026, 11, 10)},
    {"label": "P3 design / P4 tests / P5 integration / P6 deploy", "type": "task", "start": date(2026, 11, 3), "end": date(2026, 11, 10)},
    {"label": "I5 Final models, regression, report", "type": "iteration", "start": date(2026, 11, 11), "end": date(2026, 11, 15)},
    {"label": "12/11 feature freeze", "type": "milestone", "date": date(2026, 11, 12)},
    {"label": "13/11 buffer: real fixes and retest", "type": "task", "start": date(2026, 11, 13), "end": date(2026, 11, 13)},
    {"label": "14/11 PDF and package QA", "type": "task", "start": date(2026, 11, 14), "end": date(2026, 11, 14)},
    {"label": "15/11 Part 2 target submission", "type": "milestone", "date": date(2026, 11, 15)},
    {"label": "16/11 Part 2 presentation", "type": "milestone", "date": date(2026, 11, 16)},
    {"label": "I6 Feedback fixes and Part 3", "type": "iteration", "start": date(2026, 11, 17), "end": date(2026, 11, 29)},
    {"label": "29/11 Part 3 submission", "type": "milestone", "date": date(2026, 11, 29)},
    {"label": "30/11 Part 3 presentation", "type": "milestone", "date": date(2026, 11, 30)},
]

BLUE = "#004387"
PALE = "#E7F0F6"
MID = "#7FA7CF"
RED = "#C0392B"
GRID = "#C8D6E4"
WEEKEND = "#F3F6F8"
ACTUAL = "#52616F"
TEXT = "#202B36"
MUTED = "#52616F"
WHITE = "#FFFFFF"

WIDTH = 2300
HEADER = 128
ROW_H = 72
FOOTER = 120
HEIGHT = HEADER + ROW_H * len(ROWS) + FOOTER
LABEL_W = 630
DATE_W = 250
X0 = LABEL_W + DATE_W
X1 = WIDTH - 60
ND = (D1 - D0).days + 1
DAY_W = (X1 - X0) / ND


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    path = Path(r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf")
    return ImageFont.truetype(str(path), size)


def wrap_text(draw: ImageDraw.ImageDraw, value: str, use_font: ImageFont.FreeTypeFont, max_width: float) -> list[str]:
    lines: list[str] = []
    for paragraph in value.split("\n"):
        words = paragraph.split()
        if not words:
            lines.append("")
            continue
        current = words[0]
        for word in words[1:]:
            candidate = current + " " + word
            if draw.textlength(candidate, font=use_font) <= max_width:
                current = candidate
            else:
                lines.append(current)
                current = word
        lines.append(current)
    return lines


def day_x(day: date) -> float:
    return X0 + (day - D0).days * DAY_W


def date_label(row: dict) -> str:
    if row["type"] == "milestone":
        return row["date"].strftime("%d/%m")
    start, end = row["start"], row["end"]
    if start == end:
        return start.strftime("%d/%m")
    return f"{start:%d/%m}-{end:%d/%m}"


def iter_days(start: date, end: date):
    current = start
    while current <= end:
        yield current
        current += timedelta(days=1)


def draw_png() -> None:
    img = Image.new("RGB", (WIDTH, HEIGHT), WHITE)
    draw = ImageDraw.Draw(img)
    draw.rectangle((0, 0, WIDTH, HEADER), fill=BLUE)
    draw.text((14, 8), "SaigonBite Part 2 Roadmap", font=font(36, True), fill=WHITE)

    for label, start, end in (
        ("October 2026", D0, date(2026, 10, 31)),
        ("November 2026", date(2026, 11, 1), D1),
    ):
        xa, xb = day_x(start), day_x(end + timedelta(days=1))
        use_font = font(34, True)
        draw.text(((xa + xb - draw.textlength(label, font=use_font)) / 2, 8), label, font=use_font, fill=WHITE)

    draw.text((14, 69), "Iteration / task", font=font(34, True), fill=WHITE)
    draw.text((LABEL_W + 10, 69), "Dates", font=font(34, True), fill=WHITE)
    for day in iter_days(D0, D1):
        if day.weekday() == 0:
            x = day_x(day)
            draw.line((x, 54, x, HEADER), fill=WHITE, width=2)
            draw.text((x + 3, 77), day.strftime("%d/%m"), font=font(32, True), fill=WHITE)

    body_y = HEADER
    for index, row in enumerate(ROWS):
        y = body_y + index * ROW_H
        row_fill = PALE if index % 2 else WHITE
        draw.rectangle((0, y, WIDTH, y + ROW_H), fill=row_fill)
        for day in iter_days(D0, D1):
            if day.weekday() >= 5:
                x = day_x(day)
                draw.rectangle((x, y, x + DAY_W, y + ROW_H), fill="#D6E2EE" if index % 2 else WEEKEND)
        draw.line((0, y + ROW_H, WIDTH, y + ROW_H), fill=GRID, width=1)

        row_font = font(34, row["type"] == "iteration")
        lines = wrap_text(draw, row["label"], row_font, LABEL_W - 26)
        line_h = 35
        text_height = line_h * len(lines)
        text_y = y + (ROW_H - text_height) / 2
        for line_index, line in enumerate(lines):
            draw.text((14, text_y + line_index * line_h), line, font=row_font, fill=TEXT)
        draw.text((LABEL_W + 10, y + (ROW_H - 40) / 2), date_label(row), font=font(34), fill=TEXT)

        for day in row.get("actual", []):
            center = day_x(day) + DAY_W / 2
            draw.rectangle((center - DAY_W * 0.34, y + 57, center + DAY_W * 0.34, y + 65), fill=ACTUAL)

        if row["type"] in ("iteration", "task"):
            xa = day_x(row["start"]) + 1
            xb = day_x(row["end"] + timedelta(days=1)) - 1
            color = BLUE if row["type"] == "iteration" else MID
            draw.rounded_rectangle((xa, y + 12, xb, y + 47), radius=8, fill=color)

        milestones = [row["date"]] if row["type"] == "milestone" else row.get("milestones", [])
        for milestone in milestones:
            cx = day_x(milestone) + DAY_W / 2
            cy = y + ROW_H / 2
            size = 21
            draw.polygon(((cx, cy - size), (cx + size, cy), (cx, cy + size), (cx - size, cy)), fill=RED, outline=WHITE)

    for day in (date(2026, 10, 26), date(2026, 11, 16), date(2026, 11, 30)):
        x = day_x(day) + DAY_W / 2
        for y in range(HEADER, HEADER + ROW_H * len(ROWS), 18):
            draw.line((x, y, x, y + 9), fill=RED, width=3)

    yb = HEADER + ROW_H * len(ROWS)
    draw.line((X0, HEADER, X0, yb), fill=GRID, width=2)
    draw.line((0, yb, WIDTH, yb), fill=BLUE, width=3)
    footer_lines = (
        "Blue bar = planned iteration; light blue = planned task; red diamond = planned milestone; grey tick = dated Git change.",
        "Grey ticks mark commit dates only, not elapsed work. Grey columns = weekends; dashed lines = presentation dates.",
        "Status cut-off: 23/10/2026. Author: 722I0004 · AI-assisted (Codex).",
    )
    for i, line in enumerate(footer_lines):
        draw.text((14, yb + 8 + i * 35), line, font=font(32, i == 2), fill=TEXT if i < 2 else MUTED)
    img.save(OUT / "gantt.png", dpi=(300, 300), optimize=True)


def svg_text(parts: list[str], x: float, y: float, value: str, size: int, color: str = TEXT,
             bold: bool = False, anchor: str = "start", max_width: float | None = None) -> None:
    use_font = font(size, bold)
    dummy = Image.new("RGB", (1, 1))
    lines = wrap_text(ImageDraw.Draw(dummy), value, use_font, max_width) if max_width else value.split("\n")
    weight = "700" if bold else "400"
    parts.append(
        f'<text x="{x:.2f}" y="{y:.2f}" fill="{color}" font-family="Arial, sans-serif" '
        f'font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" dominant-baseline="hanging">'
    )
    for i, line in enumerate(lines):
        dy = 0 if i == 0 else 35
        parts.append(f'<tspan x="{x:.2f}" dy="{dy}">{escape(line)}</tspan>')
    parts.append("</text>")


def svg_rect(parts: list[str], x: float, y: float, w: float, h: float, fill: str,
             stroke: str = "none", stroke_width: int = 0, radius: int = 0) -> None:
    parts.append(
        f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" '
        f'rx="{radius}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}"/>'
    )


def draw_svg() -> None:
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">']
    svg_rect(parts, 0, 0, WIDTH, HEADER, BLUE)
    svg_text(parts, 14, 8, "SaigonBite Part 2 Roadmap", 36, WHITE, True)
    for label, start, end in (
        ("October 2026", D0, date(2026, 10, 31)),
        ("November 2026", date(2026, 11, 1), D1),
    ):
        xa, xb = day_x(start), day_x(end + timedelta(days=1))
        svg_text(parts, (xa + xb) / 2, 8, label, 34, WHITE, True, anchor="middle")
    svg_text(parts, 14, 69, "Iteration / task", 34, WHITE, True)
    svg_text(parts, LABEL_W + 10, 69, "Dates", 34, WHITE, True)
    for day in iter_days(D0, D1):
        if day.weekday() == 0:
            x = day_x(day)
            parts.append(f'<line x1="{x:.2f}" y1="54" x2="{x:.2f}" y2="{HEADER}" stroke="{WHITE}" stroke-width="2"/>')
            svg_text(parts, x + 3, 77, day.strftime("%d/%m"), 32, WHITE, True)

    body_y = HEADER
    for index, row in enumerate(ROWS):
        y = body_y + index * ROW_H
        svg_rect(parts, 0, y, WIDTH, ROW_H, PALE if index % 2 else WHITE)
        for day in iter_days(D0, D1):
            if day.weekday() >= 5:
                x = day_x(day)
                svg_rect(parts, x, y, DAY_W, ROW_H, "#D6E2EE" if index % 2 else WEEKEND)
        parts.append(f'<line x1="0" y1="{y + ROW_H}" x2="{WIDTH}" y2="{y + ROW_H}" stroke="{GRID}" stroke-width="1"/>')
        lines = wrap_text(ImageDraw.Draw(Image.new("RGB", (1, 1))), row["label"], font(34, row["type"] == "iteration"), LABEL_W - 26)
        text_y = y + (ROW_H - 35 * len(lines)) / 2
        svg_text(parts, 14, text_y, row["label"], 34, TEXT, row["type"] == "iteration", max_width=LABEL_W - 26)
        svg_text(parts, LABEL_W + 10, y + (ROW_H - 40) / 2, date_label(row), 34, TEXT)
        for day in row.get("actual", []):
            center = day_x(day) + DAY_W / 2
            svg_rect(parts, center - DAY_W * 0.34, y + 57, DAY_W * 0.68, 8, ACTUAL)
        if row["type"] in ("iteration", "task"):
            xa = day_x(row["start"]) + 1
            xb = day_x(row["end"] + timedelta(days=1)) - 1
            svg_rect(parts, xa, y + 12, xb - xa, 35, BLUE if row["type"] == "iteration" else MID, radius=8)
        milestones = [row["date"]] if row["type"] == "milestone" else row.get("milestones", [])
        for milestone in milestones:
            cx, cy, size = day_x(milestone) + DAY_W / 2, y + ROW_H / 2, 21
            points = f"{cx:.2f},{cy-size:.2f} {cx+size:.2f},{cy:.2f} {cx:.2f},{cy+size:.2f} {cx-size:.2f},{cy:.2f}"
            parts.append(f'<polygon points="{points}" fill="{RED}" stroke="{WHITE}" stroke-width="2"/>')

    for day in (date(2026, 10, 26), date(2026, 11, 16), date(2026, 11, 30)):
        x = day_x(day) + DAY_W / 2
        for y in range(HEADER, HEADER + ROW_H * len(ROWS), 18):
            parts.append(f'<line x1="{x:.2f}" y1="{y}" x2="{x:.2f}" y2="{y+9}" stroke="{RED}" stroke-width="3"/>')
    yb = HEADER + ROW_H * len(ROWS)
    parts.append(f'<line x1="{X0}" y1="{HEADER}" x2="{X0}" y2="{yb}" stroke="{GRID}" stroke-width="2"/>')
    parts.append(f'<line x1="0" y1="{yb}" x2="{WIDTH}" y2="{yb}" stroke="{BLUE}" stroke-width="3"/>')
    footer_lines = (
        "Blue bar = planned iteration; light blue = planned task; red diamond = planned milestone; grey tick = dated Git change.",
        "Grey ticks mark commit dates only, not elapsed work. Grey columns = weekends; dashed lines = presentation dates.",
        "Status cut-off: 23/10/2026. Author: 722I0004 · AI-assisted (Codex).",
    )
    for i, line in enumerate(footer_lines):
        svg_text(parts, 14, yb + 8 + i * 35, line, 32, TEXT if i < 2 else MUTED, i == 2)
    parts.append("</svg>")
    (OUT / "gantt.svg").write_text("\n".join(parts), encoding="utf-8")


def add_drawio_rect(root: ET.Element, cell_id: str, x: float, y: float, w: float, h: float,
                    fill: str, rounded: int = 0, stroke: str = "none", stroke_width: int = 0,
                    shape: str = "") -> None:
    prefix = (shape + ";") if shape else ""
    style = f"{prefix}rounded={rounded};whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};strokeWidth={stroke_width};"
    cell = ET.SubElement(root, "mxCell", {"id": cell_id, "value": "", "style": style, "vertex": "1", "parent": "1"})
    ET.SubElement(cell, "mxGeometry", {"x": f"{x:.2f}", "y": f"{y:.2f}", "width": f"{w:.2f}", "height": f"{h:.2f}", "as": "geometry"})


def add_drawio_text(root: ET.Element, cell_id: str, x: float, y: float, w: float, h: float,
                    value: str, size: int, color: str = TEXT, bold: bool = False,
                    align: str = "left") -> None:
    style = (
        "text;html=1;strokeColor=none;fillColor=none;whiteSpace=wrap;"
        f"align={align};verticalAlign=middle;spacing=0;fontFamily=Arial;fontSize={size};"
        f"fontColor={color};fontStyle={1 if bold else 0};"
    )
    cell = ET.SubElement(root, "mxCell", {"id": cell_id, "value": escape(value).replace("\n", "<br/>"),
                                           "style": style, "vertex": "1", "parent": "1"})
    ET.SubElement(cell, "mxGeometry", {"x": f"{x:.2f}", "y": f"{y:.2f}", "width": f"{w:.2f}", "height": f"{h:.2f}", "as": "geometry"})


def draw_drawio() -> None:
    mxfile = ET.Element("mxfile", {"host": "app.diagrams.net", "version": "24.7.17", "type": "device"})
    diagram = ET.SubElement(mxfile, "diagram", {"id": "saigonbite-roadmap", "name": "Part 2 Roadmap"})
    model = ET.SubElement(diagram, "mxGraphModel", {"dx": str(WIDTH), "dy": str(HEIGHT), "grid": "1", "gridSize": "10",
        "guides": "1", "tooltips": "1", "connect": "1", "arrows": "1", "fold": "1", "page": "1", "pageScale": "1",
        "pageWidth": str(WIDTH), "pageHeight": str(HEIGHT), "math": "0", "shadow": "0"})
    root = ET.SubElement(model, "root")
    ET.SubElement(root, "mxCell", {"id": "0"})
    ET.SubElement(root, "mxCell", {"id": "1", "parent": "0"})
    add_drawio_rect(root, "header", 0, 0, WIDTH, HEADER, BLUE)
    add_drawio_text(root, "title", 14, 5, 630, 48, "SaigonBite Part 2 Roadmap", 36, WHITE, True)
    for label, start, end in (
        ("October 2026", D0, date(2026, 10, 31)),
        ("November 2026", date(2026, 11, 1), D1),
    ):
        xa, xb = day_x(start), day_x(end + timedelta(days=1))
        add_drawio_text(root, "month_" + label.split()[0].lower(), xa, 3, xb - xa, 44, label, 34, WHITE, True, "center")
    add_drawio_text(root, "column_label", 14, 60, LABEL_W - 24, 55, "Iteration / task", 34, WHITE, True)
    add_drawio_text(root, "column_dates", LABEL_W + 10, 60, DATE_W - 12, 55, "Dates", 34, WHITE, True)
    for day in iter_days(D0, D1):
        if day.weekday() == 0:
            x = day_x(day)
            add_drawio_rect(root, f"week_tick_{day:%m%d}", x, 54, 2, HEADER - 54, WHITE)
            add_drawio_text(root, f"week_label_{day:%m%d}", x + 3, 75, 100, 40, day.strftime("%d/%m"), 32, WHITE, True)

    for index, row in enumerate(ROWS):
        y = HEADER + index * ROW_H
        add_drawio_rect(root, f"row_{index}", 0, y, WIDTH, ROW_H, PALE if index % 2 else WHITE)
        for day in iter_days(D0, D1):
            if day.weekday() >= 5:
                x = day_x(day)
                add_drawio_rect(root, f"weekend_{index}_{day:%m%d}", x, y, DAY_W, ROW_H, "#D6E2EE" if index % 2 else WEEKEND)
        add_drawio_rect(root, f"row_line_{index}", 0, y + ROW_H - 1, WIDTH, 1, GRID)
        add_drawio_text(root, f"row_label_{index}", 14, y + 3, LABEL_W - 26, ROW_H - 6, row["label"], 34, TEXT, row["type"] == "iteration")
        add_drawio_text(root, f"row_dates_{index}", LABEL_W + 10, y + 3, DATE_W - 12, ROW_H - 6, date_label(row), 34, TEXT)
        for j, day in enumerate(row.get("actual", [])):
            center = day_x(day) + DAY_W / 2
            add_drawio_rect(root, f"actual_{index}_{j}", center - DAY_W * 0.34, y + 57, DAY_W * 0.68, 8, ACTUAL)
        if row["type"] in ("iteration", "task"):
            xa = day_x(row["start"]) + 1
            xb = day_x(row["end"] + timedelta(days=1)) - 1
            add_drawio_rect(root, f"planned_{index}", xa, y + 12, xb - xa, 35,
                            BLUE if row["type"] == "iteration" else MID, rounded=1)
        milestones = [row["date"]] if row["type"] == "milestone" else row.get("milestones", [])
        for j, milestone in enumerate(milestones):
            cx, cy, size = day_x(milestone) + DAY_W / 2, y + ROW_H / 2, 21
            add_drawio_rect(root, f"milestone_{index}_{j}", cx - size, cy - size, size * 2, size * 2,
                            RED, stroke=WHITE, stroke_width=2, shape="rhombus")

    for index, day in enumerate((date(2026, 10, 26), date(2026, 11, 16), date(2026, 11, 30))):
        x = day_x(day) + DAY_W / 2
        for j, y in enumerate(range(HEADER, HEADER + ROW_H * len(ROWS), 18)):
            add_drawio_rect(root, f"presentation_{index}_{j}", x, y, 3, 9, RED)
    yb = HEADER + ROW_H * len(ROWS)
    add_drawio_rect(root, "timeline_boundary", X0, HEADER, 2, ROW_H * len(ROWS), GRID)
    add_drawio_rect(root, "footer_top", 0, yb, WIDTH, 3, BLUE)
    footer_lines = (
        "Blue bar = planned iteration; light blue = planned task; red diamond = planned milestone; grey tick = dated Git change.",
        "Grey ticks mark commit dates only, not elapsed work. Grey columns = weekends; dashed lines = presentation dates.",
        "Status cut-off: 23/10/2026. Author: 722I0004 · AI-assisted (Codex).",
    )
    for i, line in enumerate(footer_lines):
        add_drawio_text(root, f"footer_{i}", 14, yb + 5 + i * 35, WIDTH - 28, 34, line, 32, TEXT if i < 2 else MUTED, i == 2)
    ET.indent(mxfile, space="  ")
    (OUT / "gantt.drawio").write_text(ET.tostring(mxfile, encoding="unicode"), encoding="utf-8")


if __name__ == "__main__":
    draw_png()
    draw_svg()
    draw_drawio()
    for filename in ("gantt.py", "gantt.drawio", "gantt.svg", "gantt.png"):
        path = OUT / filename
        print(f"wrote {filename} ({path.stat().st_size} bytes)")
    print(f"canvas={WIDTH}x{HEIGHT}; rows={len(ROWS)}; date_range={D0:%d/%m/%Y}-{D1:%d/%m/%Y}; A4 landscape placement width=229mm; minimum text=32px")
