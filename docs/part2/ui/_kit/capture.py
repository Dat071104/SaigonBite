"""Screenshot run of the real app: every in-scope screen of screens.csv at its own viewport.

Author: 722I0004 · AI-assisted (Claude Sonnet 5.5)

Usage (tools venv):  capture.py --mode before|implemented [--port 5102]
  before       -> docs/part2/ui/_before/<screen id>.png
  implemented  -> docs/part2/ui/UC-0x/implemented/<screen id>.png
Also writes docs/part2/ui/_kit/captured/<mode>/<screen id>.txt (visible text of the page, the source of
the real names and money values used in the mockups) and captured/<mode>/run.json (order ids, versions).

One fresh demo DB per run (Part2/notes/P5/db/), a local Flask development server, one Edge profile per role.
Screens are reached by clicking through the UI; nothing is written to the database directly.
"""
import argparse
import json
import re
import sys
import time
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
UI = HERE.parent
REPO = UI.parents[2]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(REPO / "docs" / "part2" / "test_report" / "integration_2026-10-27" / "scripts"))
from render import measure, summary  # noqa: E402
from p5lib import NOTES, Roles, new_db, start_server, stop_server, versions  # noqa: E402
from playwright.sync_api import sync_playwright  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--mode", required=True, choices=["before", "implemented"])
ap.add_argument("--port", type=int, default=5102)
args = ap.parse_args()

BASE = f"http://127.0.0.1:{args.port}"
TXT = HERE / "captured" / args.mode
TXT.mkdir(parents=True, exist_ok=True)
run_info = {"mode": args.mode, "orders": {}, "date": date.today().isoformat()}
measures = {}
# In a full-page figure the sticky total bar would float over the middle of the page: show it in the flow instead.
FIGURE_CSS = ".summary-bar{position:static !important}"


def out_png(sid: str) -> Path:
    if args.mode == "before":
        d = UI / "_before"
    else:
        d = UI / sid[:5] / "implemented"
    d.mkdir(parents=True, exist_ok=True)
    return d / f"{sid}.png"


def vnd_int(text: str) -> int:
    return int(re.sub(r"[^\d]", "", text))


db = new_db(NOTES / "db" / f"capture_{args.mode}_{int(time.time())}.db", demo=True)
srv = start_server(db, args.port, NOTES / "logs" / f"capture_{args.mode}_server.log")
try:
    with sync_playwright() as pw:
        run_info["versions"] = versions(pw)
        R = Roles(pw, BASE, NOTES / "profiles" / f"capture_{args.mode}_{int(time.time())}",
                  ["customer", "kitchen", "kitchen_bt", "shipper", "shipper2", "admin", "manager"])
        for p in R.page.values():
            p.on("dialog", lambda d: d.accept())
        for n in R.page:
            R.login(n)

        def shot(role: str, sid: str):
            pg = R.page[role]
            pg.wait_for_load_state("load")
            pg.add_style_tag(content=FIGURE_CSS)
            pg.screenshot(path=str(out_png(sid)), full_page=True)
            (TXT / f"{sid}.txt").write_text(pg.inner_text("body"), encoding="utf-8")
            measures[sid] = {"viewport": pg.viewport_size, **measure(pg)}
            print("shot", sid, pg.url)

        def nav(pg, sel, loc=False):
            with pg.expect_navigation():
                (pg.locator(sel).click() if loc else pg.click(sel))

        def go(role, path):
            R.page[role].goto(BASE + path)

        def place_order(items: dict, hub: int = 1, payment: str = "COD", address: int = 1, snap=None,
                        decline_first: bool = False):
            """Customer flow: hub menu -> quantities -> quote -> confirm. snap = dict of screen ids to shoot."""
            snap = snap or {}
            pg = R.page["customer"]
            go("customer", f"/order/hubs/{hub}")
            for item_id, q in items.items():
                pg.fill(f"input[name=qty_{item_id}]", str(q))
            pg.select_option("#address_id", str(address))
            if "menu" in snap:
                shot("customer", snap["menu"])
            nav(pg, "button:has-text('See the quote')")
            if payment != "COD":
                pg.check(f"input[name=payment][value='{payment}']")
            if "quote" in snap:
                shot("customer", snap["quote"])
            return pg

        def confirm_and_id(pg) -> int:
            nav(pg, "button:has-text('Confirm order')")
            return int(pg.inner_text("#order-id"))

        # ------------------------------------------------------------------ UC-01
        go("customer", "/order/hubs")
        shot("customer", "UC-01-S01")

        # Order A: COD at D1. Menu (S03) and quote (S04)
        pg = place_order({4: 1, 6: 1}, snap={"menu": "UC-01-S03", "quote": "UC-01-S04"})
        # S05: the admin changes a dish price after the customer opened the quote -> the quote changed
        R.page["admin"].goto(BASE + "/admin/items/4")
        R.page["admin"].fill("input[name=price]", "61000")
        nav(R.page["admin"], "button:has-text('Save dish')")
        nav(pg, "button:has-text('Confirm order')")
        shot("customer", "UC-01-S05")
        R.page["admin"].goto(BASE + "/admin/items/4")
        R.page["admin"].fill("input[name=price]", "60000")
        nav(R.page["admin"], "button:has-text('Save dish')")
        # Order A again from the menu at the restored price
        pg = place_order({4: 1, 6: 1})
        a_id = confirm_and_id(pg)
        run_info["orders"]["A_cod"] = a_id
        shot("customer", "UC-01-S08")
        nav(pg, "a:has-text('Follow this order')")
        shot("customer", "UC-01-S09")
        nav(pg, "a:has-text('Printable receipt')")
        shot("customer", "UC-01-S10")

        # Order B: ONLINE; declined first (S06 simulator, S07 declined), then approved
        pg = place_order({1: 2}, payment="ONLINE:E_WALLET")
        nav(pg, "button:has-text('Confirm order')")
        shot("customer", "UC-01-S06")
        nav(pg, "button:has-text('Decline payment')")
        shot("customer", "UC-01-S07")
        pg.check("input[name=payment][value='ONLINE:E_WALLET']")
        nav(pg, "button:has-text('Confirm order')")
        nav(pg, "button:has-text('Approve payment')")
        b_id = int(pg.inner_text("#order-id"))
        run_info["orders"]["B_online"] = b_id

        # Order C: COD, cancelled by the customer (S12)
        pg = place_order({3: 1})
        c_id = confirm_and_id(pg)
        run_info["orders"]["C_cancel"] = c_id
        go("customer", f"/order/{c_id}")
        nav(pg, "button:has-text('Cancel this order')")
        shot("customer", "UC-01-S12")

        # Busy hub (S02): the admin lowers Binh Thanh to capacity 1, one order fills it, the next is refused
        ad = R.page["admin"]
        ad.goto(BASE + "/admin/hubs/2")
        ad.fill("input[name=max_active_orders]", "1")
        nav(ad, "button:has-text('Save hub')")
        pg = place_order({4: 1}, hub=2)
        run_info["orders"]["BT_fill"] = confirm_and_id(pg)
        go("customer", "/order/hubs/2")
        pg.fill("input[name=qty_4]", "1")
        pg.select_option("#address_id", "1")
        nav(pg, "button:has-text('See the quote')")
        shot("customer", "UC-01-S02")
        ad.goto(BASE + "/admin/hubs/2")
        ad.fill("input[name=max_active_orders]", "8")
        nav(ad, "button:has-text('Save hub')")

        go("customer", "/order/mine")
        shot("customer", "UC-01-S11")

        # ------------------------------------------------------------------ UC-05
        kt = R.page["kitchen"]
        # Orders D and E are placed first (their dishes are still available); the dishes then run out
        pg = place_order({4: 1})
        d_id = confirm_and_id(pg)
        run_info["orders"]["D_decline"] = d_id
        pg = place_order({7: 2})
        e_id = confirm_and_id(pg)
        run_info["orders"]["E_withdrawn"] = e_id

        def sold_out(item_id):
            kt.goto(BASE + "/kitchen/availability")
            nav(kt, f"#item-{item_id} button")

        def offer(order_id, source_item, target_name):
            kt.goto(BASE + f"/kitchen/orders/{order_id}")
            opts = kt.eval_on_selector_all("#replacement option", "els => els.map(e => [e.value, e.textContent])")
            val = next(v for v, t in opts if target_name in t)
            kt.select_option("#replacement", val)
            nav(kt, "button:has-text('Send the offer')")

        sold_out(4)                     # Com tam suon bi cha has run out
        kt.goto(BASE + "/kitchen/")
        shot("kitchen", "UC-05-S01")
        kt.goto(BASE + f"/kitchen/orders/{a_id}")
        shot("kitchen", "UC-05-S02")
        offer(a_id, 4, "Pho ga")        # order A: Pho ga (50,000) instead
        shot("kitchen", "UC-05-S03")
        kt.goto(BASE + f"/kitchen/orders/{b_id}")
        kt.fill("#reason", "The pho broth has run out for today.")
        nav(kt, "button:has-text('Reject order')")
        shot("kitchen", "UC-05-S04")
        go("customer", "/order/mine")
        shot("customer", "UC-05-S05")
        go("customer", f"/order/{a_id}")
        shot("customer", "UC-05-S06")
        nav(pg, "button:has-text('Accept Pho ga')")
        shot("customer", "UC-05-S07")
        offer(d_id, 4, "Pho ga")        # order D: the customer declines
        go("customer", f"/order/{d_id}")
        nav(pg, "button:has-text('Decline')")
        shot("customer", "UC-05-S08")
        sold_out(7)                     # order E: Banh mi thit nuong ran out, Banh mi op la offered, then it runs out too
        offer(e_id, 7, "Banh mi op la")
        sold_out(8)
        go("customer", f"/order/{e_id}")
        nav(pg, "button:has-text('Accept Banh mi op la')")
        shot("customer", "UC-05-S09")
        for item in (4, 7, 8):          # all dishes available again
            kt.goto(BASE + "/kitchen/availability")
            nav(kt, f"#item-{item} button")

        # Kitchen moves A and E to READY (needed for UC-02)
        for oid in (a_id, e_id):
            kt.goto(BASE + f"/kitchen/orders/{oid}")
            nav(kt, "button:has-text('Confirm order')")
            nav(kt, f"#order-{oid} button:has-text('Start preparing')")
            nav(kt, f"#order-{oid} button:has-text('Mark ready')")

        # ------------------------------------------------------------------ UC-02
        s1, s2 = R.page["shipper"], R.page["shipper2"]
        s1.goto(BASE + "/delivery/")
        shot("shipper", "UC-02-S01")
        s1.goto(BASE + f"/delivery/orders/{a_id}")
        shot("shipper", "UC-02-S02")
        s2.goto(BASE + f"/delivery/orders/{a_id}")
        nav(s2, "button:has-text('Pick up this order')")
        shot("shipper2", "UC-02-S03")
        nav(s1, "button:has-text('Pick up this order')")   # stale page: the order is taken
        shot("shipper", "UC-02-S04")
        cash = vnd_int(re.search(r"Collect ([\d,]+) VND", s2.inner_text("#cash-info")).group(1))
        s2.fill("#cash", str(cash - 10000))
        nav(s2, "button:has-text('Confirm delivery')")
        shot("shipper2", "UC-02-S05")
        s2.fill("#cash", str(cash))
        nav(s2, "button:has-text('Confirm delivery')")
        shot("shipper2", "UC-02-S06")
        s1.goto(BASE + f"/delivery/orders/{e_id}")
        nav(s1, "button:has-text('Pick up this order')")
        s1.fill("#reason", "Customer did not answer the phone.")
        nav(s1, "button:has-text('Report failed delivery')")
        shot("shipper", "UC-02-S07")

        # ------------------------------------------------------------------ UC-03
        ad.goto(BASE + "/admin/hubs")
        shot("admin", "UC-03-S01")
        ad.goto(BASE + "/admin/hubs/1")
        shot("admin", "UC-03-S02")
        ad.goto(BASE + "/admin/hubs/2")
        ad.fill("input[name=max_active_orders]", "10")
        nav(ad, "button:has-text('Save hub')")
        shot("admin", "UC-03-S03")
        ad.goto(BASE + "/admin/hubs/new")
        shot("admin", "UC-03-S04")
        ad.fill("input[name=code]", "HUB-D3")
        ad.fill("input[name=name]", "SaigonBite District 3 Hub")
        ad.fill("input[name=address_text]", "88 Vo Van Tan, Ward 6, District 3, Ho Chi Minh City")
        ad.fill("input[name=latitude]", "10.7790")
        ad.fill("input[name=longitude]", "106.6860")
        ad.fill("input[name=max_active_orders]", "600")
        ad.fill("input[name=base_delivery_fee]", "12000")
        ad.evaluate("document.querySelector('input[name=max_active_orders]').removeAttribute('max')")
        nav(ad, "button:has-text('Save hub')")
        shot("admin", "UC-03-S05")
        ad.fill("input[name=max_active_orders]", "6")
        nav(ad, "button:has-text('Save hub')")
        ad.goto(BASE + "/admin/hubs")
        nav(ad, "#hub-table tr:has-text('District 3') button:has-text('Archive')")
        shot("admin", "UC-03-S06")

        # ------------------------------------------------------------------ UC-06
        ad.goto(BASE + "/admin/menu")
        shot("admin", "UC-06-S01")
        ad.fill("#new-brand", "Che Hue Corner")
        nav(ad, "button:has-text('Add brand')")
        row = ad.locator("#brand-table tr:has-text('Che Hue Corner')")
        row.locator("input[name=name]").fill("Che Hue Kitchen")
        with ad.expect_navigation():
            row.locator("button:has-text('Rename')").click()
        shot("admin", "UC-06-S02")
        ad.goto(BASE + "/admin/items/new")
        shot("admin", "UC-06-S03")
        ad.select_option("select[name=brand_id]", label="Che Hue Kitchen")
        ad.fill("input[name=name]", "Che troi nuoc")
        ad.fill("input[name=description]", "Sticky rice balls in ginger syrup")
        ad.fill("input[name=price]", "0")
        ad.evaluate("document.querySelector('input[name=price]').removeAttribute('min')")
        nav(ad, "button:has-text('Save dish')")
        shot("admin", "UC-06-S05")
        ad.fill("input[name=price]", "32000")
        nav(ad, "button:has-text('Save dish')")
        ad.goto(BASE + "/admin/items/4")
        shot("admin", "UC-06-S04")
        ad.goto(BASE + "/admin/hubs/2/menu")
        shot("admin", "UC-06-S06")
        ad.select_option("#item_id", ad.eval_on_selector_all("#item_id option", "els => els.find(e => e.textContent.includes('Che troi nuoc')).value"))
        nav(ad, "button:has-text('Add to menu')")
        nav(ad, "#listing-table tr:has-text('Che troi nuoc') button:has-text('Sold out')")
        shot("admin", "UC-06-S07")
        nav(ad, "#listing-table tr:has-text('Che troi nuoc') button:has-text('Remove from menu')")
        ad.goto(BASE + "/admin/menu")
        nav(ad, "#item-table tr:has-text('Che troi nuoc') button:has-text('Archive')")
        nav(ad, "#brand-table tr:has-text('Che Hue Kitchen') button:has-text('Archive')")
        shot("admin", "UC-06-S08")

        # ------------------------------------------------------------------ UC-04
        mg = R.page["manager"]
        mg.goto(BASE + "/reports/sales")
        shot("manager", "UC-04-S01")
        mg.goto(BASE + "/reports/workload")
        shot("manager", "UC-04-S02")
        mg.goto(BASE + "/reports/delivery")
        shot("manager", "UC-04-S03")
        mg.goto(BASE + "/reports/sales?from=2030-01-01&to=2030-01-31")
        shot("manager", "UC-04-S04")
        mg.goto(BASE + "/reports/sales?from=2026-12-31&to=2026-01-01")
        shot("manager", "UC-04-S05")

        run_info["events"] = {k: v for k, v in R.events.items() if v}
        R.close()
finally:
    stop_server(srv)
run_info["db"] = str(db)
(TXT / "measure.json").write_text(json.dumps(measures, indent=1), encoding="utf-8")
with (TXT / "measure.csv").open("w", encoding="utf-8", newline="") as f:
    import csv
    w = csv.writer(f)
    w.writerow(["screen", "viewport", "overflow", "contrast_min", "contrast_fail", "tap_small", "unlabeled", "h1", "summary"])
    for sid, m in sorted(measures.items()):
        w.writerow([sid, f"{m['viewport']['width']}x{m['viewport']['height']}", m["overflow"], m["contrast_min"],
                    len(m["contrast_fail"]), len(m["tap_small"]), len(m["unlabeled"]), m["h1"], summary(m)])
(TXT / "run.json").write_text(json.dumps(run_info, indent=1), encoding="utf-8")
print(json.dumps(run_info, indent=1))
