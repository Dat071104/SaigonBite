"""Build docs/part2/ui/screens.csv and coverage_check.md from the 41-occurrence SSD map.

Author: 722I0004 · AI-assisted (Claude Sonnet 5.5)

The screen list is written here (goal screens and the key alternatives only); the controller method of every
operation is read from Part2/notes/P4_B02/actual_route_controller_SSD_map.csv (SHA-256 7fcb455e...), so the table
cannot drift from the map. The check fails when any of the 41 occurrences has no screen.
"""
import csv
import hashlib
from pathlib import Path

UI = Path(__file__).resolve().parents[1]
MAP = Path(r"D:\RAD\FINAL\Part2\notes\P4_B02\actual_route_controller_SSD_map.csv")
MAP_SHA = "7fcb455ee23df6eebd23663534a177dc5e5c3a54de88503a5552134f4cd22fed"
assert hashlib.sha256(MAP.read_bytes()).hexdigest() == MAP_SHA, "SSD map changed"

P, D = "390x844", "1440x900"
CUST, KIT, SHIP, ADM, MGR = "CUSTOMER", "KITCHEN_STAFF", "SHIPPER", "ADMIN", "MANAGER"

# uc, id, name, role, viewport, routes, [(op, occurrence)], kind, template
S = [
 ("UC-01", "S01", "Choose a kitchen hub", CUST, P, "GET /order/hubs", [("OP-13", "01S-M01")], "goal", "order/hubs.html"),
 ("UC-01", "S02", "Hub is full, quieter hubs suggested", CUST, P, "POST /order/quote -> 409", [("OP-15", "01S-M03")], "alternative", "order/hubs.html"),
 ("UC-01", "S03", "Choose dishes, address and voucher", CUST, P, "GET /order/hubs/<id>", [("OP-14", "01S-M02")], "goal", "order/menu.html"),
 ("UC-01", "S04", "Check the quote and choose payment", CUST, P, "POST /order/quote", [("OP-15", "01S-M03")], "goal", "order/quote.html"),
 ("UC-01", "S05", "Quote changed, check it again", CUST, P, "POST /order/confirm -> 409", [("OP-01", "01S-M04")], "alternative", "order/quote.html"),
 ("UC-01", "S06", "Online payment simulator", CUST, P, "POST /order/confirm (ONLINE)", [("OP-01", "01S-M04")], "goal (online)", "order/payment_simulator.html"),
 ("UC-01", "S07", "Online payment declined", CUST, P, "POST /order/confirm -> 402", [("OP-01", "01S-M04")], "alternative", "order/quote.html"),
 ("UC-01", "S08", "Order placed", CUST, P, "POST /order/confirm -> GET /order/<id>/confirmation", [("OP-01", "01S-M04")], "goal", "order/confirmation.html"),
 ("UC-01", "S09", "Follow an order", CUST, P, "GET /order/<id>", [("OP-16", "01S-M05"), ("OP-07", "01S-M07")], "goal", "order/detail.html"),
 ("UC-01", "S10", "Receipt", CUST, P, "GET /order/<id>/receipt", [("OP-16", "01S-M05")], "goal", "order/receipt.html"),
 ("UC-01", "S11", "My orders", CUST, P, "GET /order/mine", [("OP-17", "01S-M06")], "goal", "order/my_orders.html"),
 ("UC-01", "S12", "Order cancelled", CUST, P, "POST /order/<id>/cancel -> GET /order/<id>", [("OP-07", "01S-M07")], "alternative", "order/detail.html"),

 ("UC-05", "S01", "Kitchen board", KIT, D, "GET /kitchen/", [("OP-19", "05S-M01")], "goal", "kitchen/board.html"),
 ("UC-05", "S02", "Kitchen order: confirm, offer a replacement or reject", KIT, D, "GET /kitchen/orders/<id>", [("OP-20", "05S-M02"), ("OP-02", "05S-M03"), ("OP-03", "05S-M04"), ("OP-04", "05S-M05")], "goal", "kitchen/order.html"),
 ("UC-05", "S03", "Replacement offered, waiting for the customer", KIT, D, "POST /kitchen/orders/<id>/offer", [("OP-04", "05S-M05")], "goal", "kitchen/order.html"),
 ("UC-05", "S04", "Order rejected with a reason", KIT, D, "POST /kitchen/orders/<id>/reject", [("OP-03", "05S-M04")], "alternative", "kitchen/order.html"),
 ("UC-05", "S05", "My orders: your answer is needed", CUST, P, "GET /order/mine", [("OP-17", "05S-M06")], "goal", "order/my_orders.html"),
 ("UC-05", "S06", "Replacement offer: accept or decline", CUST, P, "GET /order/<id>", [("OP-18", "05S-M07"), ("OP-05", "05S-M08"), ("OP-06", "05S-M09")], "goal", "order/detail.html"),
 ("UC-05", "S07", "Replacement accepted", CUST, P, "POST /order/<id>/replacement (accept)", [("OP-05", "05S-M08")], "goal", "order/detail.html"),
 ("UC-05", "S08", "Replacement declined", CUST, P, "POST /order/<id>/replacement (decline)", [("OP-06", "05S-M09")], "alternative", "order/detail.html"),
 ("UC-05", "S09", "Offer withdrawn: replacement ran out", CUST, P, "POST /order/<id>/replacement (accept, dish gone)", [("OP-05", "05S-M08")], "alternative", "order/detail.html"),

 ("UC-02", "S01", "Deliveries: ready for pickup", SHIP, P, "GET /delivery/", [("OP-21", "M01")], "goal", "delivery/board.html"),
 ("UC-02", "S02", "Delivery waiting for pickup", SHIP, P, "GET /delivery/orders/<id>", [("OP-22", "M02"), ("OP-10", "M03")], "goal", "delivery/detail.html"),
 ("UC-02", "S03", "Picked up: deliver or report a problem", SHIP, P, "POST /delivery/orders/<id>/pickup", [("OP-10", "M03"), ("OP-11", "M04"), ("OP-12", "M05")], "goal", "delivery/detail.html"),
 ("UC-02", "S04", "Pick-up lost to another shipper", SHIP, P, "POST /delivery/orders/<id>/pickup -> conflict", [("OP-10", "M03")], "alternative", "error.html"),
 ("UC-02", "S05", "Cash amount refused", SHIP, P, "POST /delivery/orders/<id>/delivered -> error", [("OP-11", "M04")], "alternative", "delivery/detail.html"),
 ("UC-02", "S06", "Delivered, cash collected", SHIP, P, "POST /delivery/orders/<id>/delivered", [("OP-11", "M04")], "goal", "delivery/detail.html"),
 ("UC-02", "S07", "Failed delivery recorded", SHIP, P, "POST /delivery/orders/<id>/failed", [("OP-12", "M05")], "alternative", "delivery/detail.html"),

 ("UC-03", "S01", "Hubs and kitchen capacity", ADM, D, "GET /admin/hubs", [("OP-23", "M03-01")], "goal", "admin/hubs.html"),
 ("UC-03", "S02", "Edit a hub", ADM, D, "GET /admin/hubs/<id>", [("OP-24", "M03-02"), ("OP-35", "M03-04")], "goal", "admin/hub_form.html"),
 ("UC-03", "S03", "Hub saved", ADM, D, "POST /admin/hubs/<id> -> GET /admin/hubs", [("OP-35", "M03-04")], "goal", "admin/hubs.html"),
 ("UC-03", "S04", "New hub", ADM, D, "GET /admin/hubs/new", [("OP-34", "M03-03")], "goal", "admin/hub_form.html"),
 ("UC-03", "S05", "Hub form refused: capacity out of range", ADM, D, "POST /admin/hubs/new -> 400", [("OP-34", "M03-03"), ("OP-35", "M03-04")], "alternative", "admin/hub_form.html"),
 ("UC-03", "S06", "Hub archived", ADM, D, "POST /admin/hubs/<id>/archive", [("OP-36", "M03-05")], "goal", "admin/hubs.html"),

 ("UC-06", "S01", "Brands and dishes", ADM, D, "GET /admin/menu", [("OP-25", "M06-A01"), ("OP-25", "M06-B01"), ("OP-37", "M06-A02"), ("OP-38", "M06-A03"), ("OP-39", "M06-A04"), ("OP-42", "M06-B04")], "goal", "admin/catalogue.html"),
 ("UC-06", "S02", "Brand created and renamed", ADM, D, "POST /admin/brands, POST /admin/brands/<id>", [("OP-37", "M06-A02"), ("OP-38", "M06-A03")], "goal", "admin/catalogue.html"),
 ("UC-06", "S03", "New dish", ADM, D, "GET /admin/items/new", [("OP-40", "M06-B02")], "goal", "admin/item_form.html"),
 ("UC-06", "S04", "Edit a dish", ADM, D, "GET /admin/items/<id>", [("OP-41", "M06-B03")], "goal", "admin/item_form.html"),
 ("UC-06", "S05", "Dish form refused: price", ADM, D, "POST /admin/items/new -> 400", [("OP-40", "M06-B02"), ("OP-41", "M06-B03")], "alternative", "admin/item_form.html"),
 ("UC-06", "S06", "Menu of a hub", ADM, D, "GET /admin/hubs/<id>/menu", [("OP-25", "M06-C01"), ("OP-43", "M06-C02"), ("OP-44", "M06-C03"), ("OP-45", "M06-C04")], "goal", "admin/hub_menu.html"),
 ("UC-06", "S07", "Dish added to the hub menu and marked sold out", ADM, D, "POST /admin/hubs/<id>/menu, POST .../availability", [("OP-43", "M06-C02"), ("OP-44", "M06-C03")], "goal", "admin/hub_menu.html"),
 ("UC-06", "S08", "Archived brand and dish stay listed as archived", ADM, D, "POST /admin/brands/<id>/archive, POST /admin/items/<id>/archive", [("OP-39", "M06-A04"), ("OP-42", "M06-B04"), ("OP-45", "M06-C04")], "alternative", "admin/catalogue.html"),

 ("UC-04", "S01", "Sales report", MGR, D, "GET /reports/sales", [("OP-26", "M01")], "goal", "reports/sales.html"),
 ("UC-04", "S02", "Hub workload now", MGR, D, "GET /reports/workload", [("OP-27", "M02")], "goal", "reports/workload.html"),
 ("UC-04", "S03", "Delivery performance", MGR, D, "GET /reports/delivery", [("OP-28", "M03")], "goal", "reports/delivery.html"),
 ("UC-04", "S04", "Empty period shows n/a", MGR, D, "GET /reports/sales?from=..&to=..", [("OP-26", "M01"), ("OP-28", "M03")], "alternative", "reports/sales.html"),
 ("UC-04", "S05", "Filter refused: From is after To", MGR, D, "GET /reports/sales -> 400", [("OP-26", "M01")], "alternative", "reports/sales.html"),
]


def occ_key(uc, op, occ):
    return f"{uc}|{op}|{occ}"


with MAP.open(encoding="utf-8", newline="") as f:
    rows = list(csv.DictReader(f))
ctrl = {r["op_id"]: r["controller_method"] for r in rows}
want = {}
for r in rows:
    occ = r["SSD_identity"].rsplit("#", 1)[1]
    want[occ_key(r["UC"], r["op_id"], occ)] = r
assert len(want) == 41, len(want)

covered = {}
out_rows = []
for uc, sid, name, role, vp, routes, ops, kind, tpl in S:
    for op, occ in ops:
        k = occ_key(uc, op, occ)
        assert k in want, f"{uc}-{sid}: {k} is not in the SSD map"
        covered.setdefault(k, []).append(f"{uc}-{sid}")
    out_rows.append({
        "uc": uc, "screen_id": f"{uc}-{sid}", "name": name, "role": role, "viewport": vp, "routes": routes,
        "ssd_ops": " ".join(o for o, _ in ops), "occurrences": " ".join(f"{uc}#{c}" for _, c in ops),
        "controller_methods": " ".join(sorted({ctrl[o] for o, _ in ops})), "kind": kind, "template": tpl})

with (UI / "screens.csv").open("w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(out_rows[0]))
    w.writeheader()
    w.writerows(out_rows)

missing = sorted(set(want) - set(covered))
lines = ["# SSD occurrence coverage check", "",
         "Author: 722I0004 · AI-assisted (Claude Sonnet 5.5)", "",
         f"Source map: `Part2/notes/P4_B02/actual_route_controller_SSD_map.csv` (SHA-256 `{MAP_SHA}`), "
         f"{len(rows)} rows, {len(want)} distinct occurrences (the three `listCatalogue` occurrences M06-A01, M06-B01, "
         "M06-C01 are kept apart).", "",
         f"Screens in `screens.csv`: {len(out_rows)}. Occurrences with at least one screen: {len(covered)} of {len(want)}.",
         f"Result: {'PASS' if not missing else 'FAIL, missing ' + ', '.join(missing)}", "",
         "| UC | Op | Occurrence | Operation | Screens |", "|---|---|---|---|---|"]
for k, r in sorted(want.items()):
    uc, op, occ = k.split("|")
    lines.append(f"| {uc} | {op} | {occ} | {r['operation']} | {', '.join(covered.get(k, ['MISSING']))} |")
(UI / "coverage_check.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"screens={len(out_rows)} occurrences covered={len(covered)}/{len(want)} missing={missing}")
assert not missing
