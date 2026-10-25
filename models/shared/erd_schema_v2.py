"""Build the Phase 3 schema-v2 ERD and class/table mapping from frozen JSON inputs.

Author: 722I0004 · AI-assisted (Codex). Reads the AST inventory/model only;
it never imports or executes application code.
"""
from __future__ import annotations

import csv
import importlib.util
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

sys.dont_write_bytecode = True

OUT = Path(__file__).resolve().parent
REPO = OUT.parent.parent
INVENTORY_PATH = REPO / "docs/part2/design/code_inventory.json"
MODEL_PATH = OUT / "design_model.json"
MAPPING_PATH = REPO / "docs/part2/design/class_table_mapping.csv"
WIDTH, HEIGHT = 1800, 1360

TABLE_CLASS = {
    "hub": "Hub",
    "brand": "Brand",
    "menu_item": "MenuItem",
    "hub_menu_item": "HubMenuItem",
    "user_account": "UserAccount",
    "customer": "Customer",
    "address": "Address",
    "voucher": "Voucher",
    "orders": "Order",
    "order_line": "OrderLine",
    "payment": "Payment",
    "delivery": "Delivery",
    "replacement_offer": "ReplacementOffer",
}

# The diagram pages are deliberately bounded and split by related table groups.
PARTS = {
    "PartA": {
        "figure": "4.3.1A",
        "title": "Schema v2 · identity, customer and hub records",
        "tables": ["hub", "user_account", "customer", "address"],
        "references": [],
        "continuation": "Catalogue/listing continues in PartB; orders in PartC; payment/delivery in PartD; offers in PartE.",
        "note": [
            "† P2-S02: user_account.created_at is required by §5.3 but is absent from the C0 table and class implementation.",
            "† P2-S03: TOURIST CHECK requires passport_no and email; nationality IS NOT NULL is absent at C0.",
            "† P2-S07: customer.user_id is FK + UNIQUE, but SQL does not require the linked user_account.role = CUSTOMER.",
            "Customer is one table with customer_type LOCAL / TOURIST; no subtype tables. Kitchen staff role iff hub_id is set.",
            "† design target, not yet in code at C0 (see P4 inputs P2-S02/S03/S07).",
        ],
    },
    "PartB": {
        "figure": "4.3.1B",
        "title": "Schema v2 · brands, menu items, hub listings and vouchers",
        "tables": ["brand", "menu_item", "hub_menu_item", "voucher"],
        "references": ["hub"],
        "continuation": "Hub resolves to PartA; orders/lines continue in PartC; payment/delivery and replacement offers in PartsD/E.",
        "note": [
            "hub_menu_item is the Hub–MenuItem association class; its composite PK is (hub_id, menu_item_id).",
            "UNIQUE: menu_item(brand_id, name); hub_menu_item(hub_id, menu_item_id) PK; brand.name and voucher.code.",
            "An absent hub_menu_item row is unlisted; is_available is per hub. Order snapshots retain historical names/prices.",
        ],
    },
    "PartC": {
        "figure": "4.3.1C",
        "title": "Schema v2 · orders and line snapshots",
        "tables": ["orders", "order_line"],
        "references": ["customer", "hub", "address", "voucher", "menu_item"],
        "continuation": "Refs are in PartsA/B; payment/delivery in PartD; offers in PartE.",
        "note": [
            "CHECK: T = S - D + F - Q; details in class_table_mapping.csv.",
            "SQL allows 0..* OrderLines; checkout targets 1..* (P2-S09).",
            "UNIQUE: token; order_line(order_id, menu_item_id); line snapshots retained.",
        ],
    },
    "PartD": {
        "figure": "4.3.1D",
        "title": "Schema v2 · payment and delivery records",
        "tables": ["payment", "delivery"],
        "references": ["orders", "user_account"],
        "continuation": "Order resolves to PartC; UserAccount resolves to PartA; replacement offers continue in PartE.",
        "note": [
            "Order 1–0..1 Payment and Order 1–0..1 Delivery are SQL maxima; successful checkout / markReady supplies required rows.",
            "Payment.amount is COD due or captured ONLINE amount C; refund_amount is owed, not paid. All event timestamps are UTC.",
            "Payment.updated_at is SQL NOT NULL; PaymentDAO.insert uses updated_at or created_at (P2-S08), so this is not a gap.",
            "FAILED / REFUNDED remain SQL/enum values but are deferred or unreachable per P2-S01; no payout is drawn.",
        ],
    },
    "PartE": {
        "figure": "4.3.1E",
        "title": "Schema v2 · replacement-offer history",
        "tables": ["replacement_offer"],
        "references": ["orders", "order_line", "menu_item"],
        "continuation": "Order and OrderLine resolve to PartC; target MenuItem resolves to PartB; payment history is in PartD.",
        "note": [
            "idx_offer_one_open is UNIQUE on order_id only WHERE state = 'OFFERED'; all resolved offers remain history.",
            "SQL does not require offer.order_id to match order_line.order_id or recheck target eligibility at the same hub (P2-S09).",
            "Original/new names and prices are snapshots; only new_menu_item_id references the current target item.",
            "Offer timestamps are UTC. No withdrawal_reason column or separate Shipper table exists in schema v2.",
        ],
    },
}

TABLE_POSITIONS = {
    "PartA": {
        "hub": (80, 120, 650),
        "user_account": (1000, 120, 650),
        "customer": (80, 590, 650),
        "address": (1000, 590, 650),
    },
    "PartB": {
        "brand": (80, 140, 600),
        "menu_item": (1000, 140, 600),
        "voucher": (80, 600, 600),
        "hub_menu_item": (1000, 600, 600),
    },
    "PartC": {
        "orders": (60, 110, 620),
        "order_line": (60, 900, 620),
    },
    "PartD": {
        "payment": (120, 140, 620),
        "delivery": (1040, 140, 620),
    },
    "PartE": {
        "replacement_offer": (550, 140, 700),
    },
}

REF_POSITIONS = {
    "PartB": {"hub": (1000, 850, 600, 120, "A")},
    "PartC": {
        "customer": (830, 110, 830, 120, "A"),
        "hub": (830, 290, 830, 120, "A"),
        "address": (830, 470, 830, 120, "A"),
        "voucher": (830, 650, 830, 120, "A"),
        "menu_item": (830, 900, 830, 120, "B"),
    },
    "PartD": {
        "orders": (120, 720, 620, 130, "C"),
        "user_account": (1040, 720, 620, 130, "A"),
    },
    "PartE": {
        "orders": (60, 750, 450, 130, "C"),
        "order_line": (675, 750, 450, 130, "C"),
        "menu_item": (1290, 750, 450, 130, "B"),
    },
}

# (part, child table, FK column, parent table, child endpoint, parent endpoint,
#  route points, child-end multiplicity, parent-end multiplicity, label locations)
EDGE_LAYOUTS = [
    ("PartA", "user_account", "hub_id", "hub", (1000, 250), (730, 250), [(1000, 250), (730, 250)], "0..*", "0..1", (930, 215, 740, 215)),
    ("PartA", "customer", "user_id", "user_account", (730, 670), (1150, 402), [(730, 670), (850, 670), (850, 500), (1150, 500), (1150, 402)], "0..1", "1", (740, 635, 1160, 438)),
    ("PartA", "address", "customer_id", "customer", (1000, 700), (730, 700), [(1000, 700), (730, 700)], "0..*", "1", (935, 665, 735, 720)),
    ("PartB", "menu_item", "brand_id", "brand", (1000, 270), (680, 270), [(1000, 270), (680, 270)], "0..*", "1", (930, 235, 685, 275)),
    ("PartB", "hub_menu_item", "menu_item_id", "menu_item", (1300, 600), (1300, 391), [(1300, 600), (1300, 391)], "0..*", "1", (1310, 550, 1310, 405)),
    ("PartB", "hub_menu_item", "hub_id", "hub", (1300, 758), (1300, 850), [(1300, 758), (1300, 850)], "0..*", "1", (1310, 770, 1360, 825)),
    ("PartC", "orders", "customer_id", "customer", (680, 180), (830, 170), [(680, 180), (830, 170)], "0..*", "1", (685, 150, 780, 145)),
    ("PartC", "orders", "hub_id", "hub", (680, 360), (830, 350), [(680, 360), (830, 350)], "0..*", "1", (685, 330, 780, 325)),
    ("PartC", "orders", "address_id", "address", (680, 540), (830, 530), [(680, 540), (830, 530)], "0..*", "1", (685, 510, 780, 505)),
    ("PartC", "orders", "voucher_id", "voucher", (680, 720), (830, 710), [(680, 720), (830, 710)], "0..*", "0..1", (685, 690, 780, 685)),
    ("PartC", "order_line", "order_id", "orders", (370, 900), (370, 795), [(370, 900), (370, 795)], "0..*", "1", (380, 855, 380, 810)),
    ("PartC", "order_line", "menu_item_id", "menu_item", (680, 1010), (830, 960), [(680, 1010), (830, 960)], "0..*", "1", (685, 1015, 780, 935)),
    ("PartD", "payment", "order_id", "orders", (430, 515), (430, 720), [(430, 515), (430, 720)], "0..1", "1", (440, 520, 440, 665)),
    ("PartD", "delivery", "order_id", "orders", (1040, 360), (740, 785), [(1040, 360), (800, 360), (800, 660), (740, 660), (740, 785)], "0..1", "1", (960, 330, 745, 765)),
    ("PartD", "delivery", "shipper_id", "user_account", (1350, 484), (1350, 720), [(1350, 484), (1350, 720)], "0..*", "0..1", (1360, 490, 1360, 695)),
    ("PartE", "replacement_offer", "order_id", "orders", (600, 546), (510, 815), [(600, 546), (600, 650), (510, 650), (510, 815)], "0..*", "1", (610, 550, 515, 785)),
    ("PartE", "replacement_offer", "order_line_id", "order_line", (900, 546), (900, 750), [(900, 546), (900, 750)], "0..*", "1", (910, 550, 910, 700)),
    ("PartE", "replacement_offer", "new_menu_item_id", "menu_item", (1200, 546), (1515, 750), [(1200, 546), (1200, 650), (1515, 650), (1515, 750)], "0..*", "1", (1210, 550, 1525, 700)),
]

ATTR_MAP = {
    ("hub_menu_item", "menu_item_id"): ("HubMenuItem", "item", "association object materialised from menu_item_id"),
    ("order_line", "order_id"): ("Order", "lines", "Order.lines composition; child FK has no scalar OrderLine attribute"),
    ("orders", "item_subtotal"): ("Order", "item_subtotal (property)", "derived from lines; persisted for the order row and reporting"),
    ("orders", "total_amount"): ("Order", "total (property)", "T = S − D + F − Q; derived property with a persisted SQL column"),
}

MONEY_MEANINGS = {
    "hub.base_delivery_fee": "Base delivery fee in whole VND.",
    "menu_item.price": "Current catalogue unit price in whole VND; existing order-line snapshots are unchanged.",
    "voucher.discount_value": "Whole VND for FIXED; percentage value for PERCENT.",
    "voucher.min_subtotal": "Minimum item subtotal in whole VND.",
    "voucher.max_discount": "Optional maximum discount in whole VND.",
    "orders.item_subtotal": "S: order item subtotal in whole VND before voucher discount.",
    "orders.voucher_discount": "D: voucher discount in whole VND.",
    "orders.delivery_fee": "F: charged delivery fee in whole VND.",
    "orders.quiet_discount": "Q: quiet-hub discount in whole VND.",
    "orders.total_amount": "T: order total in whole VND; SQL checks T = S − D + F − Q.",
    "order_line.unit_price": "Unit-price snapshot in whole VND; later catalogue edits do not rewrite it.",
    "payment.amount": "COD amount due or ONLINE captured amount C; current checkout writes the order total.",
    "payment.refund_amount": "Refund owed, not paid out; partial C − T after replacement, full C on an unfulfilled ONLINE order.",
    "delivery.cash_collected": "Cash recorded at delivery; COD completion requires cash equal to T.",
    "replacement_offer.original_unit_price": "Original order-line price snapshot in whole VND.",
    "replacement_offer.new_unit_price": "Offered replacement price snapshot in whole VND.",
}

TIMESTAMP_COLUMNS = {
    "hub.archived_at", "brand.archived_at", "menu_item.archived_at", "address.archived_at",
    "voucher.archived_at", "orders.placed_at", "orders.confirmed_at", "orders.ready_at",
    "orders.closed_at", "orders.archived_at", "payment.created_at", "payment.updated_at",
    "delivery.ready_at", "delivery.picked_up_at", "delivery.finished_at",
    "replacement_offer.offered_at", "replacement_offer.decided_at",
}

spec = importlib.util.spec_from_file_location("p2_diagram_renderer", OUT / "use_case_diagram.py")
R = importlib.util.module_from_spec(spec)
spec.loader.exec_module(R)
Page = R.Page


def read_inputs() -> tuple[dict, dict]:
    inventory = json.loads(INVENTORY_PATH.read_text(encoding="utf-8"))
    model = json.loads(MODEL_PATH.read_text(encoding="utf-8"))
    return inventory, model


def table_check_refs(table: dict, column: str) -> list[str]:
    pattern = re.compile(r"(?<![A-Za-z0-9_])" + re.escape(column) + r"(?![A-Za-z0-9_])")
    return [check for check in table.get("checks", []) if pattern.search(check)]


def composite_key_columns(table: dict, kind: str) -> dict[str, str]:
    result = {}
    prefix = "PRIMARY KEY" if kind == "pk" else "UNIQUE"
    for constraint in table.get("constraints", []):
        match = re.match(prefix + r"\s*\(([^)]*)\)", constraint, re.IGNORECASE)
        if match:
            cols = [part.strip() for part in match.group(1).split(",")]
            label = f"{prefix} ({', '.join(cols)})"
            for col in cols:
                result[col] = label
    return result


def indexes_for_table(schema: dict, table_name: str) -> list[dict]:
    return [idx for idx in schema.get("indexes", []) if idx.get("table") == table_name]


def column_uniqueness(schema: dict, table_name: str, table: dict, column: str) -> list[str]:
    result = []
    col = next(c for c in table["columns"] if c["name"] == column)
    if col.get("unique"):
        result.append("UNIQUE column constraint")
    composite = composite_key_columns(table, "unique")
    if column in composite:
        result.append(composite[column])
    for index in indexes_for_table(schema, table_name):
        definition = index.get("definition", "")
        if index.get("unique"):
            match = re.search(r"ON\s+\w+\s*\(([^)]*)\)", definition, re.IGNORECASE)
            index_cols = [x.strip() for x in match.group(1).split(",")] if match else [column]
            if column not in index_cols:
                continue
            index_cols_text = ", ".join(index_cols)
            where = re.search(r"\bWHERE\s+(.+?);?$", definition, re.IGNORECASE)
            condition = f" WHERE {where.group(1).rstrip(';')}" if where else ""
            result.append(f"UNIQUE index {index['name']} ({index_cols_text}){condition}")
    return result


def is_single_column_unique(schema: dict, table_name: str, table: dict, column: str) -> bool:
    col = next(c for c in table["columns"] if c["name"] == column)
    if col.get("unique"):
        return True
    # A one-column table-level UNIQUE is single-column; composite uniqueness is not.
    for constraint in table.get("constraints", []):
        match = re.match(r"UNIQUE\s*\(([^)]*)\)", constraint, re.IGNORECASE)
        if match and [x.strip() for x in match.group(1).split(",")] == [column]:
            return True
    return False


def fk_column(schema: dict, table_name: str, column: str) -> dict | None:
    table = schema["tables"][table_name]
    return next((c for c in table["columns"] if c["name"] == column), None)


def erd_column_label(schema: dict, table_name: str, column: dict) -> str:
    name = column["name"]
    table = schema["tables"][table_name]
    marks = []
    composite_pk = composite_key_columns(table, "pk")
    if column.get("primary_key") or name in composite_pk:
        marks.append("PK")
    if column.get("references"):
        marks.append("FK")
    unique = column_uniqueness(schema, table_name, table, name)
    if unique:
        marks.append("U" if unique == ["UNIQUE column constraint"] else "U*")
    if table_check_refs(table, name):
        marks.append("C")
    prefix = "/".join(marks)
    nullable = not column.get("not_null") and not column.get("primary_key") and name not in composite_pk
    suffix = "?" if nullable else ""
    return (prefix + " " if prefix else "") + name + suffix


def table_height(schema: dict, table_name: str, extra_rows: list[str] | None = None) -> int:
    attrs = [erd_column_label(schema, table_name, col) for col in schema["tables"][table_name]["columns"]]
    attrs.extend(extra_rows or [])
    return 65 + 31 * len(attrs)


def add_table(p, schema: dict, table_name: str, x: int, y: int, width: int, extra_rows: list[str] | None = None) -> int:
    attrs = [erd_column_label(schema, table_name, col) for col in schema["tables"][table_name]["columns"]]
    attrs.extend(extra_rows or [])
    p.node(table_name, table_name, x, y, width, 65 + 31 * len(attrs), "class", "#F4F8FB", attrs)
    return 65 + 31 * len(attrs)


def add_ref(p, table_name: str, x: int, y: int, width: int, height: int, part: str) -> str:
    rid = f"ref_{table_name}"
    label = f"«reference» {table_name}\nPK id · full table in {part}"
    p.node(rid, label, x, y, width, height, "ref", "#F5F8FA")
    return rid


def fk_relationship(schema: dict, child: str, column_name: str, parent: str) -> dict:
    child_table = schema["tables"][child]
    column = next(c for c in child_table["columns"] if c["name"] == column_name)
    references = column.get("references", [])
    assert [parent, "id"] in references, (child, column_name, parent, references)
    child_to_parent = "1" if column.get("not_null") else "0..1"
    parent_to_child = "0..1" if is_single_column_unique(schema, child, child_table, column_name) else "0..*"
    unique = column_uniqueness(schema, child, child_table, column_name)
    enforcement = ["FOREIGN KEY"]
    enforcement.append("NOT NULL" if column.get("not_null") else "nullable FK")
    if unique:
        enforcement.extend(unique)
    return {
        "source": child,
        "target": parent,
        "kind": "foreign_key",
        "column": column_name,
        "child_to_parent": child_to_parent,
        "parent_to_child": parent_to_child,
        "enforcement": enforcement,
    }


def read_edges_for_part(part: str, schema: dict) -> list[dict]:
    return [
        fk_relationship(schema, child, col, parent)
        for edge_part, child, col, parent, *_rest in EDGE_LAYOUTS
        if edge_part == part
    ]


def add_edges(p, part: str, schema: dict) -> list[dict]:
    metadata = []
    for i, (edge_part, child, column, parent, child_pt, parent_pt, points, child_mult, parent_mult, labels) in enumerate(EDGE_LAYOUTS):
        if edge_part != part:
            continue
        relationship = fk_relationship(schema, child, column, parent)
        assert (child_mult, parent_mult) == (relationship["parent_to_child"], relationship["child_to_parent"]), (part, child, column, "UML multiplicities belong at the opposite relation end")
        child_id = child if child in TABLE_POSITIONS[part] else f"ref_{child}"
        parent_id = parent if parent in TABLE_POSITIONS[part] else f"ref_{parent}"
        if part == "PartB" and parent == "hub":
            parent_id = "ref_hub"
        if part == "PartC" and parent in {"customer", "hub", "address", "voucher", "menu_item"}:
            parent_id = f"ref_{parent}"
        if part == "PartD" and parent in {"orders", "user_account"}:
            parent_id = f"ref_{parent}"
        if part == "PartE" and parent in {"orders", "order_line", "menu_item"}:
            parent_id = f"ref_{parent}"
        if child_id.startswith("ref_"):
            child_id = child
        if parent_id.startswith("ref_") and parent not in {r[0] for r in []}:
            pass
        p.edge(
            f"fk_{child}_{column}",
            child_id,
            parent_id,
            points,
            "",
            kind="assoc",
            ends=[(child_mult, labels[0], labels[1]), (parent_mult, labels[2], labels[3])],
        )
        metadata.append(fk_relationship(schema, child, column, parent))
    return metadata


def relevant_indexes(schema: dict, table_names: list[str], reference_names: list[str]) -> list[dict]:
    selected = set(table_names) | set(reference_names)
    return [idx for idx in schema.get("indexes", []) if idx.get("table") in selected]


def patch_sidecar(stem: str, part: str, raw: dict, phase3: dict) -> dict:
    path = OUT / f"{stem}.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["author"] = "722I0004 · AI-assisted (Codex)"
    data["phase3"] = phase3
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return data


def schema_metadata(schema: dict, table_names: list[str], reference_names: list[str]) -> dict:
    selected = list(dict.fromkeys(table_names + reference_names))
    return {
        "user_version": schema["user_version"],
        "schema_sha256": schema["sha256"],
        "tables": {
            name: {
                "columns": [
                    {k: v for k, v in column.items() if k != "definition"}
                    for column in schema["tables"][name]["columns"]
                ],
                "constraints": schema["tables"][name]["constraints"],
                "checks": schema["tables"][name]["checks"],
            }
            for name in selected
        },
        "indexes": [
            {
                "name": idx["name"],
                "table": idx["table"],
                "unique": idx["unique"],
                "definition_summary": (
                    "UNIQUE " if idx["unique"] else ""
                ) + re.search(r"ON\s+\w+\s*\(([^)]*)\)", idx.get("definition", ""), re.IGNORECASE).group(1).strip()
                + (" WHERE " + re.search(r"\bWHERE\s+(.+?);?$", idx.get("definition", ""), re.IGNORECASE).group(1).rstrip(";") if re.search(r"\bWHERE\s+(.+?);?$", idx.get("definition", ""), re.IGNORECASE) else ""),
            }
            for idx in relevant_indexes(schema, table_names, reference_names)
        ],
    }


def add_note(p, part: str, spec: dict) -> None:
    lines = spec["note"] + ["Continuation: " + spec["continuation"]]
    label = "\n".join(lines)
    if part == "PartA":
        p.node("part_note", label, 70, 960, 1660, 235, "note", "#FFF8E8")
    elif part == "PartB":
        p.node("part_note", label, 70, 1010, 1660, 215, "note", "#FFF8E8")
    elif part == "PartC":
        p.node("part_note", label, 760, 1070, 980, 145, "note", "#FFF8E8")
    elif part == "PartD":
        p.node("part_note", label, 70, 930, 1660, 285, "note", "#FFF8E8")
    elif part == "PartE":
        p.node("part_note", label, 70, 930, 1660, 285, "note", "#FFF8E8")


def build_part(part: str) -> dict:
    if part not in PARTS:
        raise ValueError(f"Unknown ERD part: {part}")
    inventory, model = read_inputs()
    schema = inventory["schema"]
    part_spec = PARTS[part]
    stem = f"erd_schema_v2_{part}"
    p = Page(stem, part_spec["title"], part_spec["figure"], WIDTH, HEIGHT)
    p.texts[-1]["text"] = f"Static schema v2 at C0 = {inventory['commit'][:7]}; full SQL mapping and notes are in §4.3.1."

    for table_name in part_spec["tables"]:
        x, y, width = TABLE_POSITIONS[part][table_name]
        add_table(p, schema, table_name, x, y, width)

    for ref_table, position in REF_POSITIONS.get(part, {}).items():
        x, y, width, height, page_ref = position
        add_ref(p, ref_table, x, y, width, height, page_ref)

    dependency_metadata = add_edges(p, part, schema)
    add_note(p, part, part_spec)
    data = p.export()

    table_names = part_spec["tables"]
    reference_names = part_spec["references"]
    elements = []
    for table_name in table_names:
        elements.append({
            "class": f"{TABLE_CLASS[table_name]} (table {table_name})",
            "attributes": [c["name"] for c in schema["tables"][table_name]["columns"]],
            "methods": [],
        })
    for ref_table in reference_names:
        elements.append({
            "class": f"{TABLE_CLASS[ref_table]} (reference to table {ref_table})",
            "attributes": ["id"],
            "methods": [],
        })
    elements.append({
        "class": f"Continuation / schema note ({part})",
        "attributes": ["cross-page references", "schema constraints", "C0 notes"],
        "methods": [],
    })

    phase3 = {
        "diagram_type": "erd",
        "elements": elements,
        "dependencies": dependency_metadata,
        "schema_metadata": schema_metadata(schema, table_names, reference_names),
        "reference_nodes": reference_names,
        "continuation": part_spec["continuation"],
        "legend": {
            "PK": "primary-key column (including composite-key members)",
            "FK": "foreign-key column; line labels show SQL multiplicity",
            "U": "single-column UNIQUE constraint",
            "U*": "member of a composite UNIQUE or partial UNIQUE index; not individually unique",
            "C": "column participates in one or more SQL CHECK expressions; full expressions are in the mapping CSV",
            "?": "SQL NULL is permitted",
            "multiplicity": "UML end labels are SQL cardinalities unless a note explicitly states an application invariant",
        },
        "schema_user_version": schema["user_version"],
        "C0": inventory["commit"],
        "evidence_label": "Static",
    }
    data = patch_sidecar(stem, part, data, phase3)
    min_pt = 26 * min(230 / WIDTH, 170 / HEIGHT) * 72 / 25.4
    data["min_placed_pt"] = min_pt
    # Preserve phase3 metadata while recording the conservative width/height print-size bound.
    data["phase3"]["min_placed_pt_at_230x170mm"] = round(min_pt, 4)
    (OUT / f"{stem}.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    assert min_pt >= 9, (stem, min_pt)
    return {"stem": stem, "nodes": len(data["nodes"]), "edges": len(data["edges"]), "min_placed_pt": round(min_pt, 4), "dependencies": len(dependency_metadata)}


def all_domain_fields(model: dict, class_name: str) -> tuple[set[str], set[str]]:
    cls = model["classes"][class_name]
    attrs = {a["name"] for a in cls.get("attributes", [])}
    properties = {m["name"] for m in cls.get("methods", []) if "property" in m.get("decorators", [])}
    return attrs, properties


def map_column(model: dict, table_name: str, column_name: str) -> tuple[str, str, str, str]:
    if (table_name, column_name) in ATTR_MAP:
        class_name, attr, note = ATTR_MAP[(table_name, column_name)]
        return class_name, attr, "association or property", note
    class_name = TABLE_CLASS[table_name]
    attrs, properties = all_domain_fields(model, class_name)
    if column_name in attrs:
        return class_name, column_name, "field", "Direct field-to-column correspondence in the shared model."
    if column_name in properties:
        return class_name, column_name + " (property)", "derived property", "Property has a persisted row column at C0."
    raise KeyError(f"No model mapping for {table_name}.{column_name} ({class_name})")


def status_and_subphase(table_name: str, column: str) -> tuple[str, str, str]:
    if (table_name, column) == ("customer", "nationality"):
        return ("P4-TARGET†", "P2-S03", "P4.7 (accepted by root)")
    if (table_name, column) == ("customer", "user_id"):
        return ("P4-TARGET†", "P2-S07", "P4.7 (accepted by root)")
    if (table_name, column) == ("payment", "updated_at"):
        return ("MATCH", "P2-S08 resolved", "No schema change; DAO supplies updated_at or created_at")
    if (table_name, column) == ("payment", "state"):
        return ("MATCH with deferred values", "P2-S01", "No FAILED/REFUNDED path or payout is designed")
    return ("MATCH (Static at C0)", "", "")


def sql_nullability(column: dict, table: dict, column_name: str) -> str:
    composite_pk = composite_key_columns(table, "pk")
    if column.get("primary_key"):
        return "NO (INTEGER PRIMARY KEY; implicit, not explicit NOT NULL)"
    if column_name in composite_pk:
        return "NO (composite PK member; explicit NOT NULL in schema)"
    return "NO (NOT NULL)" if column.get("not_null") else "YES (NULL allowed)"


def key_text(schema: dict, table_name: str, table: dict, column: dict) -> tuple[str, str, list[str]]:
    name = column["name"]
    pk_composite = composite_key_columns(table, "pk")
    pk = "PK" if column.get("primary_key") or name in pk_composite else ""
    fk = "; ".join(f"{ref[0]}.{ref[1]}" for ref in column.get("references", []))
    unique = column_uniqueness(schema, table_name, table, name)
    return pk, fk, unique


def cardinality_for_column(schema: dict, table_name: str, table: dict, column: dict) -> tuple[str, str]:
    refs = column.get("references", [])
    if not refs:
        return "—", "—"
    parent = refs[0][0]
    child_to_parent = "1" if column.get("not_null") else "0..1"
    parent_to_child = "0..1" if is_single_column_unique(schema, table_name, table, column["name"]) else "0..*"
    multiplicity = f"{TABLE_CLASS[table_name]} → {TABLE_CLASS[parent]}: {child_to_parent}; {TABLE_CLASS[parent]} → {TABLE_CLASS[table_name]}: {parent_to_child}"
    enforcement = "FOREIGN KEY"
    enforcement += " + NOT NULL" if column.get("not_null") else " (nullable FK)"
    unique = column_uniqueness(schema, table_name, table, column["name"])
    if unique:
        enforcement += "; " + "; ".join(unique)
    composite_pk = composite_key_columns(table, "pk")
    if column["name"] in composite_pk:
        enforcement += "; " + composite_pk[column["name"]]
    if (table_name, column["name"]) == ("order_line", "order_id"):
        multiplicity += "; target successful Order: 1..* lines (application invariant, not SQL minimum)"
        enforcement += "; SQL permits an Order with zero lines"
    if (table_name, column["name"]) == ("payment", "order_id"):
        multiplicity += "; successful checkout target: exactly one Payment (write-path invariant)"
        enforcement += "; SQL ensures at most one, not required presence"
    if (table_name, column["name"]) == ("delivery", "order_id"):
        multiplicity += "; created on markReady by the application path"
        enforcement += "; SQL ensures at most one, not required presence"
    if (table_name, column["name"]) == ("replacement_offer", "order_id"):
        multiplicity += "; OFFERED subset has at most one per Order"
        enforcement += "; partial UNIQUE index applies only WHERE state = 'OFFERED'"
    if (table_name, column["name"]) == ("delivery", "shipper_id"):
        enforcement += "; FK does not assert SHIPPER role or active status"
    if (table_name, column["name"]) == ("replacement_offer", "order_line_id"):
        enforcement += "; SQL does not assert offer.order_id equals the line's order_id"
    return multiplicity, enforcement


def money_or_time_meaning(table_name: str, column: str) -> str:
    key = f"{table_name}.{column}"
    if key in MONEY_MEANINGS:
        return MONEY_MEANINGS[key]
    if key in TIMESTAMP_COLUMNS:
        return "UTC timestamp (TEXT) per BR-20."
    if key in {"voucher.valid_from", "voucher.valid_until"}:
        return "Inclusive Asia/Ho_Chi_Minh calendar date (TEXT), not a UTC timestamp."
    if key == "user_account.is_active":
        return "Account lifecycle flag; SQL stores 0/1 and deactivation is distinct from archive."
    if key == "hub_menu_item.is_available":
        return "Per-hub availability flag; SQL stores 0/1."
    if key == "customer.customer_type":
        return "Single-table LOCAL / TOURIST discriminator."
    if key == "orders.archived_at":
        return "Order archive timestamp; child history and obligations remain attached to the retained order."
    if key in {"hub.archived_at", "brand.archived_at", "menu_item.archived_at", "address.archived_at", "voucher.archived_at"}:
        return "Nullable archive timestamp; non-null represents archived parent/profile/catalogue data."
    if key == "payment.state":
        return "Payment lifecycle value; SQL permits FAILED/REFUNDED, but the contract defers/unreaches those paths."
    if key == "delivery.shipper_id":
        return "Nullable FK to UserAccount; SHIPPER role/active checks remain application guards."
    if key == "order_line.item_name":
        return "Order-time menu-item name snapshot."
    if key in {"replacement_offer.original_item_name", "replacement_offer.new_item_name"}:
        return "Offer-time name snapshot."
    return "Persisted value or foreign-key scalar; see plan §5.3 and the relationship columns."


def build_mapping(inventory: dict, model: dict) -> dict:
    schema = inventory["schema"]
    headers = [
        "class", "attribute", "mapping_kind", "table", "column", "sql_type", "nullability",
        "check", "primary_key", "foreign_key", "unique", "multiplicity", "cardinality_enforcement",
        "meaning", "c0_status", "p4_input", "p4_subphase",
    ]
    rows = []
    all_columns = set()
    for table_name, class_name in TABLE_CLASS.items():
        table = schema["tables"][table_name]
        for column in table["columns"]:
            column_name = column["name"]
            all_columns.add((table_name, column_name))
            mapped_class, attr, mapping_kind, mapping_note = map_column(model, table_name, column_name)
            checks = table_check_refs(table, column_name)
            pk, fk, unique = key_text(schema, table_name, table, column)
            multiplicity, enforcement = cardinality_for_column(schema, table_name, table, column)
            status, p4_input, p4_subphase = status_and_subphase(table_name, column_name)
            meaning = money_or_time_meaning(table_name, column_name)
            if mapping_note:
                meaning = (meaning + " " + mapping_note).strip()
            if (table_name, column_name) == ("payment", "updated_at"):
                meaning += " Payment.updated_at is Optional[str] in the model; PaymentDAO.insert writes the supplied value or created_at."
            if (table_name, column_name) == ("customer", "nationality"):
                meaning += " The column exists but the TOURIST SQL condition does not require it; controller validation is Static evidence only."
            if (table_name, column_name) == ("customer", "user_id"):
                meaning += " FK + UNIQUE gives at most one profile per account; no SQL role=CUSTOMER condition."
            if (table_name, column_name) == ("payment", "state"):
                meaning += " FAILED / REFUNDED are declared values only; no failed-attempt row or payout operation is added here."
            rows.append({
                "class": mapped_class,
                "attribute": attr,
                "mapping_kind": mapping_kind,
                "table": table_name,
                "column": column_name,
                "sql_type": column["type"],
                "nullability": sql_nullability(column, table, column_name),
                "check": " | ".join(checks) if checks else "—",
                "primary_key": pk or "—",
                "foreign_key": fk or "—",
                "unique": " | ".join(unique) if unique else "—",
                "multiplicity": multiplicity,
                "cardinality_enforcement": enforcement,
                "meaning": meaning,
                "c0_status": status,
                "p4_input": p4_input or "—",
                "p4_subphase": p4_subphase or "—",
            })

        if table_name == "user_account":
            model_attr = next(a for a in model["classes"]["UserAccount"]["attributes"] if a["name"] == "created_at")
            assert model_attr["status"] == "GAP"
            rows.append({
                "class": "UserAccount", "attribute": "created_at", "mapping_kind": "target gap",
                "table": "user_account", "column": "— (column absent at C0)", "sql_type": "—",
                "nullability": "—", "check": "—", "primary_key": "—", "foreign_key": "—", "unique": "—",
                "multiplicity": "—", "cardinality_enforcement": "—",
                "meaning": "Required by plan §5.3; target column is missing from the schema and the code implementation.",
                "c0_status": "GAP†", "p4_input": "P2-S02", "p4_subphase": "P4.1",
            })

    # The read model exposes Brand.name with MenuItem, but that value is not stored in menu_item.
    rows.append({
        "class": "MenuItem", "attribute": "brand_name", "mapping_kind": "joined projection",
        "table": "brand", "column": "name (JOIN projection; not stored in menu_item)", "sql_type": "TEXT",
        "nullability": "NO (source brand.name NOT NULL)", "check": "—", "primary_key": "—",
        "foreign_key": "menu_item.brand_id → brand.id", "unique": "—", "multiplicity": "Brand 1 → 0..* MenuItem",
        "cardinality_enforcement": "menu_item.brand_id FK + NOT NULL; MenuItem brand_name is a read projection.",
        "meaning": "Display name joined from the persistent Brand row; not a menu_item column.",
        "c0_status": "MATCH (Static read projection)", "p4_input": "—", "p4_subphase": "—",
    })

    for subtype in ("LocalCustomer", "TouristCustomer"):
        rows.append({
            "class": subtype, "attribute": "customer_type", "mapping_kind": "single-table discriminator",
            "table": "customer", "column": "customer_type", "sql_type": "TEXT", "nullability": "NO (NOT NULL)",
            "check": "customer_type IN ('LOCAL', 'TOURIST')",
            "primary_key": "—", "foreign_key": "—", "unique": "—",
            "multiplicity": "No separate subtype table; one Customer row per linked account.",
            "cardinality_enforcement": "Customer.customer_type CHECK selects the subtype; one table stores both.",
            "meaning": "Local/Tourist discriminator maps to the same customer.customer_type column.",
            "c0_status": "MATCH (single-table inheritance)", "p4_input": "—", "p4_subphase": "—",
        })

    rows.append({
        "class": "OrderLine", "attribute": "line_total (property)", "mapping_kind": "computed, not persisted",
        "table": "—", "column": "— (unit_price × quantity)", "sql_type": "—", "nullability": "—",
        "check": "—", "primary_key": "—", "foreign_key": "—", "unique": "—", "multiplicity": "—",
        "cardinality_enforcement": "—", "meaning": "Computed from the line snapshot; no separate SQL column.",
        "c0_status": "MATCH (derived property)", "p4_input": "—", "p4_subphase": "—",
    })

    # Coverage guards: all real SQL columns have exactly one primary mapping row.
    primary_rows = [
        row for row in rows
        if row["table"] in schema["tables"]
        and row["column"] in {c["name"] for c in schema["tables"][row["table"]]["columns"]}
        and row["mapping_kind"] not in ("single-table discriminator", "joined projection")
    ]
    mapped = [(row["table"], row["column"]) for row in primary_rows]
    assert set(mapped) == all_columns, (sorted(all_columns - set(mapped)), sorted(set(mapped) - all_columns))
    assert len(mapped) == len(set(mapped)), "Duplicate primary class-to-column mapping"

    with MAPPING_PATH.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    return {"path": str(MAPPING_PATH), "rows": len(rows), "sql_columns": len(all_columns), "tables": len(TABLE_CLASS)}


def build_all() -> dict:
    inventory, model = read_inputs()
    schema = inventory["schema"]
    expected_tables = set(TABLE_CLASS)
    assert set(schema["tables"]) == expected_tables, (set(schema["tables"]), expected_tables)
    assert schema["user_version"] == 2
    assert model["C0"] == inventory["commit"]
    diagrams = [build_part(part) for part in PARTS]
    expected_fks = {
        (table_name, column["name"], ref[0])
        for table_name, table in schema["tables"].items()
        for column in table["columns"]
        for ref in column.get("references", [])
    }
    displayed_fks = {
        (child, column, parent)
        for _part, child, column, parent, *_rest in EDGE_LAYOUTS
    }
    assert expected_fks == displayed_fks, (sorted(expected_fks - displayed_fks), sorted(displayed_fks - expected_fks))
    assert len(displayed_fks) == 18
    mapping = build_mapping(inventory, model)
    return {"schema_user_version": schema["user_version"], "table_count": len(schema["tables"]), "foreign_key_count": len(expected_fks), "diagrams": diagrams, "mapping": mapping}


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps(build_all(), ensure_ascii=False, indent=2))
