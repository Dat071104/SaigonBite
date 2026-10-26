"""P5.2 integration run: scenarios S1 to S8 in one sequence on one fresh demo database.

Author: 722I0004 · AI-assisted (Claude Sonnet 5.5)

Run with the tools venv:  run_integration.py [--tag NAME]
  * creates a fresh demo DB (init_db.py) and, for S7 part A, a separate oracle DB (no demo history + tests/fixtures/report_oracle.sql)
  * starts a local Flask development server on 5100 (main) and 5101 (oracle), debug off, random secret in the process environment only
  * one persistent Edge profile per role (customer, tourist, kitchen, kitchen_bt, shipper, shipper2, admin, manager)
  * every step: screenshot S<n>/S<n>_<step>_<role>.png, the expected sentence (copied from S<n>/expected.md), the checks, the actual
    page text, pass/fail, order id, and the console / HTTP >= 400 events the step produced
  * writes results.json, S<n>/db_facts.json (read-only corroboration), forms_seen.json (every POST form seen: CSRF token present?)
The expected results were written and hashed before this script ran (S<n>/expected.md); nothing here edits them.
"""
import argparse
import json
import re
import shutil
import sqlite3
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
EVID = HERE.parent
REPO = EVID.parents[3]
sys.path.insert(0, str(HERE))
from p5lib import NOTES, REPO_PY, ROLES, Roles, db_rows, new_db, start_server, stop_server, versions  # noqa: E402
from playwright.sync_api import sync_playwright  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--tag", default=datetime.now().strftime("%H%M%S"))
args = ap.parse_args()
TS = args.tag
MAIN, ORACLE = "http://127.0.0.1:5100", "http://127.0.0.1:5101"
FIGURE_CSS = ".summary-bar{position:static !important}"

main_db = new_db(NOTES / "db" / f"main_{TS}.db", demo=True)
oracle_db = new_db(NOTES / "db" / f"oracle_{TS}.db", demo=False)
conn = sqlite3.connect(oracle_db)
conn.executescript((REPO / "tests" / "fixtures" / "report_oracle.sql").read_text(encoding="utf-8"))
conn.commit()
conn.close()

RESULTS, FORMS = [], []
CURRENT = {"S": None}
STEP_EVENTS = {}


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s or "").strip()


def text(pg, sel="main") -> str:
    return norm(pg.inner_text(sel))


def cells(pg, sel) -> list[str]:
    return [norm(c) for c in pg.locator(sel).all_inner_texts()]


class Run:
    def __init__(self, pw):
        self.pw = pw
        self.R = Roles(pw, MAIN, NOTES / "profiles" / f"main_{TS}", list(ROLES))
        self.RO = Roles(pw, ORACLE, NOTES / "profiles" / f"oracle_{TS}", ["manager"])
        for roles in (self.R, self.RO):
            for n, p in roles.page.items():
                p.on("dialog", lambda d: d.accept())
                p.on("load", lambda _page, n=n, p=p: self.scan_forms(n, p))
        self.evcount = {}

    def scan_forms(self, role, pg):
        try:
            forms = pg.evaluate("""() => Array.from(document.querySelectorAll('form')).filter(f => f.method.toLowerCase() === 'post')
                .map(f => ({action: f.getAttribute('action') || '', token: ((f.querySelector('input[name=csrf_token]') || {}).value || '').length}))""")
            for f in forms:
                FORMS.append({"role": role, "url": pg.url.split("?")[0], "action": f["action"], "token_len": f["token"]})
        except Exception:
            pass

    def events_since(self, roles_obj, role):
        ev = roles_obj.events[role]
        n = self.evcount.get((id(roles_obj), role), 0)
        self.evcount[(id(roles_obj), role)] = len(ev)
        return ev[n:]


def shot(roles_obj, role, name, folder):
    pg = roles_obj.page[role]
    pg.add_style_tag(content=FIGURE_CSS)
    path = EVID / folder / name
    pg.screenshot(path=str(path), full_page=True)
    return name


def step(run, sc, sid, role, action, expected, checks, roles_obj=None, pg_text="", order=None, extra=None, shots=None):
    """Record one step. checks = [(label, bool)]. The step passes when every check is true."""
    roles_obj = roles_obj or run.R
    names = shots or [f"{sc}_{sid}_{role}.png"]
    shot_names = []
    for nm in names:
        if isinstance(nm, tuple):
            r_obj, rl, fname = nm
            shot_names.append(shot(r_obj, rl, fname, sc))
        else:
            base = role if role in roles_obj.page else (role.split("+")[0] if role.split("+")[0] in roles_obj.page else "admin")
            shot_names.append(shot(roles_obj, base, nm, sc))
    failed = [lbl for lbl, ok in checks if not ok]
    ev = []
    for r_obj in (run.R, run.RO):
        for rl in r_obj.events:
            ev += [f"{rl}: {k} {v}" for k, v in run.events_since(r_obj, rl)]
    rec = {"scenario": sc, "step": sid, "role": role, "action": action, "expected": expected,
           "checks": [{"check": lbl, "ok": bool(ok)} for lbl, ok in checks], "result": "PASS" if not failed else "FAIL",
           "failed_checks": failed, "actual": pg_text[:700], "screenshots": shot_names, "order": order, "events": ev, "extra": extra or {}}
    RESULTS.append(rec)
    print(f"{sc} {sid} {role}: {rec['result']}" + (f"  FAILED: {failed}" if failed else ""))
    return rec


def nav(pg, sel):
    with pg.expect_navigation() as info:
        pg.click(sel)
    return info.value


def goto(pg, url):
    return pg.goto(url)


def facts(sc, queries: dict, db=main_db):
    out = {k: db_rows(db, q) for k, q in queries.items()}
    (EVID / sc / "db_facts.json").write_text(json.dumps(out, indent=1, default=str), encoding="utf-8")
    return out


def place(run, role, hub, items: dict, address, payment=None):
    pg = run.R.page[role]
    goto(pg, f"{MAIN}/order/hubs/{hub}")
    for i, q in items.items():
        pg.fill(f"input[name=qty_{i}]", str(q))
    pg.select_option("#address_id", str(address))
    resp = nav(pg, "button:has-text('See the quote')")
    if payment:
        pg.check(f"input[name=payment][value='{payment}']")
    return pg, resp


def has(t, *parts):
    return [(f"text contains: {p}", p in t) for p in parts]


def row_cells(pg, sel):
    return [norm(x) for x in pg.locator(f"{sel} td").all_inner_texts()]


def run_all(pw):
    run = Run(pw)
    R, RO = run.R, run.RO
    for n in R.page:
        R.login(n)
    RO.login("manager")
    P = R.page
    env = {"commit": subprocess.run(["git", "rev-parse", "HEAD"], cwd=str(REPO), capture_output=True, text=True).stdout.strip(),
           "git_status": subprocess.run(["git", "status", "--short"], cwd=str(REPO), capture_output=True, text=True).stdout.strip().splitlines(),
           "versions": versions(pw), "main_db": str(main_db), "oracle_db": str(oracle_db),
           "server": "local Flask development server (python -m flask run), debug off, ports 5100 (main) and 5101 (oracle)",
           "started": datetime.now().isoformat(timespec="seconds")}

    # ======================================================================= S1
    sc = "S1"
    P["admin"].goto(f"{MAIN}/admin/hubs")
    t = text(P["admin"])
    step(run, sc, "1.1", "admin", "open Hubs", "HUB-D1 shows 1 / 12 Quiet; HUB-BT shows 0 / 8 Quiet",
         has(t, "Hubs and kitchen capacity") + [("D1 row 1 / 12", "1 / 12" in text(P["admin"], "#hub-1")), ("D1 quiet", "Quiet" in text(P["admin"], "#hub-1")),
          ("BT row 0 / 8", "0 / 8" in text(P["admin"], "#hub-2")), ("BT quiet", "Quiet" in text(P["admin"], "#hub-2"))], pg_text=t)
    ad = P["admin"]
    goto(ad, f"{MAIN}/admin/hubs/1")
    ad.fill("input[name=max_active_orders]", "14")
    nav(ad, "button:has-text('Save hub')")
    t = text(ad)
    step(run, sc, "1.2", "admin", "Edit D1, capacity 14, Save hub", "banner 'The hub is saved.'; D1 row 1 / 14",
         has(t, "The hub is saved.") + [("D1 row 1 / 14", "1 / 14" in text(ad, "#hub-1"))], pg_text=t)
    goto(ad, f"{MAIN}/admin/hubs/1/menu")
    ad.select_option("#item_id", ad.eval_on_selector_all("#item_id option", "els => els.find(e => e.textContent.includes('Che thai')).value"))
    nav(ad, "button:has-text('Add to menu')")
    t = text(ad)
    row = text(ad, "#listed-9")
    step(run, sc, "1.3", "admin", "D1 menu: add Sweet Che House: Che thai, Available", "banner 'The dish is on the hub's menu.'; row Che thai Sweet Che House 30,000 VND Available",
         has(t, "The dish is on the hub's menu.") + [(f"row has {x}", x in row) for x in ("Che thai", "Sweet Che House", "30,000 VND", "Available")], pg_text=t + " || " + row)
    cu = P["customer"]
    goto(cu, f"{MAIN}/order/hubs")
    nav(cu, "a[aria-label='Order from SaigonBite District 1 Hub']")
    t = text(cu)
    step(run, sc, "1.4", "customer", "D1 menu", "Sweet Che House / Che thai 30,000 VND with a quantity field; Com tam ga nuong Sold out without a field",
         has(t, "Sweet Che House", "Che thai", "30,000 VND", "Com tam ga nuong", "Sold out") +
         [("qty field for Che thai", cu.locator("input[name=qty_9]").count() == 1), ("no qty field for sold-out dish 5", cu.locator("input[name=qty_5]").count() == 0)], pg_text=t)
    goto(ad, f"{MAIN}/admin/menu")
    nav(ad, "#item-8 button:has-text('Archive')")
    t = text(ad)
    step(run, sc, "1.5", "admin", "archive the dish Banh mi op la", "banner 'The dish is archived. It can no longer be ordered.'; row shows Archived",
         has(t, "The dish is archived. It can no longer be ordered.") + [("row Archived", "Archived" in text(ad, "#item-8"))], pg_text=t)
    goto(cu, f"{MAIN}/order/hubs/1")
    t = text(cu)
    step(run, sc, "1.6", "customer", "reload the D1 menu", "Banh mi op la is not on the page",
         [("Banh mi op la absent", "Banh mi op la" not in t), ("no qty_8 field", cu.locator("input[name=qty_8]").count() == 0)], pg_text=t)
    for sid, item, label in (("1.7", 5, "sold-out dish"), ("1.8", 8, "archived dish")):
        goto(cu, f"{MAIN}/order/hubs/1")
        cu.evaluate("(n) => { const f = document.querySelector('form[data-menu-form]'); const i = document.createElement('input'); i.type = 'hidden'; i.name = 'qty_' + n; i.value = '1'; f.appendChild(i); }", item)
        cu.select_option("#address_id", "1")
        resp = nav(cu, "button:has-text('See the quote')")
        t = text(cu)
        step(run, sc, sid, "customer", f"post qty_{item} = 1 ({label}) by script", f"HTTP 400 on the menu page, 'Item {item} is not available at SaigonBite District 1 Hub.', no quote",
             [("HTTP 400", resp.status == 400), (f"message item {item}", f"Item {item} is not available at SaigonBite District 1 Hub." in t),
              ("no quote table", cu.locator("#quote-table").count() == 0)], pg_text=t, extra={"status": resp.status})
    pg, _ = place(run, "customer", 1, {9: 1}, 1)
    qt = text(pg)
    ok1 = has(qt, "Dishes 30,000 VND", "Delivery fee (0.39 km) 15,000 VND", "Quiet hub discount -5,000 VND", "Total 40,000 VND")
    nav(pg, "button:has-text('Confirm order')")
    t = text(pg)
    step(run, sc, "1.9", "customer", "order 1 x Che thai COD at D1", "quote 30,000 + 15,000 - 5,000 = 40,000; 'Order 9 is placed', 40,000 VND, PLACED",
         ok1 + has(t, "Order 9 is placed", "40,000 VND") + [("state PLACED", "PLACED" in text(pg, "#order-state"))], pg_text=qt + " || " + t, order=9,
         shots=["S1_1.9_customer.png"])
    facts(sc, {"orders": "select id,hub_id,state,total_amount from orders order by id",
               "lines_after_8": "select order_id,menu_item_id,item_name,quantity from order_line where order_id>8"})

    # ======================================================================= S2
    sc = "S2"
    goto(ad, f"{MAIN}/admin/hubs/2")
    ad.fill("input[name=max_active_orders]", "1")
    nav(ad, "button:has-text('Save hub')")
    t = text(ad)
    step(run, sc, "2.1", "admin", "Edit BT capacity 1", "banner 'The hub is saved.'; BT row 0 / 1",
         has(t, "The hub is saved.") + [("BT 0 / 1", "0 / 1" in text(ad, "#hub-2"))], pg_text=t)
    pg, _ = place(run, "customer", 2, {4: 1}, 1)
    qt = text(pg)
    ok2 = has(qt, "Dishes 60,000 VND", "Delivery fee (4.06 km) 25,000 VND", "Quiet hub discount -5,000 VND", "Total 80,000 VND")
    nav(pg, "button:has-text('Confirm order')")
    t = text(pg)
    step(run, sc, "2.2", "customer", "order 1 x Com tam suon bi cha at BT", "quote 60,000 + 25,000 - 5,000 = 80,000; 'Order 10 is placed'",
         ok2 + has(t, "Order 10 is placed", "80,000 VND"), pg_text=qt + " || " + t, order=10)
    goto(ad, f"{MAIN}/admin/hubs")
    t = text(ad, "#hub-2")
    step(run, sc, "2.3", "admin", "open Hubs", "BT shows 1 / 1 and Busy", [("1 / 1", "1 / 1" in t), ("Busy", "Busy" in t)], pg_text=t)
    tr = P["tourist"]
    goto(tr, f"{MAIN}/order/hubs/2")
    tr.fill("input[name=qty_4]", "1")
    tr.select_option("#address_id", "3")
    resp = nav(tr, "button:has-text('See the quote')")
    t = text(tr)
    step(run, sc, "2.4", "tourist", "order at the full BT hub", "HTTP 409; 'too busy' banner; suggestion D1 with 'Quiet: 5,000 VND off delivery'; BT card 'Busy now'; no quote",
         [("HTTP 409", resp.status == 409)] + has(t, "SaigonBite Binh Thanh Hub is too busy to take new orders right now.", "These hubs can take your order now", "Busy now") +
         [("suggestion D1", "SaigonBite District 1 Hub" in text(tr, "#suggestions")), ("quiet note", "Quiet: 5,000 VND off delivery" in text(tr, "#suggestions")),
          ("no quote", tr.locator("#quote-table").count() == 0)], pg_text=t, extra={"status": resp.status})
    nav(tr, "#suggestions a")
    tr.fill("input[name=qty_1]", "1")
    tr.select_option("#address_id", "3")
    nav(tr, "button:has-text('See the quote')")
    t = text(tr)
    step(run, sc, "2.5", "tourist", "follow the suggestion, fresh quote at D1", "D1 quote: 55,000 + 15,000 - 5,000 = 65,000",
         has(t, "SaigonBite District 1 Hub", "Dishes 55,000 VND", "Delivery fee (0.06 km) 15,000 VND", "Quiet hub discount -5,000 VND", "Total 65,000 VND"), pg_text=t)
    f = facts(sc, {"orders": "select id,customer_id,hub_id,state,total_amount from orders order by id", "payments": "select order_id,method,state,amount from payment order by order_id",
                   "lines": "select count(*) n from order_line"})
    step(run, sc, "2.6", "tourist", "leave without confirming (database check)", "still 10 orders and 10 payment rows; nothing from steps 2.4 and 2.5",
         [("10 orders", len(f["orders"]) == 10), ("10 payments", len(f["payments"]) == 10)], pg_text=json.dumps(f["orders"]), shots=[f"S2_2.6_tourist.png"])
    goto(ad, f"{MAIN}/admin/hubs/2")
    ad.fill("input[name=max_active_orders]", "8")
    nav(ad, "button:has-text('Save hub')")
    t = text(ad)
    step(run, sc, "2.7", "admin", "restore BT capacity 8", "banner 'The hub is saved.'; BT 1 / 8", has(t, "The hub is saved.") + [("BT 1 / 8", "1 / 8" in text(ad, "#hub-2"))], pg_text=t)

    # ======================================================================= S3
    sc = "S3"
    pg, _ = place(run, "customer", 1, {2: 2}, 1)
    qt = text(pg)
    ok3 = has(qt, "Dishes 100,000 VND", "Delivery fee (0.39 km) 15,000 VND", "Quiet hub discount -5,000 VND", "Total 110,000 VND")
    nav(pg, "button:has-text('Confirm order')")
    t = text(pg)
    step(run, sc, "3.1", "customer", "order 2 x Pho ga at D1", "quote 100,000 + 15,000 - 5,000 = 110,000; 'Order 11 is placed'",
         ok3 + has(t, "Order 11 is placed", "110,000 VND") + [("PLACED", "PLACED" in text(pg, "#order-state"))], pg_text=qt + " || " + t, order=11)
    kt, kb = P["kitchen"], P["kitchen_bt"]
    goto(kt, f"{MAIN}/kitchen/")
    t = text(kt)
    step(run, sc, "3.2", "kitchen", "D1 Kitchen board", "heading D1; card Order 11 in New with 2 x Pho ga and Confirm; New shows 3",
         has(t, "SaigonBite District 1 Hub") + [("card Order 11", kt.locator("#order-11").count() == 1), ("2 x Pho ga", "2 x Pho ga" in text(kt, "#order-11")),
          ("Confirm button", kt.locator("#order-11 button:has-text('Confirm')").count() == 1), ("New 3", "New 3" in text(kt, "#col-PLACED"))], pg_text=t, order=11)
    goto(kb, f"{MAIN}/kitchen/")
    t = text(kb)
    step(run, sc, "3.3", "kitchen_bt", "BT Kitchen board", "heading BT; card Order 10; no Order 11",
         has(t, "SaigonBite Binh Thanh Hub") + [("card Order 10", kb.locator("#order-10").count() == 1), ("no card 11", kb.locator("#order-11").count() == 0), ("no text Order 11", "Order 11" not in t)], pg_text=t)
    resp = goto(kb, f"{MAIN}/kitchen/orders/11")
    t = text(kb)
    step(run, sc, "3.4", "kitchen_bt", "type /kitchen/orders/11", "HTTP 403 Not allowed, 'This order belongs to another hub.'",
         [("HTTP 403", resp.status == 403)] + has(t, "Not allowed", "This order belongs to another hub."), pg_text=t, order=11, extra={"status": resp.status})
    kb.evaluate("""() => { const tok = document.querySelector('input[name=csrf_token]').value; const f = document.createElement('form'); f.method = 'post';
        f.action = '/kitchen/orders/11/confirm'; const i = document.createElement('input'); i.type = 'hidden'; i.name = 'csrf_token'; i.value = tok; f.appendChild(i);
        document.body.appendChild(f); }""")
    with kb.expect_navigation() as info:
        kb.evaluate("document.body.lastElementChild.submit()")
    resp = info.value
    t = text(kb)
    d = db_rows(main_db, "select state,confirmed_at from orders where id=11")[0]
    step(run, sc, "3.5", "kitchen_bt", "post Confirm for order 11 from the BT session", "HTTP 403, 'This order belongs to another hub.'; order 11 stays PLACED, confirmed_at empty",
         [("HTTP 403", resp.status == 403)] + has(t, "This order belongs to another hub.") + [("PLACED", d["state"] == "PLACED"), ("not confirmed", d["confirmed_at"] is None)],
         pg_text=t, order=11, extra={"status": resp.status, "db": d})
    goto(kt, f"{MAIN}/kitchen/orders/11")
    t = text(kt)
    step(run, sc, "3.6", "kitchen", "open Order 11", "2 x Pho ga, Total 110,000, Placed, Confirm order and Reject order buttons and the Offer a replacement section",
         has(t, "Pho ga", "110,000 VND", "Placed") + [("Confirm order button", kt.locator("button:has-text('Confirm order')").count() == 1),
          ("Reject order button", kt.locator("button:has-text('Reject order')").count() == 1), ("Offer a replacement section", "Offer a replacement" in t)], pg_text=t, order=11)
    facts(sc, {"order11": "select id,hub_id,state,confirmed_at,total_amount from orders where id=11"})

    # ======================================================================= S4
    sc = "S4"
    goto(kt, f"{MAIN}/kitchen/availability")
    nav(kt, "#item-2 button:has-text('Mark sold out')")
    t = text(kt)
    step(run, sc, "4.1", "kitchen", "mark Pho ga sold out", "banner 'Availability updated.'; Pho ga Sold out with 'Available again'",
         has(t, "Availability updated.") + [("row Sold out", "Sold out" in text(kt, "#item-2")), ("Available again", "Available again" in text(kt, "#item-2"))], pg_text=t)
    goto(kt, f"{MAIN}/kitchen/orders/11")
    val = kt.eval_on_selector_all("#replacement option", "els => (els.find(e => e.textContent.includes('Pho ga') && e.textContent.includes('Goi cuon')) || {}).value")
    kt.select_option("#replacement", val)
    nav(kt, "button:has-text('Send the offer')")
    t = text(kt)
    step(run, sc, "4.2", "kitchen", "offer Pho ga -> Goi cuon (35,000 VND)", "banner 'The replacement is offered...'; 'Replacement offered: Pho ga → Goi cuon'; no Confirm button",
         has(t, "The replacement is offered. The order waits for the customer's answer.", "Replacement offered: Pho ga → Goi cuon", "Waiting for the customer") +
         [("no Confirm order button", kt.locator("button:has-text('Confirm order')").count() == 0)], pg_text=t, order=11)
    goto(cu, f"{MAIN}/order/mine")
    tm = text(cu)
    goto(cu, f"{MAIN}/order/11")
    t = text(cu)
    step(run, sc, "4.3", "customer", "My orders, then Order 11", "'Your answer needed'; panel: Pho ga has run out... Goi cuon at 35,000 VND instead of 50,000 VND; new total 80,000 VND (now 110,000 VND)",
         [("My orders shows Your answer needed", "Your answer needed" in tm)] +
         has(t, "The kitchen asks about a replacement", "Pho ga has run out. The kitchen offers Goi cuon at 35,000 VND instead of 50,000 VND.", "the new total is 80,000 VND (now 110,000 VND)"),
         pg_text=t, order=11)
    nav(cu, "button:has-text('Accept Goi cuon')")
    t = text(cu)
    step(run, sc, "4.4", "customer", "Accept Goi cuon", "banner 'Replacement accepted...'; Goi cuon 2 x 35,000 = 70,000; Total 80,000; panel gone",
         has(t, "Replacement accepted. The kitchen may now confirm your order.", "Goi cuon", "70,000 VND", "Total 80,000 VND") + [("panel gone", "The kitchen asks about a replacement" not in t)], pg_text=t, order=11)
    goto(kt, f"{MAIN}/kitchen/orders/11")
    nav(kt, "button:has-text('Confirm order')")
    t1 = text(kt)
    nav(kt, "#order-11 button:has-text('Start preparing')")
    t2 = text(kt)
    nav(kt, "#order-11 button:has-text('Mark ready')")
    t3 = text(kt)
    step(run, sc, "4.5", "kitchen", "Confirm order, Start preparing, Mark ready", "three banners; Order 11 under Ready for pickup",
         has(t1, "Order 11 is confirmed.") + has(t2, "Order 11 is being prepared.") + has(t3, "Order 11 is ready. Shippers can now pick it up.") +
         [("in Ready column", kt.locator("section:has(#col-READY) #order-11").count() == 1)], pg_text=t1 + " | " + t2 + " | " + t3, order=11)
    goto(cu, f"{MAIN}/order/11")
    t = text(cu)
    step(run, sc, "4.6", "customer", "open Order 11", "Status Ready", [("Ready badge", text(cu, "#order-state") == "Ready")], pg_text=t, order=11)
    goto(kt, f"{MAIN}/kitchen/availability")
    nav(kt, "#item-2 button:has-text('Available again')")
    t = text(kt)
    step(run, sc, "4.7", "kitchen", "Pho ga available again", "banner 'Availability updated.'; Pho ga Available",
         has(t, "Availability updated.") + [("row Available", "Available" in text(kt, "#item-2") and "Sold out" not in text(kt, "#item-2"))], pg_text=t)
    f = facts(sc, {"order11": "select id,state,total_amount from orders where id=11", "delivery": "select order_id,state,shipper_id from delivery where order_id=11",
                   "offers": "select id,order_id,state from replacement_offer where order_id=11"})
    RESULTS[-1]["extra"]["db_checks"] = {"one delivery row for order 11": len(f["delivery"]) == 1 and f["delivery"][0]["state"] == "AWAITING_PICKUP", "offer ACCEPTED": f["offers"][0]["state"] == "ACCEPTED"}
    if not all(RESULTS[-1]["extra"]["db_checks"].values()):
        RESULTS[-1]["result"] = "FAIL"
        RESULTS[-1]["failed_checks"].append("db corroboration: delivery/offer")

    # ======================================================================= S5
    sc = "S5"
    s1, s2 = P["shipper"], P["shipper2"]
    for p in (s1, s2):
        goto(p, f"{MAIN}/delivery/")
    t1, t2 = text(s1), text(s2)
    step(run, sc, "5.1", "shipper", "open Deliveries (both shippers)", "Order 11 under Ready for pickup with 'Cash on delivery: 80,000 VND'; also Order 7 (65,000 VND)",
         [("shipper sees Order 11 80,000", "Order 11" in text(s1, "#waiting-11") and "80,000 VND" in text(s1, "#waiting-11")),
          ("shipper2 sees Order 11 80,000", "Order 11" in text(s2, "#waiting-11") and "80,000 VND" in text(s2, "#waiting-11")),
          ("Order 7 65,000", "65,000 VND" in text(s1, "#waiting-7"))], pg_text=t1, order=11, shots=["S5_5.1_shipper.png", (R, "shipper2", "S5_5.1_shipper2.png")])
    for p in (s1, s2):
        goto(p, f"{MAIN}/delivery/orders/11")
    t0 = time.time()
    with s1.expect_navigation() as n1, s2.expect_navigation() as n2:
        s1.evaluate("document.querySelector(\"form[action$='/orders/11/pickup']\").requestSubmit()")
        d1 = time.time() - t0
        s2.evaluate("document.querySelector(\"form[action$='/orders/11/pickup']\").requestSubmit()")
        d2 = time.time() - t0
    ta, tb = text(s1), text(s2)
    won1, won2 = "You picked up order 11." in ta, "You picked up order 11." in tb
    winner, loser = ("shipper", "shipper2") if won1 else ("shipper2", "shipper")
    wp, lp = P[winner], P[loser]
    lt = text(lp)
    drow = db_rows(main_db, "select shipper_id,state from delivery where order_id=11")[0]
    step(run, sc, "5.2", "shipper+shipper2", "press Pick up this order in both profiles together", "exactly one winner 'You picked up order 11.' + Picked up; the other 'Order 11 has already been picked up. Nothing was changed.' and 'Back to deliveries'",
         [("exactly one winner", won1 != won2), ("winner badge Picked up", "Picked up" in text(wp, "#delivery-state") if (won1 != won2) else False),
          ("loser banner", "Order 11 has already been picked up. Nothing was changed." in lt), ("loser has Back to deliveries", "Back to deliveries" in lt),
          ("one shipper on the delivery", drow["state"] == "PICKED_UP" and drow["shipper_id"] in (3, 8))],
         pg_text=f"winner={winner}: {text(wp)} || loser={loser}: {lt}", order=11, extra={"winner": winner, "loser": loser, "dispatch_ms": [round(d1 * 1000), round(d2 * 1000)], "delivery_row": drow},
         shots=[(R, winner, f"S5_5.2_{winner}_winner.png"), (R, loser, f"S5_5.2_{loser}_loser.png")])
    wp.fill("#cash", "79000")
    nav(wp, "button:has-text('Confirm delivery')")
    t = text(wp)
    step(run, sc, "5.3", winner, "enter 79,000 as cash", "refused: 'Collect exactly 80,000 VND in cash and enter that amount.'; still Picked up",
         has(t, "Collect exactly 80,000 VND in cash and enter that amount.") + [("still Picked up", "Picked up" in text(wp, "#delivery-state"))], pg_text=t, order=11)
    wp.fill("#cash", "80000")
    nav(wp, "button:has-text('Confirm delivery')")
    t = text(wp)
    step(run, sc, "5.4", winner, "enter 80,000", "banner 'Order 11 is delivered.'; Delivered; Cash collected 80,000 VND",
         has(t, "Order 11 is delivered.", "Cash collected", "80,000 VND") + [("badge Delivered", "Delivered" in text(wp, "#delivery-state"))], pg_text=t, order=11)
    goto(cu, f"{MAIN}/order/11")
    to = text(cu)
    goto(cu, f"{MAIN}/order/11/receipt")
    tr_ = text(cu)
    step(run, sc, "5.5", "customer", "open Order 11 and its receipt", "Delivered; payment 'COD, paid'; receipt PAID, 80,000 VND, Total T 80,000 VND, Refund owed 0 VND",
         [("Delivered", True)] + has(to, "Delivered", "COD, paid") + has(tr_, "Payment state PAID", "Payment amount 80,000 VND", "Total T 80,000 VND", "Refund owed, payout pending 0 VND"),
         pg_text=to + " || " + tr_, order=11, shots=["S5_5.5_customer_receipt.png"])
    facts(sc, {"delivery": "select order_id,state,shipper_id,cash_collected from delivery where order_id=11", "payment": "select order_id,method,state,amount from payment where order_id=11",
               "order": "select id,state from orders where id=11"})

    # ======================================================================= S6
    sc = "S6"
    pg, _ = place(run, "customer", 1, {6: 1}, 1)
    pg.check("input[name=payment][value='ONLINE:E_WALLET']")
    nav(pg, "button:has-text('Confirm order')")
    t = text(pg)
    step(run, sc, "6a.1", "customer", "order 1 x Tra da, pay online E-wallet, Confirm order", "next screen is the Payment simulator: Amount 20,000 VND, Method E-wallet; no 'price changed' notice",
         has(t, "Payment simulator", "Amount: 20,000 VND", "Method: E-wallet") + [("no false notice", "The price changed" not in t)], pg_text=t)
    resp = nav(pg, "button:has-text('Decline payment')")
    t = text(pg)
    step(run, sc, "6a.2", "customer", "Decline payment", "HTTP 402 quote page 'The payment was declined. No order was placed. Try again or choose cash on delivery.'",
         [("HTTP 402", resp.status == 402)] + has(t, "The payment was declined. No order was placed. Try again or choose cash on delivery."), pg_text=t, extra={"status": resp.status})
    f = facts(sc, {"orders": "select id from orders", "payments": "select order_id from payment"})
    step(run, sc, "6a.3", "customer", "database check", "11 orders and 11 payment rows; no order 12", [("11 orders", len(f["orders"]) == 11), ("11 payments", len(f["payments"]) == 11)],
         pg_text=f"orders={len(f['orders'])} payments={len(f['payments'])}", shots=["S6_6a.3_customer.png"])
    pg, _ = place(run, "customer", 1, {1: 1}, 1, payment="ONLINE:E_WALLET")
    nav(pg, "button:has-text('Confirm order')")
    nav(pg, "button:has-text('Approve payment')")
    t = text(pg)
    step(run, sc, "6b.1", "customer", "order 1 x Pho bo tai online E-wallet, Approve payment", "'Order 12 is placed', 65,000 VND, ONLINE PAID, 'You paid online'",
         has(t, "Order 12 is placed", "65,000 VND", "You paid online") + [("ONLINE", text(pg, "#payment-method") == "ONLINE"), ("PAID", text(pg, "#payment-state") == "PAID")], pg_text=t, order=12)
    goto(kt, f"{MAIN}/kitchen/orders/12")
    kt.fill("#reason", "The beef has run out for today.")
    nav(kt, "button:has-text('Reject order')")
    t = text(kt)
    step(run, sc, "6b.2", "kitchen", "reject Order 12 with a reason", "banner 'Order 12 is rejected and the customer is told why.'", has(t, "Order 12 is rejected and the customer is told why."), pg_text=t, order=12)
    goto(cu, f"{MAIN}/order/12")
    to = text(cu)
    goto(cu, f"{MAIN}/order/12/receipt")
    tr_ = text(cu)
    detail_ok = "refund owed" in to.lower()
    step(run, sc, "6b.3", "customer", "open Order 12 and its receipt", "Rejected + reason; payment refund pending with 65,000 VND named as a refund owed (payout pending), never refunded; receipt: captured C 65,000, REFUND_PENDING, Refund owed 65,000",
         has(to, "Rejected", "The beef has run out for today.", "refund pending", "65,000 VND") + [("order page names it a refund owed", detail_ok)] +
         has(tr_, "captured C 65,000 VND", "Payment state REFUND_PENDING", "Refund owed, payout pending 65,000 VND") +
         [("no 'Refunded' state", not re.search(r"(?<!to be )\brefunded\b", to + " " + tr_, re.I))], pg_text=to + " || " + tr_, order=12, shots=["S6_6b.3_customer_receipt.png"])
    pg, _ = place(run, "customer", 1, {6: 1}, 1)
    nav(pg, "button:has-text('Confirm order')")
    t = text(pg)
    step(run, sc, "6c.1", "customer", "order 1 x Tra da COD", "'Order 13 is placed', 20,000 VND", has(t, "Order 13 is placed", "20,000 VND"), pg_text=t, order=13)
    goto(cu, f"{MAIN}/order/13")
    nav(cu, "button:has-text('Cancel this order')")
    t = text(cu)
    step(run, sc, "6c.2", "customer", "Cancel this order (confirmation accepted)", "banner 'Order 13 is cancelled.'; Cancelled; payment 'COD, voided'",
         has(t, "Order 13 is cancelled.", "COD, voided") + [("Cancelled badge", text(cu, "#order-state") == "Cancelled")], pg_text=t, order=13)
    goto(kt, f"{MAIN}/kitchen/")
    t = text(kt)
    step(run, sc, "6c.3", "kitchen", "open the Kitchen board", "no card for Order 13", [("no card 13", kt.locator("#order-13").count() == 0)], pg_text=t, order=13)
    goto(s1, f"{MAIN}/delivery/")
    nav(s1, "#waiting-7 button:has-text('Pick up this order')")
    t = text(s1)
    step(run, sc, "6d.1", "shipper", "pick up demo Order 7", "banner 'You picked up order 7.'; Picked up",
         has(t, "You picked up order 7.") + [("badge", "Picked up" in text(s1, "#delivery-state"))], pg_text=t, order=7)
    s1.fill("#reason", "Customer did not answer the phone.")
    nav(s1, "button:has-text('Report failed delivery')")
    t = text(s1)
    step(run, sc, "6d.2", "shipper", "Report failed delivery with a reason", "banner 'The failed delivery of order 7 is recorded. Bring the food back to the hub.'; Failed; Problem shows the reason",
         has(t, "The failed delivery of order 7 is recorded. Bring the food back to the hub.", "Customer did not answer the phone.") + [("badge Failed", "Failed" in text(s1, "#delivery-state"))], pg_text=t, order=7)
    goto(cu, f"{MAIN}/order/7")
    t = text(cu)
    step(run, sc, "6d.3", "customer", "open Order 7", "Delivery failed; Delivery problem shows the reason; payment 'COD, voided'",
         has(t, "Delivery problem", "Customer did not answer the phone.", "COD, voided") + [("state", text(cu, "#order-state") == "Delivery failed")], pg_text=t, order=7)
    facts(sc, {"orders": "select id,state,total_amount from orders where id in (7,12,13) order by id", "payments": "select order_id,method,state,amount,refund_amount from payment where order_id in (7,12,13) order by order_id",
               "delivery7": "select order_id,state,failure_reason from delivery where order_id=7", "count": "select count(*) n from orders"})

    # ======================================================================= S7
    sc = "S7"
    mo = RO.page["manager"]
    goto(mo, f"{ORACLE}/reports/sales")
    mo.fill("#from", "2026-10-20")
    mo.fill("#to", "2026-10-20")
    mo.select_option("#hub", "")
    nav(mo, "button:has-text('Show')")
    rows = [row_cells(mo, f"#sales-table tbody tr:nth-child({i})") for i in (1, 2, 3)]
    tot = row_cells(mo, "#sales-total")
    top = [row_cells(mo, f"#top-items tbody tr:nth-child({i})") for i in (1, 2)]
    t = text(mo)
    def has_row(cells_, label_part, nums):
        return label_part in cells_[0] and cells_[1:] == nums
    names = [r[0] for r in rows if r]
    d1r = next((r for r in rows if r and "District 1" in r[0]), [])
    btr = next((r for r in rows if r and "Binh Thanh" in r[0]), [])
    step(run, sc, "7.1", "manager", "Sales 2026-10-20, all hubs (oracle DB)", "D1 1/90,000/-10,000/10,000/90,000/10,000/90,000; BT 1/60,000/0/10,000/70,000/0/70,000; All 2/150,000/-10,000/20,000/160,000/10,000/160,000; top items 3 & 1",
         [("District 1 row", d1r[1:] == ["1", "90,000 VND", "-10,000 VND", "10,000 VND", "90,000 VND", "10,000 VND", "90,000 VND"]),
          ("Binh Thanh row", btr[1:] == ["1", "60,000 VND", "0 VND", "10,000 VND", "70,000 VND", "0 VND", "70,000 VND"]),
          ("All hubs row", tot[1:] == ["2", "150,000 VND", "-10,000 VND", "20,000 VND", "160,000 VND", "10,000 VND", "160,000 VND"]),
          ("top item 1", top[0] == ["Renamed snapshot", "3", "100,000 VND"]), ("top item 2", top[1] == ["Shared name", "1", "50,000 VND"])],
         roles_obj=RO, pg_text=json.dumps({"rows": rows, "total": tot, "top": top}), extra={"rows": rows, "total": tot, "top": top})
    mo.select_option("#hub", "2")
    nav(mo, "button:has-text('Show')")
    tot2 = row_cells(mo, "#sales-total")
    t = text(mo)
    step(run, sc, "7.2", "manager", "same period, hub = Binh Thanh", "1 order, total 70,000 VND, refunds owed 0, net 70,000",
         [("total row", tot2[1] == "1" and tot2[5] == "70,000 VND" and tot2[6] == "0 VND" and tot2[7] == "70,000 VND")], roles_obj=RO, pg_text=json.dumps(tot2), extra={"total": tot2})
    goto(mo, f"{ORACLE}/reports/delivery")
    mo.fill("#from", "2026-10-20")
    mo.fill("#to", "2026-10-20")
    nav(mo, "button:has-text('Show')")
    ov = row_cells(mo, "#delivery-overall")
    hubs_ = [row_cells(mo, f"#delivery-by-hub tbody:first-of-type tr:nth-child({i})") for i in (1, 2)]
    ship = row_cells(mo, "#delivery-by-shipper tbody tr")
    d1d = next((r for r in hubs_ if "District 1" in r[0]), [])
    btd = next((r for r in hubs_ if "Binh Thanh" in r[0]), [])
    step(run, sc, "7.3", "manager", "Delivery performance 2026-10-20", "overall 2/1/33.3%/20.0 min (n=3)/25.0 min (n=2); D1 1/0/0.0%/10.0 (n=1)/20.0 (n=1); BT 1/1/50.0%/25.0 (n=2)/30.0 (n=1); one shipper = overall",
         [("overall", ov[1:] == ["2", "1", "33.3%", "20.0 min (n=3)", "25.0 min (n=2)"]), ("District 1", d1d[1:] == ["1", "0", "0.0%", "10.0 min (n=1)", "20.0 min (n=1)"]),
          ("Binh Thanh", btd[1:] == ["1", "1", "50.0%", "25.0 min (n=2)", "30.0 min (n=1)"]), ("shipper row", ship[1:] == ov[1:] and "Shipper One" in ship[0])],
         roles_obj=RO, pg_text=json.dumps({"overall": ov, "hubs": hubs_, "shipper": ship}), extra={"overall": ov, "hubs": hubs_, "shipper": ship})
    goto(mo, f"{ORACLE}/reports/workload")
    w1, w2 = row_cells(mo, "#workload-1"), row_cells(mo, "#workload-2")
    step(run, sc, "7.4", "manager", "Workload now", "D1: New 0 Confirmed 0 Preparing 0, 0 / 12; Binh Thanh (Archived): New 1, 1 / 8",
         [("D1", "District 1" in w1[0] and w1[1:4] == ["0", "0", "0"] and w1[4] == "0 / 12"), ("BT", "Binh Thanh" in w2[0] and "Archived" in w2[0] and w2[1:4] == ["1", "0", "0"] and w2[4] == "1 / 8")],
         roles_obj=RO, pg_text=json.dumps([w1, w2]), extra={"d1": w1, "bt": w2})
    goto(mo, f"{ORACLE}/reports/sales")
    mo.fill("#from", "2026-01-01")
    mo.fill("#to", "2026-01-01")
    nav(mo, "button:has-text('Show')")
    ts_ = text(mo)
    tot3 = row_cells(mo, "#sales-total")
    shot_s = shot(RO, "manager", "S7_7.5_manager_sales.png", sc)
    goto(mo, f"{ORACLE}/reports/delivery")
    mo.fill("#from", "2026-01-01")
    mo.fill("#to", "2026-01-01")
    nav(mo, "button:has-text('Show')")
    ov3 = row_cells(mo, "#delivery-overall")
    step(run, sc, "7.5", "manager", "empty day 2026-01-01 (Sales, Delivery)", "Sales 'No delivered orders in this period.' and 0 / 0 VND; Delivery n/a, n/a (n=0), n/a (n=0)",
         has(ts_, "No delivered orders in this period.") + [("sales total zeros", tot3[1:] == ["0", "0 VND", "0 VND", "0 VND", "0 VND", "0 VND", "0 VND"]),
          ("delivery n/a", ov3[1:] == ["0", "0", "n/a", "n/a (n=0)", "n/a (n=0)"])], roles_obj=RO, pg_text=ts_ + " || " + json.dumps(ov3), extra={"sales_total": tot3, "delivery_overall": ov3},
         shots=[(RO, "manager", "S7_7.5_manager_delivery.png")])
    # -- part B, main database
    mg = P["manager"]
    goto(mg, f"{MAIN}/reports/sales")
    mg.fill("#from", "2026-10-01")
    mg.fill("#to", "2026-10-27")
    nav(mg, "button:has-text('Show')")
    before_tab = text(mg, "#sales-table")
    step(run, sc, "7.6", "manager", "Sales 2026-10-01 to 2026-10-27, main DB", "(reference text for 7.8)", [("table present", "All hubs" in before_tab)], pg_text=before_tab)
    goto(ad, f"{MAIN}/admin/archive")
    ad.fill("#order_id", "1")
    nav(ad, "#archive-one button:has-text('Archive this order')")
    t = text(ad)
    resp = goto(ad, f"{MAIN}/admin/archive/1")
    th = text(ad)
    step(run, sc, "7.7", "admin", "archive closed order 1", "banner 'The closed order is archived. Its history and reports are kept.'; Recently archived lists order 1; the history page opens",
         has(t, "The closed order is archived. Its history and reports are kept.", "Recently archived") + [("history page 200", resp.status == 200), ("history heading", "Archived order 1" in th)],
         pg_text=t + " || " + th, order=1, shots=["S7_7.7_admin.png"])
    resp = goto(cu, f"{MAIN}/order/1/receipt")
    trc = text(cu)
    goto(mg, f"{MAIN}/reports/sales")
    mg.fill("#from", "2026-10-01")
    mg.fill("#to", "2026-10-27")
    nav(mg, "button:has-text('Show')")
    after_tab = text(mg, "#sales-table")
    goto(cu, f"{MAIN}/order/mine")
    step(run, sc, "7.8", "customer+manager", "open the receipt of order 1; repeat the sales report", "receipt opens (Receipt · Order 1, Total T 130,000 VND); Sales table text identical; My orders no longer lists Order 1",
         [("receipt 200", resp.status == 200)] + has(trc, "Receipt · Order 1", "Total T 130,000 VND") + [("sales table identical", before_tab == after_tab),
          ("My orders without Order 1", cu.locator("a:text-is('Order 1')").count() == 0)], pg_text=trc + " || identical=" + str(before_tab == after_tab), order=1,
         shots=["S7_7.8_customer_my_orders.png", (R, "manager", "S7_7.8_manager.png")])
    goto(ad, f"{MAIN}/admin/archive")
    ad.fill("#order_id", "9")
    nav(ad, "#archive-one button:has-text('Archive this order')")
    t = text(ad)
    d9 = db_rows(main_db, "select archived_at from orders where id=9")[0]
    step(run, sc, "7.9", "admin", "archive open order 9", "banner 'Only a closed, unarchived order can be archived.'; order 9 stays unarchived",
         has(t, "Only a closed, unarchived order can be archived.") + [("order 9 archived_at empty", d9["archived_at"] is None)], pg_text=t, order=9)
    facts(sc, {"orders_1_9": "select id,state,archived_at from orders where id in (1,9)"})
    facts("S7", {"oracle_orders": "select id,state from orders order by id"}, db=oracle_db) if False else None
    (EVID / "S7" / "db_facts_oracle.json").write_text(json.dumps(db_rows(oracle_db, "select id,hub_id,state,total_amount from orders order by id"), indent=1), encoding="utf-8")

    # ======================================================================= S8
    sc = "S8"
    total_forms = len(FORMS)
    missing = [f for f in FORMS if f["token_len"] == 0]
    pages = sorted({(f["role"], re.sub(r"/\d+", "/<id>", f["url"].replace(MAIN, "").replace(ORACLE, ""))) for f in FORMS})
    step(run, sc, "8.1", "all roles", "every post form seen during S1 to S7", "0 post forms without a non-empty csrf_token",
         [(f"{total_forms} post forms seen, none without a token", total_forms > 0 and not missing)], pg_text=f"{total_forms} post forms on {len(pages)} distinct role/page pairs; missing: {len(missing)}",
         extra={"forms": total_forms, "pages": [list(p_) for p_ in pages], "missing": missing}, shots=["S8_8.1_admin.png"])
    for sid, mode in (("8.2", "remove"), ("8.3", "alter")):
        goto(ad, f"{MAIN}/admin/hubs/2")
        ad.fill("input[name=max_active_orders]", "7")
        ad.evaluate("(m) => { const i = document.querySelector(\"form[action$='/admin/hubs/2'] input[name=csrf_token]\"); if (m === 'remove') i.remove(); else i.value = 'x' + i.value; }", mode)
        resp = nav(ad, "button:has-text('Save hub')")
        t = text(ad)
        goto(ad, f"{MAIN}/admin/hubs")
        step(run, sc, sid, "admin", f"Save hub BT with the csrf_token {'removed' if mode == 'remove' else 'changed'}", "HTTP 400 'Form expired' with the expiry message; BT still 1 / 8",
             [("HTTP 400", resp.status == 400)] + has(t, "Form expired", "This form has expired or did not come from SaigonBite. Go back, reload the page and try again.") + [("BT unchanged 1 / 8", "1 / 8" in text(ad, "#hub-2"))],
             pg_text=t, extra={"status": resp.status}, shots=[f"S8_{sid}_admin.png"])
    goto(kt, f"{MAIN}/kitchen/availability")
    kt.evaluate("() => document.querySelector('#item-1 form input[name=csrf_token]').remove()")
    resp = nav(kt, "#item-1 button")
    t = text(kt)
    goto(kt, f"{MAIN}/kitchen/availability")
    step(run, sc, "8.4", "kitchen", "Mark sold out Pho bo tai with the csrf_token removed", "HTTP 400 Form expired; Pho bo tai still Available",
         [("HTTP 400", resp.status == 400)] + has(t, "Form expired") + [("still Available", "Available" in text(kt, "#item-1") and "Sold out" not in text(kt, "#item-1"))], pg_text=t, extra={"status": resp.status})
    goto(cu, f"{MAIN}/order/9")
    cu.evaluate("() => document.querySelector(\"form[action$='/cancel'] input[name=csrf_token]\").remove()")
    resp = nav(cu, "button:has-text('Cancel this order')")
    t = text(cu)
    d9 = db_rows(main_db, "select state from orders where id=9")[0]
    step(run, sc, "8.5", "customer", "Cancel this order 9 with the csrf_token removed", "HTTP 400 Form expired; order 9 still PLACED",
         [("HTTP 400", resp.status == 400)] + has(t, "Form expired") + [("order 9 PLACED", d9["state"] == "PLACED")], pg_text=t, order=9, extra={"status": resp.status})
    facts(sc, {"bt_capacity": "select id,max_active_orders from hub", "item1_hub1": "select hub_id,menu_item_id,is_available from hub_menu_item where menu_item_id=1", "order9": "select id,state from orders where id=9"})
    env["finished"] = datetime.now().isoformat(timespec="seconds")
    env["all_events"] = {k: v for k, v in {**{f"main/{k}": v for k, v in R.events.items()}, **{f"oracle/{k}": v for k, v in RO.events.items()}}.items() if v}
    R.close()
    RO.close()
    return env


srv1 = start_server(main_db, 5100, NOTES / "logs" / f"integration_main_{TS}.log")
srv2 = start_server(oracle_db, 5101, NOTES / "logs" / f"integration_oracle_{TS}.log")
try:
    with sync_playwright() as pw:
        env = run_all(pw)
finally:
    stop_server(srv1)
    stop_server(srv2)
(EVID / "results.json").write_text(json.dumps({"environment": env, "steps": RESULTS}, indent=1, default=str), encoding="utf-8")
(EVID / "forms_seen.json").write_text(json.dumps(FORMS, indent=1), encoding="utf-8")
fails = [r for r in RESULTS if r["result"] != "PASS"]
print(f"\n{len(RESULTS)} steps, {len(RESULTS) - len(fails)} PASS, {len(fails)} FAIL")
for r in fails:
    print(" FAIL", r["scenario"], r["step"], r["failed_checks"])
sys.exit(1 if fails else 0)
