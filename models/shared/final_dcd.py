"""Final design class diagrams per main use case (report 3.x.5).

Author: 722I0004 · AI-assisted (Claude).

3.x.2 lists every member of every design class. This generator draws, per use case,
  - one OVERVIEW figure: all classes of the four layers (view, controller, domain, data
    access) with class names only, every call/use arrow, the DAO -> entity links
    («persists» when a DAO method the use case calls writes the entity's table,
    «loads» when it only reads it) and the domain associations with multiplicities;
  - DETAIL SHEETS, one set per controller: the controller, the view functions that call it,
    the domain classes and DAOs it uses, with the member signatures read from the source
    tree at generation time (saigonbite/, parsed with ast).
Which DAO method writes or reads which table is read from the SQL statements recorded in
models/shared/design_model.json (INSERT/UPDATE/DELETE = writes, SELECT = reads).

Arrow directions follow the layering: view -> controller -> domain / DAO, and DAO -> entity
(the data access layer depends on the domain layer, never the other way round).

Each figure is laid out for a printed page (landscape 230 x 150 mm or portrait 170 x 225 mm,
the limits of the report build) and the generator searches the layout (row width, rank direction,
spacing, signature wrap) and the page orientation that give the largest printed text. The estimate is
    est_pt = min_font_pt_in_dot x placed_width_mm / (png_width_px / dpi x 25.4)
When the sheets of a controller do not reach THRESHOLD (9 pt) as one sheet, they are cut further
(STRATEGIES: view and controller / controller and domain / data access in one or two shares) and
the sheets are numbered A1, A2 ... (A, B per controller).
Run: python models/shared/final_dcd.py [UC-03 ...] [--summary out.json]   (needs Graphviz `dot` on PATH;
     a full run takes about 30 minutes). --controller X [--strategy four] redoes the sheets of one controller.
"""
from __future__ import annotations

import argparse
import ast
import json
import re
import struct
import subprocess
from concurrent.futures import ThreadPoolExecutor
from html import escape
from pathlib import Path

try:  # text measurement for packing boxes into rows; falls back to a width estimate
    from PIL import ImageFont
except ImportError:  # pragma: no cover
    ImageFont = None

REPO = Path(__file__).resolve().parents[2]
MODEL = json.loads((REPO / "models/shared/design_model.json").read_text(encoding="utf-8"))
UC_NAMES = {
    "UC-01": "Place an order",
    "UC-02": "Deliver an order",
    "UC-03": "Maintain hubs and kitchen capacity",
    "UC-04": "Produce management reports",
    "UC-05": "Decide an incoming order",
    "UC-06": "Maintain brands, menu items and hub listings",
}
OWNERS = {"UC-01": "722I0004", "UC-02": "523K0049", "UC-03": "722I0004",
          "UC-04": "523K0049", "UC-05": "523K0050", "UC-06": "523K0050"}
TABLE_CLASS = {"orders": "Order", "order_line": "OrderLine", "payment": "Payment", "delivery": "Delivery",
               "hub": "Hub", "hub_menu_item": "HubMenuItem", "menu_item": "MenuItem", "brand": "Brand",
               "voucher": "Voucher", "customer": "Customer", "address": "Address",
               "user_account": "UserAccount", "replacement_offer": "ReplacementOffer"}
LAYERS = [("view", "View layer (Flask blueprint functions)", "#E8F1FA"),
          ("controller", "Controller layer", "#EAF5EA"),
          ("dao", "Data access layer", "#F2ECF8"),
          ("domain", "Domain layer (entities and value objects)", "#FFF6E0")]
FILL = {k: f for k, _, f in LAYERS}
C_CALL, C_PERSIST, C_LOAD, C_ASSOC = "#4A5663", "#7A4FA0", "#00796B", "#B07A00"
DPI = 200
THRESHOLD = 9.0   # minimum printed text size (pt) a figure must reach
TARGET = 9.4      # a layout with this much is preferred if it is also airier
PAD = 0.08       # graph pad in inches (png size = bounding box + 2 x pad)
FONT = 14          # every text in a figure uses this size (the title block is larger)
PAGES = {"L": (230.0, 150.0), "P": (170.0, 225.0)}   # (max width mm, max height mm) in the report build
PAGE_NAME = {"L": "landscape", "P": "portrait"}


# ----------------------------------------------------------------------------- reading the code
def read_code():
    """Signatures and dataclass fields from the source tree."""
    classes = {}
    for path in (REPO / "saigonbite").rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in tree.body:
            if isinstance(node, ast.ClassDef):
                methods, fields = {}, []
                for item in node.body:
                    if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        methods[item.name] = signature(item)
                    elif isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
                        fields.append((item.target.id, ast.unparse(item.annotation)))
                classes[node.name] = {"methods": methods, "fields": fields}
    return classes


def signature(fn) -> str:
    args = []
    for a in fn.args.args + fn.args.kwonlyargs:
        if a.arg in ("self", "cls"):
            continue
        args.append(a.arg + (": " + short_type(ast.unparse(a.annotation)) if a.annotation else ""))
    ret = ": " + short_type(ast.unparse(fn.returns)) if fn.returns else ""
    return f"{fn.name}({', '.join(args)}){ret}"


def short_type(t: str) -> str:
    t = t.replace("typing.", "").replace("'", "")
    return re.sub(r"Optional\[(.+)\]$", r"\1 | None", t)


def split_calls(value: str):
    out = []
    for part in (value or "").split(";"):
        m = re.match(r"^([A-Za-z_][A-Za-z0-9_]*)\.([A-Za-z_][A-Za-z0-9_]*)", part.strip())
        if m:
            out.append((m.group(1), m.group(2)))
    return out


def layer_of(name: str) -> str:
    module = MODEL["classes"].get(name, {}).get("module", "")
    if "data_access" in module:
        return "dao"
    if "/controllers/" in module:
        return "controller"  # controllers and their value objects (view models) live in the controller layer
    return "domain"


def table_modes(dao: str, methods) -> dict:
    """Tables the called methods of one DAO touch: 'W' if an INSERT/UPDATE/DELETE statement names it, else 'R'."""
    modes = {}
    for meth in MODEL["classes"].get(dao, {}).get("methods", []):
        if meth["name"] not in methods:
            continue
        for stmt in meth.get("sql", []):
            write = any(k in ("INSERT", "UPDATE", "DELETE") for k in stmt["kinds"])
            for table in stmt["tables"]:
                if write or table not in modes:
                    modes[table] = "W" if write else modes.get(table, "R")
    return modes


# ----------------------------------------------------------------------------- the use-case model
def controllers(uc: str) -> list[str]:
    seen = []
    for r in MODEL["operation_rows"]:
        name = r["controller.method(signature)"].split(".", 1)[0]
        if r["UC"] == uc and name not in seen:
            seen.append(name)
    return seen


def collect(uc: str, code, only_controller=None) -> dict:
    """Classes, members and arrows of one use case (or of one of its controllers)."""
    rows = [r for r in MODEL["operation_rows"] if r["UC"] == uc
            and (only_controller is None or r["controller.method(signature)"].startswith(only_controller + "."))]
    view_ops, members, view_calls, uses = {}, {}, set(), set()
    for r in rows:
        vf = r["view function (blueprint.function, METHOD /rule)"]
        ctrl = re.match(r"^([A-Za-z]+)\.([a-z_0-9]+)\(", r["controller.method(signature)"])
        if ctrl:
            members.setdefault(ctrl.group(1), set()).add(ctrl.group(2))
        for m in re.finditer(r"([a-z_]+)\.([a-z_0-9]+), ((?:GET|POST)(?:/POST)?) (\S+)", vf):
            bp, fn, verb, rule = m.groups()
            view_ops.setdefault(bp, set()).add(f"{fn}() {verb} {rule}")
            if ctrl:
                view_calls.add((bp, ctrl.group(1)))
        for cls, meth in split_calls(r["domain calls"]) + split_calls(r["DAO calls"]):
            members.setdefault(cls, set()).add(meth)
            if ctrl:
                uses.add((ctrl.group(1), cls))
    nodes = {}  # id -> node dict
    for bp, ops in view_ops.items():
        nodes[f"bp_{bp}"] = dict(layer="view", name=f"{bp} views", stereo="boundary", attrs=[], ops=sorted(ops), raw=True)
    persist = set()  # (dao, entity, 'persists' | 'loads')
    dao_modes = {}
    for cls, meths in members.items():
        layer = layer_of(cls)
        if layer == "dao":
            dao_modes[cls] = table_modes(cls, meths)
    written = {t for modes in dao_modes.values() for t, m in modes.items() if m == "W"}
    entities = {}
    for dao, modes in dao_modes.items():
        for table, mode in modes.items():
            cls = TABLE_CLASS.get(table)
            if cls:
                entities[cls] = entities.get(cls) or table
                persist.add((dao, cls, "persists" if mode == "W" else "loads"))
    for cls in set(members) | set(entities):
        layer = layer_of(cls)
        model_stereo = MODEL["classes"].get(cls, {}).get("stereotype")
        stereo = {"controller": "control" if cls.endswith("Controller") else (model_stereo or "value"),
                  "dao": model_stereo or "DAO", "domain": model_stereo or "entity"}[layer]
        info = code.get(cls, {"methods": {}, "fields": []})
        ops = [info["methods"].get(m, m + "(…)") for m in sorted(members.get(cls, ())) if not m.startswith("__")]
        attrs, show_all = [], False
        if layer == "domain":
            table = next((t for t, c in TABLE_CLASS.items() if c == cls), None)
            show_all = table in written
            for fname, ftype in info["fields"]:
                if fname.endswith("_id") and fname != "id":
                    continue  # foreign keys are drawn as associations
                if show_all or fname in ("id", "state", "name", "code", "status"):
                    attrs.append(f"{fname}: {short_type(ftype)}")
        nodes[cls] = dict(layer=layer, name=cls, stereo=stereo, attrs=attrs, ops=ops, raw=False, written=show_all)
    assoc = []
    for a in MODEL["associations"]:
        if a["source"] in nodes and a["target"] in nodes and nodes[a["source"]]["layer"] == nodes[a["target"]]["layer"] == "domain":
            assoc.append(a)
    edges = [(f"bp_{bp}", c, "call") for bp, c in view_calls if f"bp_{bp}" in nodes]
    edges += [(c, d, "use") for c, d in uses if c in nodes and d in nodes and c != d]
    edges += [(d, e, kind) for d, e, kind in persist if d in nodes and e in nodes]
    return dict(uc=uc, controller=only_controller, nodes=nodes, edges=sorted(set(edges)), assoc=assoc)


# ----------------------------------------------------------------------------- text and boxes
_FONTS = {}


def text_width_in(text: str, size: float, bold=False) -> float:
    if ImageFont is not None:
        key = (size, bold)
        if key not in _FONTS:
            try:
                _FONTS[key] = ImageFont.truetype("arialbd.ttf" if bold else "arial.ttf", int(size * 10))
            except OSError:
                _FONTS[key] = None
        if _FONTS[key] is not None:
            return _FONTS[key].getlength(text) / 10 / 72
    return len(text) * size * 0.55 / 72


def split_top(s: str, sep: str = ",") -> list[str]:
    parts, depth, cur = [], 0, ""
    for ch in s:
        if ch in "[(":
            depth += 1
        elif ch in "])":
            depth -= 1
        if ch == sep and depth == 0:
            parts.append(cur.strip())
            cur = ""
        else:
            cur += ch
    if cur.strip():
        parts.append(cur.strip())
    return parts


def wrap(sig: str, width: int) -> list[str]:
    """Break a signature after commas outside brackets; continuation lines are indented."""
    if len(sig) <= width:
        return [sig]
    head, _, rest = sig.partition("(")
    params, _, tail = rest.rpartition(")")
    lines, cur = [], head + "("
    for p in split_top(params):
        piece = p + ", "
        if len(cur) + len(piece) > width and cur.strip() != head + "(":
            lines.append(cur.rstrip())
            cur = "     "
        cur += piece
    lines.append(cur.rstrip(", ") + ")" + tail)
    return lines


def box_lines(node, mode, wrap_w):
    attrs = node["attrs"] if mode == "full" else []
    ops = []
    if mode == "full":
        for op in node["ops"]:
            for k, piece in enumerate([op] if node.get("raw") else wrap(op, wrap_w)):
                ops.append(("+ " if k == 0 else "  ") + piece)
    return attrs, ops


def class_box(node, mode, wrap_w, size) -> tuple[str, float, float]:
    """HTML label and the estimated width and height (inches) of one class box."""
    attrs, ops = box_lines(node, mode, wrap_w)
    pad = 3
    s = size
    if mode == "names":  # one line: the stereotype is named once in the layer title
        return (f'<<TABLE BORDER="1" CELLBORDER="0" CELLSPACING="0" CELLPADDING="{pad}" BGCOLOR="{FILL[node["layer"]]}"><TR><TD>'
                f'<FONT POINT-SIZE="{s}"><B>{escape(node["name"])}</B></FONT></TD></TR></TABLE>>',
                text_width_in(node["name"], s, True) + 2 * (pad + 2) / 72, (1.25 * s + 2 * (pad + 2)) / 72)
    rows = [f'<TR><TD BGCOLOR="{FILL[node["layer"]]}" CELLPADDING="{pad}"><FONT POINT-SIZE="{s}">«{escape(node["stereo"])}»</FONT><BR/>'
            f'<FONT POINT-SIZE="{s}"><B>{escape(node["name"])}</B></FONT></TD></TR>']
    widths = [text_width_in(node["name"], s, True), text_width_in("«" + node["stereo"] + "»", s)]
    if attrs:
        cols = 2 if len(attrs) > 6 else 1
        per = -(-len(attrs) // cols)
        cells = []
        for c in range(cols):
            part = attrs[c * per:(c + 1) * per]
            cells.append('<TD ALIGN="LEFT" BALIGN="LEFT" CELLPADDING="1">' + "".join(
                f'<FONT POINT-SIZE="{s}">{escape(a)}</FONT><BR ALIGN="LEFT"/>' for a in part) + "</TD>")
        inner = ('<TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0" CELLPADDING="0"><TR>' + "".join(cells) + "</TR></TABLE>")
        rows.append(f'<TR><TD ALIGN="LEFT" CELLPADDING="{pad}">{inner}</TD></TR>')
        widths.append(sum(max(text_width_in(a, s) for a in attrs[c * per:(c + 1) * per]) for c in range(cols)) + 0.12 * (cols - 1))
    if ops:
        body = "".join(f'<FONT POINT-SIZE="{s}">{escape(o).replace(" ", "&#160;") if o.startswith(("  ", "+  ")) else escape(o)}</FONT><BR ALIGN="LEFT"/>' for o in ops)
        rows.append(f'<TR><TD ALIGN="LEFT" BALIGN="LEFT" CELLPADDING="{pad}">{body}</TD></TR>')
        widths.append(max(text_width_in(o, s) for o in ops))
    width = max(widths) + 2 * (pad + 3) / 72
    n_attr = -(-len(attrs) // (2 if len(attrs) > 6 else 1)) if attrs else 0
    height = (1.25 * s * (2 + n_attr + len(ops)) + 2 * (pad + 2) * (1 + bool(attrs) + bool(ops))) / 72
    return ('<<TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0" CELLPADDING="0" BGCOLOR="white">' + "".join(rows) + "</TABLE>>",
            width, height)


# ----------------------------------------------------------------------------- the dot file
def pack_rows(items, max_w, gap):
    """Greedy left-to-right packing of (id, width) into rows no wider than max_w."""
    rows, cur, w = [], [], 0.0
    for ident, width in items:
        if cur and w + gap + width > max_w:
            rows.append(cur)
            cur, w = [], 0.0
        w += (gap if cur else 0) + width
        cur.append(ident)
    if cur:
        rows.append(cur)
    return rows


def dao_shares(data, count):
    """Split the DAO boxes of a use case into `count` shares of similar height (member count)."""
    daos = sorted((k for k, v in data["nodes"].items() if v["layer"] == "dao"),
                  key=lambda k: (-len(data["nodes"][k]["ops"]), k))
    load, share = [0] * count, {}
    for k in daos:
        i = load.index(min(load))
        share[k] = i
        load[i] += len(data["nodes"][k]["ops"]) + 2
    return share


def select_nodes(data, modes):
    """The boxes a sheet shows and how each is drawn ('full' or 'names')."""
    nodes, node_mode = {}, {}
    group = modes.get("dao_group")  # (index, count): only this share of the DAOs, balanced by member count
    shares = dao_shares(data, group[1]) if group else {}
    for k, v in data["nodes"].items():
        m = modes.get(v["layer"])
        if m in ("active", "behaviour", "written"):  # domain classes picked by what they carry, drawn in full
            keep = {"active": v["ops"] or v["written"], "behaviour": v["ops"], "written": v["written"]}[m]
            if not keep:
                continue
            m = "full"
        if m and group and v["layer"] == "dao" and shares[k] != group[0]:
            continue
        if m:
            nodes[k], node_mode[k] = v, m
    # a DAO or entity with no call, use, persists or loads arrow to another box of this sheet would float; leave it out
    for k in [k for k, v in nodes.items() if v["layer"] in ("dao", "domain")]:
        if not any((e[0] == k and e[1] in nodes) or (e[1] == k and e[0] in nodes) for e in data["edges"]):
            del nodes[k], node_mode[k]
    return nodes, node_mode


def build_dot(data, modes, title, max_w, wrap_w, size=FONT, domain_free=False, nodesep=0.22, ranksep=0.4,
              rankdir="TB"):
    """modes: layer -> 'full' | 'names' | None (layer left out).
    Layers run top to bottom: view, controller, data access, domain, so every dependency arrow points
    downwards. The domain boxes are either packed in rows of max_w inches (domain_free False) or ranked by
    their associations (domain_free True). With rankdir LR the layers are columns and max_w is the
    tallest column in inches."""
    nodes, node_mode = select_nodes(data, modes)
    roles = modes.get("domain") != "names"
    labels = {k: class_box(v, node_mode[k], wrap_w, size) for k, v in nodes.items()}
    out = ["digraph G {",
           f'graph [rankdir={rankdir}, nodesep={nodesep}, ranksep={ranksep}, fontname="Arial", fontsize={size}, pad={PAD}, dpi={DPI}, newrank=true];',
           f'node [shape=plain, fontname="Arial", fontsize={size}];',
           f'edge [fontname="Arial", fontsize={size}, arrowsize=0.9, penwidth=1.1];']
    out.append(f'labelloc="t"; labeljust="l"; label={title};')
    prev_last = None
    for key, ltitle, _ in LAYERS:
        ids = sorted(k for k, v in nodes.items() if v["layer"] == key)
        if not ids:
            continue
        free = key == "domain" and domain_free
        rows = [] if free else pack_rows([(k, labels[k][1 if rankdir == 'TB' else 2]) for k in ids], max_w, nodesep)
        if all(node_mode[i] == "names" for i in ids):
            stereos = sorted({nodes[i]["stereo"] for i in ids}, key=lambda x: (x != "DAO", x))
            ltitle = f'{ltitle.split(" (")[0]} ({", ".join("«" + x + "»" for x in stereos)})'
        out.append(f'subgraph cluster_{key} {{ label=<<B>{escape(ltitle)}</B>>; labeljust="l"; style="rounded,filled"; fillcolor="#FAFAFA"; '
                   f'color="#9AA7B4"; fontsize={size}; margin=5;')
        for r in rows:
            out.append("  { rank=same; " + " ".join(f'"{n}";' for n in r) + " }")
        for n in ids:
            out.append(f'  "{n}" [label={labels[n][0]}];')
        out.append("}")
        firsts = ids if free else [rows[0][0]]
        if prev_last:
            for f in firsts:
                out.append(f'"{prev_last}" -> "{f}" [style=invis];')
        for a, b in zip(rows, rows[1:]):
            out.append(f'"{a[0]}" -> "{b[0]}" [style=invis];')
        prev_last = None if free else rows[-1][0]
    for src, dst, kind in data["edges"]:
        if src not in nodes or dst not in nodes:
            continue
        if kind in ("call", "use"):
            out.append(f'"{src}" -> "{dst}" [style=dashed, arrowhead=vee, color="{C_CALL}"];')
        else:
            color = C_PERSIST if kind == "persists" else C_LOAD
            style = "dashed" if kind == "persists" else "dotted"
            out.append(f'"{src}" -> "{dst}" [style={style}, arrowhead=vee, color="{color}", fontcolor="{color}", xlabel="«{kind}»"];')
    # Detail sheets show members only; the overview shows each domain association as a plain line, without
    # multiplicity labels (they piled up at the small domain boxes). Multiplicities: domain model 2.1.7.
    for a in ([] if "detail sheet" in title else data["assoc"]):
        if a["source"] in nodes and a["target"] in nodes:
            head = "vee" if a.get("navigable") else "none"
            tail = "diamond" if a.get("kind") == "composition" else ("odiamond" if a.get("kind") == "aggregation" else "none")
            out.append(f'"{a["source"]}" -> "{a["target"]}" [arrowhead={head}, dir=both, arrowtail={tail}, '
                                              f'{("xlabel=" + chr(34) + escape(a.get("role", "")) + chr(34) + ", ") if roles else ""}color="{C_ASSOC}", fontcolor="{C_ASSOC}"'
                       f'{"" if domain_free else ", constraint=false"}];')
    out.append("}")
    return "\n".join(out)


LEGEND = [("grey dashed: calls or uses", C_CALL), ("amber: association (multiplicities in the domain model, 2.1.7)", C_ASSOC),
          ("purple dashed: «persists» (DAO writes the entity)", C_PERSIST), ("teal dotted: «loads» (DAO only reads it)", C_LOAD)]


def title_block(uc, tag, size=FONT, width_in=9.0):
    """Title, footer line and legend; legend items fill lines no wider than width_in inches."""
    lines = [f'<B><FONT POINT-SIZE="{size + 2}">{escape(uc)} {escape(UC_NAMES[uc])}</FONT></B>',
             f'<B><FONT POINT-SIZE="{size}">Final design class diagram, {escape(tag)}</FONT></B>',
             f'<FONT POINT-SIZE="{size}">Owner {OWNERS[uc]} · Author 722I0004 · AI-assisted (Claude)</FONT>']
    cur, cur_w = "", 0.0
    for text, color in LEGEND:
        if color == C_ASSOC and tag.startswith("detail"):
            continue
        w = text_width_in(text + "    ", size)
        if cur and cur_w + w > width_in:
            lines.append(cur)
            cur, cur_w = "", 0.0
        cur += f'<FONT POINT-SIZE="{size}" COLOR="{color}">{escape(text)}</FONT>    '
        cur_w += w
    lines.append(cur)
    return "<" + '<BR ALIGN="LEFT"/>'.join(lines) + '<BR ALIGN="LEFT"/>>'


# ----------------------------------------------------------------------------- sizing
def render(dot: str, fmt: str = "png") -> bytes:
    return subprocess.run(["dot", f"-T{fmt}"], input=dot.encode("utf-8"), capture_output=True, check=True, timeout=300).stdout


def png_size(blob: bytes) -> tuple[int, int]:
    return struct.unpack(">II", blob[16:24])


def min_font(dot: str) -> float:
    sizes = [float(x) for x in re.findall(r'(?:fontsize=|POINT-SIZE=")([0-9.]+)', dot)]
    return min(sizes)


def estimate(w_px: int, h_px: int, font: float, page: str) -> float:
    wmax, hmax = PAGES[page]
    w_mm, h_mm = w_px / DPI * 25.4, h_px / DPI * 25.4
    return font * min(wmax / w_mm, hmax / h_mm)


def plain_px(dot: str) -> tuple[int, int]:
    """Pixel size of the PNG, from the bounding box that -Tplain reports (cheaper than rendering)."""
    out = subprocess.run(["dot", "-Tplain"], input=dot.encode("utf-8"), capture_output=True, check=True, timeout=60).stdout
    w, h = [float(x) for x in out.split(b"\n", 1)[0].split()[2:4]]
    return round((w + 2 * PAD) * DPI), round((h + 2 * PAD) * DPI)


def _try(args):
    data, modes, uc, tag, opt, size = args
    dot = build_dot(data, modes, title_block(uc, tag, size, opt["max_w"] + 1.0), size=size, **opt)
    try:
        w_px, h_px = plain_px(dot)
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
        return None
    best = None
    for page in "LP":
        est = estimate(w_px, h_px, min_font(dot), page)
        if best is None or est > best["est"]:
            best = dict(est=est, page=page, dot=dot, px=(w_px, h_px), opt=opt)
    return best


SPACINGS = ((0.12, 0.24), (0.2, 0.34))   # (nodesep, ranksep) in inches


def _search(data, modes, uc, tag, size, options):
    jobs = [(data, modes, uc, tag, opt, size) for opt in options]
    with ThreadPoolExecutor(max_workers=6) as pool:
        return [r for r in pool.map(_try, jobs) if r]


def best_layout(data, modes, uc, tag, size=FONT):
    """Search row width, signature wrap width, domain layout and spacing for the largest printed text
    (a coarse grid, then a refinement around the best three)."""
    full = any(m in ("full", "active", "behaviour", "written") for m in modes.values() if isinstance(m, str))
    wraps = (28, 38, 48) if full else (40,)
    coarse = [dict(max_w=float(mw), wrap_w=w, domain_free=free, nodesep=ns, ranksep=rs, rankdir=rd)
              for rd in ("TB", "LR") for free in (False, True) for ns, rs in SPACINGS for w in wraps
              for mw in (4, 6, 8, 10, 12, 15, 18)]
    results = _search(data, modes, uc, tag, size, coarse)
    seen = {tuple(sorted(r["opt"].items())) for r in results}
    fine = []
    for r in sorted(results, key=lambda r: -r["est"])[:3]:
        o = r["opt"]
        for dm in (-1.0, 0.0, 1.0):
            for dw in ((-5, 0, 5) if full else (0,)):
                for ns, rs in SPACINGS:
                    opt = dict(o, max_w=max(3.0, o["max_w"] + dm), wrap_w=max(24, o["wrap_w"] + dw), nodesep=ns, ranksep=rs)
                    key = tuple(sorted(opt.items()))
                    if key not in seen:
                        seen.add(key)
                        fine.append(opt)
    results += _search(data, modes, uc, tag, size, fine)
    # Prefer the airiest layout that still prints at TARGET or more; otherwise the largest text.
    good = [r for r in results if r["est"] >= TARGET]
    if good:
        return max(good, key=lambda r: (r["opt"]["nodesep"], r["est"]))
    return max(results, key=lambda r: r["est"])


# ----------------------------------------------------------------------------- the figures of each use case
FULL = {"view": "full", "controller": "full", "dao": "full", "domain": "full"}
# How the detail sheets of one controller are cut when one sheet is too crowded for 9 pt on the page:
# a list of (tag, layer modes); sheets that would be empty are skipped and the rest are numbered A1, A2 and so on. 'active' keeps the domain classes with called members or written attributes.
STRATEGIES = {
    "single": [("{c}", FULL)],
    "two": [("{c}, view, controller and domain", {"view": "full", "controller": "full", "dao": None, "domain": "active"}),
            ("{c}, data access", {"view": None, "controller": "names", "dao": "full", "domain": "names"})],
    "three": [("{c}, view and controller", {"view": "full", "controller": "full", "dao": None, "domain": None}),
              ("{c}, controller and domain", {"view": None, "controller": "names", "dao": None, "domain": "active"}),
              ("{c}, data access", {"view": None, "controller": "names", "dao": "full", "domain": "names"})],
    "four": [("{c}, view and controller", {"view": "full", "controller": "full", "dao": None, "domain": None}),
             ("{c}, controller and domain", {"view": None, "controller": "names", "dao": None, "domain": "active"}),
             ("{c}, data access (1 of 2)",
              {"view": None, "controller": "names", "dao": "full", "domain": "names", "dao_group": (0, 2)}),
             ("{c}, data access (2 of 2)",
              {"view": None, "controller": "names", "dao": "full", "domain": "names", "dao_group": (1, 2)})],
    "six": [("{c}, view functions", {"view": "full", "controller": "names", "dao": None, "domain": None}),
            ("{c}, controller and domain behaviour", {"view": None, "controller": "full", "dao": None, "domain": "behaviour"}),
            ("{c}, entities written", {"view": None, "controller": None, "dao": "names", "domain": "written"}),
            ("{c}, data access (1 of 2)",
             {"view": None, "controller": "names", "dao": "full", "domain": "names", "dao_group": (0, 2)}),
            ("{c}, data access (2 of 2)",
             {"view": None, "controller": "names", "dao": "full", "domain": "names", "dao_group": (1, 2)})],
}
START = {"UC-01": "three", "UC-02": "three", "UC-03": "single", "UC-04": "single", "UC-05": "three", "UC-06": "single"}   # first strategy tried per use case (the larger ones skip the small ones)


def figures(uc: str, code, report=print, only=None, strategy=None):
    """Yield (stem, tag, best layout) for the overview and the detail sheets of one use case.
    only: a controller name, to redo just its sheets; strategy: the first strategy to try for them."""
    base = f"dcd_{uc.lower().replace('-', '')}_final"
    tag = "overview (class names only)"
    modes = {k: "names" for k, _, _ in LAYERS}
    if only is None:
        yield f"{base}_overview", tag, best_layout(collect(uc, code), modes, uc, tag)
    for k, ctrl in enumerate(controllers(uc)):
        if only and ctrl != only:
            continue
        data, letter = collect(uc, code, ctrl), chr(65 + k)
        names = list(STRATEGIES)
        order = names[names.index(strategy or START.get(uc, "single")):]
        for name in order:
            made = []
            wanted = []
            for text, modes in STRATEGIES[name]:
                nodes, _ = select_nodes(data, modes)
                if len(nodes) > (1 if modes.get("controller") == "names" else 0):  # skip a sheet with nothing but a controller name
                    wanted.append((text, modes))
            for n, (text, modes) in enumerate(wanted, 1):
                suffix = "" if name == "single" else str(n)
                tag = f"detail sheet {letter}{suffix}: " + text.format(c=ctrl)
                made.append((f"{base}_detail_{letter}{suffix}", tag, best_layout(data, modes, uc, tag)))
            report(f"  {uc} {ctrl}: strategy {name} -> " + ", ".join(f"{m[0][-3:]} {m[2]['est']:.2f}" for m in made))
            if min(m[2]["est"] for m in made) >= THRESHOLD or name == order[-1]:
                yield from made
                break


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ucs", nargs="*")
    ap.add_argument("--summary")
    ap.add_argument("--controller", help="redo only the detail sheets of this controller")
    ap.add_argument("--strategy", help="first strategy to try with --controller: " + ", ".join(STRATEGIES))
    args = ap.parse_args()
    code = read_code()
    summary = []
    for uc in args.ucs or UC_NAMES:
        folder = REPO / "models" / uc
        for stem, tag, best in figures(uc, code, only=args.controller, strategy=args.strategy):
            (folder / f"{stem}.dot").write_text(best["dot"], encoding="utf-8")
            for fmt in ("svg", "png"):
                (folder / f"{stem}.{fmt}").write_bytes(render(best["dot"], fmt))
            w_px, h_px = png_size((folder / f"{stem}.png").read_bytes())
            wmax, _ = PAGES[best["page"]]
            summary.append(dict(uc=uc, stem=stem, tag=tag, png=f"models/{uc}/{stem}.png", dot=f"models/{uc}/{stem}.dot",
                                px=f"{w_px}x{h_px}", page=PAGE_NAME[best["page"]], width_mm=int(wmax),
                                min_font=min_font(best["dot"]),
                                est=round(estimate(w_px, h_px, min_font(best["dot"]), best["page"]), 2)))
            print(summary[-1])
    if args.summary:
        Path(args.summary).write_text(json.dumps(summary, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
