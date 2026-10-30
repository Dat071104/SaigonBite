"""Final design class diagram per main use case (report 3.x.5).

Author: 722I0004 · AI-assisted (Claude).
The per-layer plates in 3.x.2 list every member of every design class. This generator
consolidates them into one layered diagram per use case and refines it with what the
sequence diagrams and the code fixed: only the members the use case's system operations
call, signatures read from the code at HEAD, navigability, and a «persists» link from
each DAO to the entity it stores.

Inputs: models/shared/design_model.json (operation rows, classes, associations) and the
source tree saigonbite/ (signatures). Output per UC: models/UC-0x/dcd_uc0x_final_overview.{dot,svg,png}.
Run: python models/shared/final_dcd.py   (needs Graphviz `dot` on PATH)
"""
from __future__ import annotations

import ast
import json
import re
import subprocess
from html import escape
from pathlib import Path

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
# DAO that writes each table (from the INSERT/UPDATE statements in saigonbite/data_access/).
TABLE_DAO = {"orders": "OrderDAO", "order_line": "OrderDAO", "payment": "PaymentDAO", "delivery": "DeliveryDAO",
             "hub": "HubDAO", "hub_menu_item": "MenuDAO", "menu_item": "MenuDAO", "brand": "MenuDAO",
             "voucher": "VoucherDAO", "customer": "CustomerDAO", "address": "CustomerDAO",
             "user_account": "UserDAO", "replacement_offer": "ReplacementOfferDAO"}
LAYERS = [("view", "View layer (Flask blueprints, templates)", "#E8F1FA"),
          ("controller", "Controller layer (one use-case controller)", "#EAF5EA"),
          ("domain", "Domain layer (entities and value objects)", "#FFF6E0"),
          ("dao", "Data access layer (DAO per table)", "#F2ECF8")]


def read_code():
    """Signatures and dataclass fields from the code at HEAD."""
    classes, views = {}, {}
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
            elif isinstance(node, ast.FunctionDef):
                views[node.name] = signature(node)
    return classes, views


def signature(fn) -> str:
    args = []
    for a in fn.args.args:
        if a.arg in ("self", "cls"):
            continue
        args.append(a.arg + (": " + short_type(ast.unparse(a.annotation)) if a.annotation else ""))
    for a in fn.args.kwonlyargs:
        args.append(a.arg + (": " + short_type(ast.unparse(a.annotation)) if a.annotation else ""))
    ret = ": " + short_type(ast.unparse(fn.returns)) if fn.returns else ""
    return f"{fn.name}({', '.join(args)}){ret}"


def short_type(t: str) -> str:
    t = t.replace("typing.", "").replace("'", "")
    t = re.sub(r"Optional\[(.+)\]$", r"\1 | None", t)
    return t


def split_calls(value: str):
    out = []
    for part in (value or "").split(";"):
        part = part.strip()
        m = re.match(r"^([A-Za-z_][A-Za-z0-9_]*)\.([A-Za-z_][A-Za-z0-9_]*)", part)
        if m:
            out.append((m.group(1), m.group(2)))
    return out


def layer_of(name: str) -> str:
    c = MODEL["classes"].get(name, {})
    module = c.get("module", "")
    if "data_access" in module:
        return "dao"
    if "/domain/" in module:
        return "domain"
    if "/controllers/" in module:
        return "controller" if name.endswith("Controller") else "domain"
    return "domain"


def wrap(sig: str, width: int = 44) -> list[str]:
    if len(sig) <= width:
        return [sig]
    head, _, rest = sig.partition("(")
    params, _, tail = rest.rpartition(")")
    lines, cur = [], head + "("
    for p in [x.strip() for x in params.split(",")] if params else []:
        piece = p + ", "
        if len(cur) + len(piece) > width and cur.strip() not in (head + "(",):
            lines.append(cur.rstrip())
            cur = "      "
        cur += piece
    cur = cur.rstrip(", ") + ")" + tail
    lines.append(cur)
    return lines


def class_box(name, stereo, attrs, ops, fill):
    rows = [f'<TR><TD BGCOLOR="{fill}" BALIGN="CENTER"><FONT POINT-SIZE="12">«{escape(stereo)}»</FONT><BR/><B>{escape(name)}</B></TD></TR>']
    body = "<BR ALIGN=\"LEFT\"/>".join(escape(a) for a in attrs) + ('<BR ALIGN="LEFT"/>' if attrs else "")
    rows.append(f'<TR><TD ALIGN="LEFT" BALIGN="LEFT">{body if attrs else " "}</TD></TR>')
    lines = []
    for op in ops:
        for k, piece in enumerate(wrap(op)):
            lines.append(escape(("+ " if k == 0 else "  ") + piece))
    body = "<BR ALIGN=\"LEFT\"/>".join(lines) + ('<BR ALIGN="LEFT"/>' if lines else "")
    rows.append(f'<TR><TD ALIGN="LEFT" BALIGN="LEFT">{body if lines else " "}</TD></TR>')
    return '<<TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0" CELLPADDING="3" BGCOLOR="white">' + "".join(rows) + "</TABLE>>"


def build(uc: str, code_classes, code_views, only_controller=None, title_suffix="") -> str:
    rows = [r for r in MODEL["operation_rows"] if r["UC"] == uc
            and (only_controller is None or r["controller.method(signature)"].startswith(only_controller + "."))]
    view_ops, members, written, read = {}, {}, set(), set()
    calls = set()
    for r in rows:
        vf = r["view function (blueprint.function, METHOD /rule)"]
        ctrl = re.match(r"^([A-Za-z]+)\.([a-z_0-9]+)\(", r["controller.method(signature)"])
        if ctrl:
            members.setdefault(ctrl.group(1), set()).add(ctrl.group(2))
        for m in re.finditer(r"([a-z_]+)\.([a-z_0-9]+), ((?:GET|POST)(?:/POST)?) (\S+)", vf):
            bp, fn, verb, rule = m.groups()
            view_ops.setdefault(bp, []).append(f"{fn}() {verb} {rule}")
            if ctrl:
                calls.add((f"bp_{bp}", ctrl.group(1), "calls"))
        for cls, meth in split_calls(r["domain calls"]) + split_calls(r["DAO calls"]):
            members.setdefault(cls, set()).add(meth)
            if ctrl:
                calls.add((ctrl.group(1), cls, "uses"))
        for part in (r["tables R/W"] or "").split(";"):
            if ":" in part:
                table, mode = [x.strip() for x in part.split(":", 1)]
                (written if "W" in mode else read).add(table)
    # Entities persisted or read by this use case appear in the domain layer.
    for table in written | read:
        cls = TABLE_CLASS.get(table)
        if cls:
            members.setdefault(cls, set())
    nodes = {k: [] for k, _, _ in LAYERS}
    for bp, ops in sorted(view_ops.items()):
        nodes["view"].append((f"bp_{bp}", class_box(f"{bp} views", "boundary", [], sorted(set(ops)), LAYERS[0][2])))
    for cls in sorted(members):
        layer = layer_of(cls)
        info = code_classes.get(cls, {"methods": {}, "fields": []})
        ops = [info["methods"].get(m, m + "(…)") for m in sorted(members[cls]) if not m.startswith("__")]
        stereo = {"controller": "control", "dao": "DAO", "domain": MODEL["classes"].get(cls, {}).get("stereotype", "entity")}[layer]
        attrs = []
        if layer == "domain":
            table = next((t for t, c in TABLE_CLASS.items() if c == cls), None)
            show_all = table in written
            for fname, ftype in info["fields"]:
                if fname.endswith("_id") and fname != "id":
                    continue  # foreign keys are drawn as associations
                if show_all or fname in ("id", "state", "name", "code", "status"):
                    attrs.append(f"{fname}: {short_type(ftype)}")
            if table and not show_all:
                attrs.append("(read only in this use case)")
        fill = dict((k, f) for k, _, f in LAYERS)[layer]
        nodes[layer].append((cls, class_box(cls, stereo, attrs, ops, fill)))
    present = {n for layer in nodes.values() for n, _ in layer}
    out = ["digraph G {", 'graph [rankdir=TB, nodesep=0.15, ranksep=0.5, fontname="Arial", fontsize=16, pad=0.2, dpi=200];',
           'node [shape=plain, fontname="Arial", fontsize=13];', 'edge [fontname="Arial", fontsize=12];',
           f'labelloc="t"; label=<<B>{escape(uc)} {escape(UC_NAMES[uc])} — final design class diagram{escape(title_suffix)}</B><BR/>'
           f'<FONT POINT-SIZE="13">Owner {OWNERS[uc]} · Author 722I0004 · AI-assisted (Claude) · signatures from the code at the release commit</FONT>>;']
    for key, title, fill in LAYERS:
        if not nodes[key]:
            continue
        out.append(f'subgraph cluster_{key} {{ label=<<B>{escape(title)}</B>>; style="rounded,filled"; fillcolor="#FAFAFA"; color="#9AA7B4"; fontsize=15;')
        out.append("  { rank=same; " + " ".join(f'"{n}";' for n, _ in nodes[key]) + " }")
        for name, label in nodes[key]:
            out.append(f'  "{name}" [label={label}];')
        out.append("}")
    # Keep the four layers in four bands.
    order = [key for key, _, _ in LAYERS if nodes[key]]
    for a, b in zip(order, order[1:]):
        out.append(f'"{nodes[a][0][0]}" -> "{nodes[b][0][0]}" [style=invis, weight=5];')
    for src, dst, kind in sorted(calls):
        if src in present and dst in present and src != dst:
            out.append(f'"{src}" -> "{dst}" [style=dashed, arrowhead=vee, color="#5B6B7A"];')
    for table in sorted(written | read):
        cls, dao = TABLE_CLASS.get(table), TABLE_DAO.get(table)
        if cls in present and dao in present:
            out.append(f'"{dao}" -> "{cls}" [style=dashed, arrowhead=vee, dir=back, color="#7A4FA0", xlabel="«persists»", fontcolor="#7A4FA0", constraint=false];')
    for a in MODEL["associations"]:
        if a["source"] in present and a["target"] in present and layer_of(a["source"]) == layer_of(a["target"]) == "domain":
            head = "vee" if a.get("navigable") else "none"
            arrowtail = "diamond" if a.get("kind") == "composition" else ("odiamond" if a.get("kind") == "aggregation" else "none")
            out.append(f'"{a["source"]}" -> "{a["target"]}" [arrowhead={head}, dir=both, arrowtail={arrowtail}, '
                       f'taillabel="{a["source_multiplicity"]}", headlabel="{a["target_multiplicity"]}", label="{escape(a.get("role", ""))}", color="#B07A00", constraint=false];')
    out.append("}")
    return "\n".join(out)


def controllers(uc: str) -> list[str]:
    seen = []
    for r in MODEL["operation_rows"]:
        name = r["controller.method(signature)"].split(".", 1)[0]
        if r["UC"] == uc and name not in seen:
            seen.append(name)
    return seen


def main():
    code_classes, code_views = read_code()
    for uc in UC_NAMES:
        folder = REPO / "models" / uc
        parts = controllers(uc)
        # A use case served by two controllers gets one diagram per controller (Part A, Part B) to stay legible.
        for k, ctrl in enumerate(parts if len(parts) > 1 else [None]):
            suffix = f"_Part{chr(65 + k)}" if ctrl else ""
            stem = f"dcd_{uc.lower().replace('-', '')}_final_overview{suffix}"
            dot = build(uc, code_classes, code_views, ctrl, f" (part {chr(65 + k)}: {ctrl})" if ctrl else "")
            (folder / f"{stem}.dot").write_text(dot, encoding="utf-8")
            for fmt in ("svg", "png"):
                subprocess.run(["dot", f"-T{fmt}", str(folder / f"{stem}.dot"), "-o", str(folder / f"{stem}.{fmt}")], check=True)
            print("wrote", folder / f"{stem}.png")


if __name__ == "__main__":
    main()
