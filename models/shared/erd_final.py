"""Entity-relationship diagram of the delivered schema (report 4.3.1).

Author: 722I0004 · AI-assisted (Claude).
Loads db/schema.sql into an in-memory SQLite database and draws every table, column, key and
foreign key with Graphviz, in two parts (people, hubs and catalogue / orders and their records).
Also writes models/shared/class_table_mapping.csv, the persistent-class to table mapping.
Run: python models/shared/erd_final.py   (needs Graphviz `dot`)
"""
import ast
import csv
import sqlite3
import subprocess
from html import escape
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "models/shared"
PARTS = {
    "A": ("People, hubs, catalogue and vouchers", ["user_account", "customer", "address", "hub", "brand", "menu_item", "hub_menu_item", "voucher"]),
    "B": ("Orders and their records", ["orders", "order_line", "payment", "delivery", "replacement_offer"]),
}
CLASS_OF = {"user_account": "UserAccount", "customer": "Customer (LocalCustomer, TouristCustomer)", "address": "Address",
            "hub": "Hub", "brand": "Brand", "menu_item": "MenuItem", "hub_menu_item": "HubMenuItem (association class)",
            "voucher": "Voucher", "orders": "Order", "order_line": "OrderLine", "payment": "Payment",
            "delivery": "Delivery", "replacement_offer": "ReplacementOffer"}


def schema():
    db = sqlite3.connect(":memory:")
    db.executescript((REPO / "db/schema.sql").read_text(encoding="utf-8"))
    tables = {}
    for (name,) in db.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"):
        cols = db.execute(f"PRAGMA table_info({name})").fetchall()
        fks = db.execute(f"PRAGMA foreign_key_list({name})").fetchall()
        uniq = set()
        for idx in db.execute(f"PRAGMA index_list({name})").fetchall():
            if idx[2] and not idx[4]:  # unique, and not a partial index
                info = db.execute(f"PRAGMA index_info({idx[1]})").fetchall()
                if len(info) == 1:
                    uniq.add(info[0][2])
        tables[name] = {"cols": cols, "fks": fks, "unique": uniq}
    triggers = [r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type='trigger'")]
    indexes = [r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type='index' AND sql IS NOT NULL")]
    return tables, triggers, indexes


def box(name, t, fill):
    fk_cols = {f[3] for f in t["fks"]}
    rows = [f'<TR><TD BGCOLOR="{fill}" COLSPAN="2"><B>{escape(name)}</B></TD></TR>']
    for cid, col, typ, notnull, default, pk in t["cols"]:
        marks = []
        if pk:
            marks.append("PK")
        if col in fk_cols:
            marks.append("FK")
        if col in t["unique"]:
            marks.append("U")
        label = escape(col) + ("" if notnull or pk else " ?")
        rows.append(f'<TR><TD ALIGN="LEFT" PORT="{escape(col)}">{label}</TD><TD ALIGN="LEFT">{escape(typ)} {" ".join(marks)}</TD></TR>')
    return '<<TABLE BORDER="1" CELLBORDER="0" CELLSPACING="0" CELLPADDING="3" BGCOLOR="white">' + "".join(rows) + "</TABLE>>"


def draw(tables):
    for key, (title, names) in PARTS.items():
        out = ["digraph ERD {", 'graph [rankdir=LR, nodesep=0.3, ranksep=0.7, fontname="Arial", fontsize=16, pad=0.2, dpi=200, labelloc="t",',
               f' label=<<B>Schema v2 (db/schema.sql) — part {key}: {escape(title)}</B><BR/><FONT POINT-SIZE="12">Author 722I0004 · AI-assisted (Claude) · PK primary key · FK foreign key · U unique · ? nullable · relationship ends: || exactly one · |o zero or one · o&lt; zero or many (also written as 1, 0..1, 0..*)</FONT>>];',
               'node [shape=plain, fontname="Arial", fontsize=13];', 'edge [color="#40505F", penwidth=1.2];']
        shown = set(names)
        for n in names:
            out.append(f'"{n}" [label={box(n, tables[n], "#E8F1FA" if key == "A" else "#FFF6E0")}];')
        for n in names:
            for f in tables[n]["fks"]:
                target = f[2]
                if target not in shown:
                    out.append(f'"{target}" [label=<<TABLE BORDER="1" CELLBORDER="0" BGCOLOR="#EEEEEE"><TR><TD><I>{escape(target)}</I><BR/><FONT POINT-SIZE="11">(part {"A" if key == "B" else "B"})</FONT></TD></TR></TABLE>>];')
                    shown.add(target)
                # Crow's foot ends (shape nearest the table first): child end 0..1 when the FK column is UNIQUE,
                # else 0..*; parent end exactly 1 when the FK column is NOT NULL, else 0..1.
                notnull = next(c[3] for c in tables[n]["cols"] if c[1] == f[3])
                unique = f[3] in tables[n]["unique"]
                head, hl = ("teeodot", "0..1") if unique else ("crowodot", "0..*")
                tail, tl = ("teetee", "1") if notnull else ("teeodot", "0..1")
                out.append(f'"{target}" -> "{n}":"{f[3]}" [arrowhead={head}, arrowtail={tail}, dir=both, '
                           f'headlabel="{hl}", taillabel="{tl}", labelfontsize=11, labelfontname=Arial, labeldistance=2.2];')
        out.append("}")
        dot = OUT / f"erd_final_Part{key}.dot"
        dot.write_text("\n".join(out), encoding="utf-8")
        for fmt in ("svg", "png"):
            subprocess.run(["dot", f"-T{fmt}", str(dot), "-o", str(dot.with_suffix("." + fmt))], check=True)


def dataclass_fields():
    fields = {}
    tree = ast.parse((REPO / "saigonbite/business/domain/models.py").read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            fields[node.name] = [s.target.id for s in node.body if isinstance(s, ast.AnnAssign)]
    return fields


def mapping(tables):
    fields = dataclass_fields()
    rows = []
    for table, cls in CLASS_OF.items():
        base = cls.split(" ")[0]
        attrs = set(fields.get(base, []))
        cols = [c[1] for c in tables[table]["cols"]]
        fks = {f[3]: f[2] for f in tables[table]["fks"]}
        same = [c for c in cols if c in attrs and c not in fks]
        fk = [f"{c} → {fks[c]}" for c in cols if c in fks]
        only_db = [c for c in cols if c not in attrs and c not in fks]
        only_cls = sorted(a for a in attrs if a not in cols)
        rows.append({"class": cls, "table": table, "attributes stored in columns of the same name": ", ".join(same),
                     "associations stored as foreign keys": ", ".join(fk) or "—",
                     "columns without a same-name attribute": ", ".join(only_db) or "—",
                     "attributes not stored as a column": ", ".join(only_cls) or "—"})
    with (OUT / "class_table_mapping.csv").open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    return rows


if __name__ == "__main__":
    tables, triggers, indexes = schema()
    draw(tables)
    rows = mapping(tables)
    print(len(tables), "tables;", sum(len(t["cols"]) for t in tables.values()), "columns;",
          sum(len(t["fks"]) for t in tables.values()), "foreign keys;", len(triggers), "triggers;", len(indexes), "indexes")
