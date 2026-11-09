"""Whole Order lifecycle on one page (report 2.2.1 iv, Figure 2.3).

Author: 722I0004 · AI-assisted (Claude).
States and allowed transitions are read from ALLOWED_TRANSITIONS in
saigonbite/business/domain/models.py (the script stops if they differ from the labels);
the event [guard] / effect labels are written by hand and cross-checked against views 2.3A-E.
Run: python models/shared/sm_order_overview.py   (needs Graphviz `dot`)
"""
import ast
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "models/shared/sm_order_overview"

LABELS = {
    ("PLACED", "CONFIRMED"): "confirmOrder [own hub, no open offer]\n(UC-05)",
    ("PLACED", "REJECTED"): "rejectOrder(reason) (UC-05) or\ndeclineReplacement (SUC-03)\n/ release payment",
    ("PLACED", "CANCELLED"): "cancelOrder (SUC-04)\n/ withdraw offer, release payment",
    ("CONFIRMED", "PREPARING"): "startPreparing\n[own hub] (SUC-05)",
    ("CONFIRMED", "CANCELLED"): "cancelOrder (SUC-04)\n/ release payment",
    ("PREPARING", "READY"): "markReady (SUC-05)\n/ create Delivery AWAITING_PICKUP",
    ("READY", "OUT_FOR_DELIVERY"): "takeDelivery [active shipper,\nnot yet assigned] (UC-02)",
    ("OUT_FOR_DELIVERY", "DELIVERED"): "confirmDelivered [assigned shipper;\nCOD cash = total] / COD PAID (UC-02)",
    ("OUT_FOR_DELIVERY", "DELIVERY_FAILED"): "reportFailure(reason) [assigned shipper]\n/ release payment (UC-02)",
}


def transitions():
    tree = ast.parse((REPO / "saigonbite/business/domain/models.py").read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.AnnAssign) and getattr(node.target, "id", "") == "ALLOWED_TRANSITIONS":
            for key, value in zip(node.value.keys, node.value.values):
                src = key.attr
                targets = [e.attr for e in value.args[0].elts] if value.args else []
                for dst in targets:
                    yield src, dst
            return


def main():
    pairs = sorted(transitions())
    assert set(pairs) == set(LABELS), set(pairs) ^ set(LABELS)
    states = sorted({s for p in pairs for s in p})
    terminal = {"DELIVERED", "DELIVERY_FAILED", "REJECTED", "CANCELLED"}
    out = ['digraph G {', 'graph [rankdir=TB, fontname="Arial", fontsize=16, nodesep=0.6, ranksep=0.45, pad=0.3, dpi=200,',
           ' labelloc="t", label=<<B>Order — complete lifecycle (states and transitions from the code)</B><BR/><FONT POINT-SIZE="13">Author 722I0004 · AI-assisted (Claude) · detailed views with postcondition links: Figures 2.3A–2.3E</FONT>>];',
           'node [shape=box, style="rounded,filled", fillcolor="#FFF6E0", fontname="Arial", fontsize=15, penwidth=1.4];',
           'edge [fontname="Arial", fontsize=12, color="#36454F"];',
           'start [shape=circle, label="", width=0.25, style=filled, fillcolor=black];']
    for s in states:
        extra = ', peripheries=2, fillcolor="#EEF2F5"' if s in terminal else ""
        out.append(f'"{s}" [label="{s}"{extra}];')
    for s in sorted(terminal):
        out.append(f'"end_{s}" [shape=doublecircle, label="", width=0.18, style=filled, fillcolor=black];')
        out.append(f'"{s}" -> "end_{s}" [label="archiveOrder\\n(SUC-09)", fontsize=11, style=dotted];')
    out.append('start -> PLACED [label="confirmCheckout [quote unchanged, hub not busy,\\nCOD, or ONLINE approved by the simulator]\\n/ save lines, snapshots, payment (UC-01)"];')
    # Two separate requests by two actors: kitchen staff offers, later the customer accepts (event [guard] / effect).
    out.append('PLACED:e -> PLACED:ne [label="offerReplacement [line unavailable,\\nno open offer] / open offer (UC-05)"];')
    out.append('PLACED:w -> PLACED:nw [label="acceptReplacement [offer still valid]\\n/ swap line, recompute totals,\\nrecord refund owed (SUC-03)"];')
    # Leave PLACED from its lower corners so the side edges do not cross the two self-loop labels.
    port = {("PLACED", "CANCELLED"): ":sw", ("PLACED", "REJECTED"): ":se"}
    for (a, b) in pairs:
        out.append(f'"{a}"{port.get((a, b), "")} -> "{b}" [label="{LABELS[(a, b)]}"];')
    out.append('{ rank=same; REJECTED; CANCELLED; }')
    out.append('}')
    OUT.with_suffix(".dot").write_text("\n".join(out), encoding="utf-8")
    for fmt in ("svg", "png"):
        subprocess.run(["dot", f"-T{fmt}", str(OUT.with_suffix(".dot")), "-o", str(OUT.with_suffix("." + fmt))], check=True)
    print("wrote", OUT.with_suffix(".png"))


if __name__ == "__main__":
    main()
