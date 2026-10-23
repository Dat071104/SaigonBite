"""Build the shared stakeholder map in draw.io, SVG and PNG from one layout.

Layout starts with the balanced-diagrams skill's layered layout functions;
the tall OFDH boundary is then expanded over the three aligned stakeholder
bands. All exports share the resulting geometry.
"""
from __future__ import annotations

from collections import deque
from html import escape as html_escape
from pathlib import Path
from xml.sax.saxutils import escape as xml_escape
import math
import xml.etree.ElementTree as ET

from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent
BLUE = "#004387"
HEADING = "#185695"
PALE = "#E7F0F6"
PALE2 = "#F3F6F8"
STROKE = "#6C8EBF"
GRID = "#C8D6E4"
TEXT = "#202B36"
MUTED = "#52616F"
WHITE = "#FFFFFF"


def compute_ranks(node_ids, edges):
    """Skill helper: longest-path layers, with deterministic cycle fallback."""
    adj = {n: [] for n in node_ids}
    indeg = {n: 0 for n in node_ids}
    for edge in edges:
        adj[edge["from"]].append(edge["to"])
        indeg[edge["to"]] += 1
    rank = {n: 0 for n in node_ids}
    remaining = dict(indeg)
    queue = deque(n for n in node_ids if remaining[n] == 0)
    order = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for target in adj[node]:
            rank[target] = max(rank[target], rank[node] + 1)
            remaining[target] -= 1
            if remaining[target] == 0:
                queue.append(target)
    if len(order) < len(node_ids):
        return {n: i for i, n in enumerate(node_ids)}, list(node_ids)
    return rank, order


def layered_positions(nodes, rank, ratio_target, pitch_x, pitch_y):
    """Skill helper: choose TD/LR layered layout closest to the target ratio."""
    layers = {}
    for node_id, layer in rank.items():
        layers.setdefault(layer, []).append(node_id)
    ordered = sorted(layers)
    layer_count = len(ordered)
    widest = max(len(layers[layer]) for layer in ordered)
    ratio_td = widest * pitch_x / (layer_count * pitch_y)
    ratio_lr = layer_count * pitch_x / (widest * pitch_y)
    score = lambda value: abs(math.log(value) - math.log(ratio_target))
    direction = "TD" if score(ratio_td) <= score(ratio_lr) else "LR"
    achieved = ratio_td if direction == "TD" else ratio_lr
    positions = {}
    if direction == "TD":
        for layer in ordered:
            row = layers[layer]
            offset = (widest - len(row)) * pitch_x / 2
            for index, node_id in enumerate(row):
                positions[node_id] = (offset + index * pitch_x, layer * pitch_y)
    else:
        for layer in ordered:
            column = layers[layer]
            offset = (widest - len(column)) * pitch_y / 2
            for index, node_id in enumerate(column):
                positions[node_id] = (layer * pitch_x, offset + index * pitch_y)
    return positions, achieved, direction


def font(size, bold=False):
    path = Path(r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf")
    return ImageFont.truetype(str(path), size)


def wrap_lines(draw, value, use_font, max_width):
    lines = []
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


def add_text_svg(parts, x, y, lines, size, color=TEXT, bold=False, line_height=None):
    weight = "700" if bold else "400"
    line_height = line_height or int(size * 1.25)
    parts.append(
        f'<text x="{x}" y="{y}" fill="{color}" font-family="Arial, sans-serif" '
        f'font-size="{size}" font-weight="{weight}" dominant-baseline="hanging">'
    )
    for index, line in enumerate(lines):
        dy = 0 if index == 0 else line_height
        parts.append(f'<tspan x="{x}" dy="{dy}">{html_escape(line)}</tspan>')
    parts.append("</text>")


def add_drawio_text(root, cell_id, x, y, w, h, lines, size, bold=False, color=TEXT):
    value = "<div>" + "<br/>".join(html_escape(line) for line in lines) + "</div>"
    style = (
        "text;html=1;strokeColor=none;fillColor=none;whiteSpace=wrap;"
        f"align=left;verticalAlign=top;spacing=0;fontFamily=Arial;fontSize={size};"
        f"fontColor={color};fontStyle={1 if bold else 0};"
    )
    cell = ET.SubElement(root, "mxCell", {"id": cell_id, "value": value, "style": style,
                                            "vertex": "1", "parent": "1"})
    ET.SubElement(cell, "mxGeometry", {"x": str(x), "y": str(y), "width": str(w),
                                        "height": str(h), "as": "geometry"})


def add_rect_svg(parts, x, y, w, h, fill, stroke=STROKE, radius=18, stroke_width=3):
    parts.append(
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}"/>'
    )


def add_rect_drawio(root, cell_id, x, y, w, h, fill, stroke=STROKE, rounded=True, width=2):
    style = (
        f"rounded={1 if rounded else 0};whiteSpace=wrap;html=1;fillColor={fill};"
        f"strokeColor={stroke};strokeWidth={width};"
    )
    cell = ET.SubElement(root, "mxCell", {"id": cell_id, "value": "", "style": style,
                                            "vertex": "1", "parent": "1"})
    ET.SubElement(cell, "mxGeometry", {"x": str(x), "y": str(y), "width": str(w),
                                        "height": str(h), "as": "geometry"})


def add_edge_svg(parts, points, label, label_x, label_y):
    path = "M " + " L ".join(f"{x} {y}" for x, y in points)
    parts.append(f'<path d="{path}" fill="none" stroke="{HEADING}" stroke-width="4" marker-end="url(#arrow)"/>')



def add_edge_drawio(root, cell_id, source, target, points, entry_y):
    style = (
        "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;html=1;"
        f"strokeColor={HEADING};strokeWidth=2;endArrow=block;endFill=1;"
        f"exitX=1;exitY=0.5;entryX=0;entryY={entry_y:.4f};"
    )
    edge = ET.SubElement(root, "mxCell", {"id": cell_id, "value": "", "style": style,
                                            "edge": "1", "parent": "1", "source": source,
                                            "target": target})
    geometry = ET.SubElement(edge, "mxGeometry", {"relative": "1", "as": "geometry"})
    array = ET.SubElement(geometry, "Array", {"as": "points"})
    for x, y in points:
        ET.SubElement(array, "mxPoint", {"x": str(x), "y": str(y)})


def main():
    # The skill helper places these three stakeholder bands as one rank and the
    # OFDH boundary as the next. Expand that boundary vertically to fit its five
    # capabilities while keeping the helper's balanced LR columns.
    nodes = ["operations", "admin_insight", "external", "ofd_platform"]
    edges = [{"from": n, "to": "ofd_platform"} for n in nodes[:-1]]
    rank, _ = compute_ranks(nodes, edges)
    positions, achieved, direction = layered_positions(
        nodes, rank, ratio_target=1.35, pitch_x=780, pitch_y=340
    )
    if direction != "LR":
        raise RuntimeError(f"Expected balanced LR layout, got {direction} ({achieved:.2f})")
    ox = 50
    oy = 100
    bands = {
        "operations": (ox + positions["operations"][0], oy + positions["operations"][1], 600, 280),
        "admin_insight": (ox + positions["admin_insight"][0], oy + positions["admin_insight"][1], 600, 280),
        "external": (ox + positions["external"][0], oy + positions["external"][1], 600, 280),
    }
    system = (ox + positions["ofd_platform"][0], oy, 580, 960)
    page_w, page_h = 1460, 1160
    img = Image.new("RGB", (page_w, page_h), WHITE)
    draw = ImageDraw.Draw(img)
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{page_w}" height="{page_h}" viewBox="0 0 {page_w} {page_h}">',
           '<defs><marker id="arrow" markerWidth="12" markerHeight="10" refX="10" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#185695"/></marker></defs>']
    mxfile = ET.Element("mxfile", {"host": "app.diagrams.net", "version": "24.7.17", "type": "device"})
    diagram = ET.SubElement(mxfile, "diagram", {"id": "stakeholder-map", "name": "Stakeholders"})
    model = ET.SubElement(diagram, "mxGraphModel", {"dx": str(page_w), "dy": str(page_h), "grid": "1",
        "gridSize": "10", "guides": "1", "tooltips": "1", "connect": "1", "arrows": "1",
        "fold": "1", "page": "1", "pageScale": "1", "pageWidth": str(page_w),
        "pageHeight": str(page_h), "math": "0", "shadow": "0"})
    root = ET.SubElement(model, "root")
    ET.SubElement(root, "mxCell", {"id": "0"})
    ET.SubElement(root, "mxCell", {"id": "1", "parent": "0"})

    # Page title and framing note.
    draw.text((50, 22), "SaigonBite client stakeholders", font=font(42, True), fill=BLUE)
    draw.text((50, 75), "Grouped by OFDH interaction; formal reporting lines are not assumed.", font=font(28), fill=MUTED)
    add_text_svg(svg, 50, 22, ["SaigonBite client stakeholders"], 42, color=BLUE, bold=True)
    add_text_svg(svg, 50, 75, ["Grouped by OFDH interaction; formal reporting lines are not assumed."], 28, color=MUTED)

    # Three stakeholder group cards, positioned by the skill layout helper.
    group_data = {
        "operations": ("Operations", [
            "Owner / management — oversight",
            "Hub managers — capacity",
            "Kitchen staff — orders, prep, availability",
            "Shippers — pickup, cash, delivery outcome",
        ]),
        "admin_insight": ("Administration and insight", [
            "Administrators — hubs, catalogue, vouchers, accounts and archive",
            "Managers / analysts — sales, workload and delivery reports",
        ]),
        "external": ("External participants", [
            "Local customers — quote, order, payment and tracking",
            "Tourist customers — registration, address and payment choice",
            "External payment provider — context only; this release uses a simulator",
        ]),
    }
    for group_id, (title, items) in group_data.items():
        x, y, w, h = bands[group_id]
        draw.rounded_rectangle((x, y, x + w, y + h), radius=18, fill=PALE, outline=STROKE, width=3)
        add_rect_svg(svg, x, y, w, h, PALE)
        add_rect_drawio(root, group_id, x, y, w, h, PALE, STROKE, True, 2)
        draw.text((x + 24, y + 18), title, font=font(34, True), fill=HEADING)
        add_text_svg(svg, x + 24, y + 18, [title], 34, color=HEADING, bold=True)
        add_drawio_text(root, group_id + "_title", x + 24, y + 18, w - 48, 44, [title], 34, True, HEADING)
        body_font = font(28)
        lines = []
        for item in items:
            wrapped = wrap_lines(draw, "• " + item, body_font, w - 56)
            lines.extend(wrapped)
        line_y = y + 70
        line_height = 34
        for line in lines:
            draw.text((x + 26, line_y), line, font=body_font, fill=TEXT)
            add_text_svg(svg, x + 26, line_y, [line], 28, color=TEXT)
            line_y += line_height
        add_drawio_text(root, group_id + "_body", x + 26, y + 68, w - 52, h - 80, lines, 28, False, TEXT)

    # One system boundary with five matching interaction areas.
    sx, sy, sw, sh = system
    draw.rounded_rectangle((sx, sy, sx + sw, sy + sh), radius=20, fill="#FFFFFF", outline=BLUE, width=5)
    add_rect_svg(svg, sx, sy, sw, sh, WHITE, BLUE, 20, 5)
    add_rect_drawio(root, "ofd_platform", sx, sy, sw, sh, WHITE, BLUE, True, 4)
    draw.text((sx + 28, sy + 22), "SaigonBite OFDH", font=font(42, True), fill=BLUE)
    draw.text((sx + 28, sy + 74), "Shared order and operating records", font=font(28), fill=MUTED)
    add_text_svg(svg, sx + 28, sy + 22, ["SaigonBite OFDH"], 42, color=BLUE, bold=True)
    add_text_svg(svg, sx + 28, sy + 74, ["Shared order and operating records"], 28, color=MUTED)
    add_drawio_text(root, "ofd_title", sx + 28, sy + 22, sw - 56, 50, ["SaigonBite OFDH"], 42, True, BLUE)
    add_drawio_text(root, "ofd_subtitle", sx + 28, sy + 73, sw - 56, 38, ["Shared order and operating records"], 28, False, MUTED)

    services = [
        ("Customer journey", "UC-01 · SUC-02–04 — quote, pay, track / receipt, cancel"),
        ("Kitchen and delivery", "UC-05 · SUC-05–06 — confirm / reject / replace, prepare / ready, availability"),
        ("Shipper delivery", "UC-02 — pick up ready orders; record delivery, COD cash or failure"),
        ("Administration", "UC-03 / UC-06 · SUC-01 / SUC-07–09 — hubs, catalogue, access, vouchers, accounts, archive"),
        ("Management reports", "UC-04 — sales, workload and delivery performance"),
    ]
    service_y = [sy + 120 + i * 150 for i in range(5)]
    card_x, card_w = sx + 24, sw - 48
    for i, (title, body) in enumerate(services):
        x, y = card_x, service_y[i]
        card_h = 166 if i == 3 else 132
        if i == 4:
            y += 34
        draw.rounded_rectangle((x, y, x + card_w, y + card_h), radius=12, fill=PALE2, outline=GRID, width=2)
        add_rect_svg(svg, x, y, card_w, card_h, PALE2, GRID, 12, 2)
        add_rect_drawio(root, f"service_{i+1}", x, y, card_w, card_h, PALE2, GRID, True, 1)
        draw.text((x + 18, y + 12), title, font=font(31, True), fill=HEADING)
        title_lines = [title]
        add_text_svg(svg, x + 18, y + 12, title_lines, 31, color=HEADING, bold=True)
        add_drawio_text(root, f"service_{i+1}_title", x + 18, y + 12, card_w - 36, 38, title_lines, 31, True, HEADING)
        body_lines = wrap_lines(draw, body, font(27), card_w - 38)
        for line_index, line in enumerate(body_lines):
            yy = y + 55 + line_index * 32
            draw.text((x + 19, yy), line, font=font(27), fill=TEXT)
            add_text_svg(svg, x + 19, yy, [line], 27, color=TEXT)
        add_drawio_text(root, f"service_{i+1}_body", x + 19, y + 54, card_w - 38,
                        card_h - 58, body_lines, 27, False, TEXT)

    # Interaction links route in the gap between role groups and the system.
    op = bands["operations"]
    ad = bands["admin_insight"]
    ex = bands["external"]
    edges = [
        ("operations", "operations_link", [(op[0]+op[2], op[1]+op[3]//2), (710, op[1]+op[3]//2), (710, sy+405), (sx, sy+405)], "operate", 585, op[1]+op[3]//2-35, (sy+405-sy)/sh),
        ("admin_insight", "admin_link", [(ad[0]+ad[2], ad[1]+ad[3]//2), (750, ad[1]+ad[3]//2), (750, sy+705), (sx, sy+705)], "administer / review", 584, ad[1]+ad[3]//2-35, (sy+705-sy)/sh),
        ("external", "external_link", [(ex[0]+ex[2], ex[1]+ex[3]//2), (790, ex[1]+ex[3]//2), (790, sy+205), (sx, sy+205)], "order / payment", 584, ex[1]+ex[3]//2-35, (sy+205-sy)/sh),
    ]
    for source_id, edge_id, points, label, lx, ly, entry_y in edges:
        for start, end in zip(points, points[1:]):
            draw.line((start, end), fill=HEADING, width=4)
        x1, y1 = points[-2]
        x2, y2 = points[-1]
        if x2 != x1:
            arrow_dir = 1 if x2 > x1 else -1
            draw.polygon([(x2, y2), (x2 - 16*arrow_dir, y2 - 9), (x2 - 16*arrow_dir, y2 + 9)], fill=HEADING)
        add_edge_svg(svg, points, label, lx, ly)
        add_edge_drawio(root, edge_id, source_id, "ofd_platform", points[1:-1], entry_y)


    credit = "Author: 722I0004 · AI-assisted (Codex)"
    draw.text((50, 1092), credit, font=font(26, True), fill=MUTED)
    add_text_svg(svg, 50, 1092, [credit], 26, color=MUTED, bold=True)
    add_drawio_text(root, "diagram_author", 50, 1092, 850, 34, [credit], 26, True, MUTED)

    svg.append("</svg>")
    ET.indent(mxfile, space="  ")
    (OUT / "stakeholder_chart.svg").write_text("\n".join(svg), encoding="utf-8")
    (OUT / "stakeholder_chart.drawio").write_text(ET.tostring(mxfile, encoding="unicode"), encoding="utf-8")
    img.save(OUT / "stakeholder_chart.png", dpi=(300, 300), optimize=True)
    ratio = page_w / page_h
    print(f"layout=balanced skill layered {direction}; target=1.35; helper ratio={achieved:.2f}; canvas={page_w}x{page_h}; final ratio={ratio:.2f}")
    for path in (OUT / "stakeholder_chart.drawio", OUT / "stakeholder_chart.svg", OUT / "stakeholder_chart.png"):
        print(f"wrote {path.name} ({path.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
