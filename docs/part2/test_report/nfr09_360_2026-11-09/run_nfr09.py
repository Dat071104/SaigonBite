"""NFR-09 check: key SaigonBite pages at a 360 CSS-pixel viewport.

Author: 722I0004 · AI-assisted (Claude Sonnet 5.5)

For every page it records document.documentElement.scrollWidth / clientWidth (PASS when scrollWidth <= clientWidth and
the layout viewport is really 360 px and the page cannot be scrolled sideways), elements that stick out past the viewport
(and whether an overflow-x wrapper clips them), and visible interactive elements (a, button, input, select) whose box is
smaller than 44 x 44 CSS px. It starts a throwaway copy of the app on a fresh seeded database and never touches
application code or real data.

Usage (tools venv with Playwright installed; the server is started with --server-python, default: this interpreter):
    python run_nfr09.py --repo <SaigonBite checkout> --out <evidence folder> [--port 5109]
                        [--server-python <python with the app requirements>] [--scratch <dir for db + log>]
"""
import argparse
import csv
import json
import os
import re
import secrets
import subprocess
import sys
import tempfile
import time
import urllib.request
from datetime import datetime
from pathlib import Path

from playwright.sync_api import sync_playwright

ap = argparse.ArgumentParser()
ap.add_argument("--repo", default=str(Path(__file__).resolve().parents[4]))
ap.add_argument("--out", default=str(Path(__file__).resolve().parent))
ap.add_argument("--port", type=int, default=5109)
ap.add_argument("--server-python", default=sys.executable)
ap.add_argument("--scratch", default=tempfile.mkdtemp(prefix="nfr09_"))
ap.add_argument("--chromium", default=None, help="path to a chrome.exe when the Playwright-pinned build is not installed")
ap.add_argument("--date", default=datetime.now().strftime("%d/%m/%Y"))
args = ap.parse_args()

REPO, OUT, SCRATCH = Path(args.repo).resolve(), Path(args.out).resolve(), Path(args.scratch).resolve()
if Path(args.server_python).exists():
    args.server_python = str(Path(args.server_python).resolve())
BASE = f"http://127.0.0.1:{args.port}"
VW, VH, DSF, MIN_TARGET = 360, 800, 2, 44
OUT.mkdir(parents=True, exist_ok=True)
SCRATCH.mkdir(parents=True, exist_ok=True)

MEASURE_JS = r"""
([minT]) => {
  const de = document.documentElement;
  const vw = de.clientWidth;
  const cs = e => getComputedStyle(e);
  const sel = e => e.tagName.toLowerCase() + (e.id ? '#' + e.id : '') + (e.classList.length ? '.' + Array.from(e.classList).join('.') : '');
  const txt = e => (e.innerText || e.value || e.getAttribute('aria-label') || e.getAttribute('title') || e.getAttribute('name') || '').replace(/\s+/g, ' ').trim().slice(0, 40);
  const visible = e => { const r = e.getBoundingClientRect(), s = cs(e);
    return s.display !== 'none' && s.visibility !== 'hidden' && r.width > 2 && r.height > 2; };
  // 1) page-level horizontal scroll (also try to scroll it for real: overflow-x:hidden on html/body can mask overflow)
  const before = window.scrollX; window.scrollTo(200, window.scrollY); const scrolled = window.scrollX; window.scrollTo(before, window.scrollY);
  // 2) elements sticking out of the viewport
  const wrapperOf = e => { for (let p = e.parentElement; p && p !== document.body && p !== de; p = p.parentElement) {
      const ox = cs(p).overflowX; if (ox === 'auto' || ox === 'scroll' || ox === 'hidden') { const r = p.getBoundingClientRect(); if (r.right <= vw + 0.5 && r.left >= -0.5) return p; } } return null; };
  const wide = [], clipped = [];
  for (const e of document.body.querySelectorAll('*')) {
    if (!visible(e)) continue;
    const r = e.getBoundingClientRect();
    if (r.right > vw + 0.5 || r.left < -0.5) {
      const w = wrapperOf(e);
      const item = {el: sel(e), left: Math.round(r.left * 10) / 10, right: Math.round(r.right * 10) / 10, width: Math.round(r.width * 10) / 10, text: txt(e)};
      if (w) { item.wrapper = sel(w); clipped.push(item); } else wide.push(item);
    }
  }
  // 3) tap targets
  const small = [], offscreen = [];
  let total = 0;
  for (const e of document.querySelectorAll('a, button, input, select')) {
    if (e.tagName === 'INPUT' && e.type === 'hidden') continue;
    if (!visible(e)) continue;
    let box = e, via = '';
    if (e.tagName === 'INPUT' && (e.type === 'checkbox' || e.type === 'radio')) {
      const lab = e.closest('label') || (e.id && document.querySelector('label[for="' + CSS.escape(e.id) + '"]'));
      if (lab && visible(lab)) { box = lab; via = 'label'; }
    }
    const r = box.getBoundingClientRect();
    if (r.bottom + window.scrollY <= 0 || r.right + window.scrollX <= 0) { offscreen.push({el: sel(e), text: txt(e), w: Math.round(r.width * 10) / 10, h: Math.round(r.height * 10) / 10}); continue; }  // e.g. skip link, shown on focus only
    total++;
    if (r.height < minT - 0.05 || r.width < minT - 0.05) {
      let inline = false;
      if (e.tagName === 'A' && cs(e).display === 'inline') {
        const par = e.parentElement; const t = (par.innerText || '').replace(/\s+/g, ' ').trim(); inline = t.length > (e.innerText || '').trim().length + 3; }
      small.push({el: sel(e), type: e.tagName.toLowerCase() + (e.type ? '[' + e.type + ']' : ''), text: txt(e), w: Math.round(r.width * 10) / 10, h: Math.round(r.height * 10) / 10,
                  inline, via, in_table: !!e.closest('table')});
    }
  }
  return {scrollWidth: de.scrollWidth, clientWidth: vw, bodyScrollWidth: document.body.scrollWidth, innerWidth: window.innerWidth,
          scrollXAfterScrollTo: scrolled, htmlOverflowX: cs(de).overflowX, bodyOverflowX: cs(document.body).overflowX,
          viewportMeta: (document.querySelector('meta[name=viewport]') || {}).content || null,
          wide, clipped, interactive_visible: total, small, offscreen};
}
"""

RESULTS = []
DIALOGS = []


def start_server():
    db = SCRATCH / "nfr09_demo.db"
    if db.exists():
        db.unlink()
    subprocess.run([args.server_python, str(REPO / "init_db.py"), "--db", str(db)], check=True, cwd=str(REPO), capture_output=True)
    env = dict(os.environ, SAIGONBITE_DATABASE=str(db), SAIGONBITE_SECRET_KEY=secrets.token_urlsafe(48))
    env.pop("FLASK_DEBUG", None)
    log = open(SCRATCH / "server.log", "w", encoding="utf-8")
    proc = subprocess.Popen([args.server_python, "-m", "flask", "--app", str(REPO / "app.py"), "run", "--port", str(args.port)],
                            cwd=str(REPO), env=env, stdout=log, stderr=subprocess.STDOUT)
    for _ in range(100):
        try:
            urllib.request.urlopen(BASE + "/", timeout=1).read()
            return proc, db
        except Exception:
            time.sleep(0.3)
    proc.kill()
    raise RuntimeError("server did not start, see " + str(SCRATCH / "server.log"))


def stop_server(proc):
    proc.terminate()
    try:
        proc.wait(timeout=10)
    except subprocess.TimeoutExpired:
        proc.kill()


def measure(page, pid, role, label, status=None):
    page.wait_for_load_state("load")
    m = page.evaluate(MEASURE_JS, [MIN_TARGET])
    page.screenshot(path=str(OUT / f"{pid}.png"), full_page=True)
    ok = m["scrollWidth"] <= m["clientWidth"] and m["clientWidth"] == VW and m["scrollXAfterScrollTo"] == 0
    small_block = [s for s in m["small"] if not s["inline"]]
    small_inline = [s for s in m["small"] if s["inline"]]
    rec = {"id": pid, "role": role, "page": label, "url": page.url.replace(BASE, ""), "http_status": status,
           "scrollWidth": m["scrollWidth"], "clientWidth": m["clientWidth"], "bodyScrollWidth": m["bodyScrollWidth"],
           "innerWidth": m["innerWidth"], "scrollXAfterScrollTo": m["scrollXAfterScrollTo"],
           "htmlOverflowX": m["htmlOverflowX"], "bodyOverflowX": m["bodyOverflowX"], "viewportMeta": m["viewportMeta"],
           "result": "PASS" if ok else "FAIL",
           "elements_wider_than_viewport": m["wide"], "elements_clipped_by_scroll_wrapper": m["clipped"],
           "interactive_visible": m["interactive_visible"],
           "small_targets_total": len(m["small"]), "small_targets_non_inline": len(small_block),
           "small_targets_inline_text_links": len(small_inline), "small_targets": m["small"], "offscreen_until_focus": m["offscreen"], "screenshot": f"{pid}.png"}
    RESULTS.append(rec)
    print(f"{pid:8} {rec['result']}  sw={rec['scrollWidth']} cw={rec['clientWidth']}  small={len(small_block)}+{len(small_inline)}inline  {rec['url']}")
    return rec


def go(page, pid, role, label, path):
    r = page.goto(BASE + path)
    return measure(page, pid, role, label, r.status if r else None)


def run(pw):
    browser = pw.chromium.launch(executable_path=args.chromium) if args.chromium else pw.chromium.launch()
    ctxs, pages = {}, {}
    for role in ("anon", "customer", "kitchen", "shipper", "admin", "manager"):
        ctx = browser.new_context(viewport={"width": VW, "height": VH}, device_scale_factor=DSF, is_mobile=True, has_touch=True)
        pg = ctx.new_page()
        pg.on("dialog", lambda d: (DIALOGS.append(d.message), d.accept()))
        ctxs[role], pages[role] = ctx, pg

    def login(role, user):
        pg = pages[role]
        pg.goto(BASE + "/login")
        pg.fill("input[name=username]", user)
        pg.fill("input[name=password]", "123456")
        with pg.expect_navigation():
            pg.click("button[type=submit]")
        return pg

    def click_nav(pg, selector):
        with pg.expect_navigation() as info:
            pg.click(selector)
        return info.value

    # ---------------------------------------------------------------- login / register (logged out)
    a = pages["anon"]
    go(a, "L01_login", "anonymous", "Login", "/login")
    go(a, "L02_register", "anonymous", "Register", "/register")
    go(a, "L03_home_anon", "anonymous", "Home (logged out)", "/")
    a.goto(BASE + "/login")
    a.fill("input[name=username]", "customer")
    a.fill("input[name=password]", "wrong-password")
    with a.expect_navigation() as info:
        a.click("button[type=submit]")
    measure(a, "L04_login_error", "anonymous", "Login, wrong password (error banner)", info.value.status)

    # ---------------------------------------------------------------- customer
    for r_, u in (("customer", "customer"), ("kitchen", "kitchen"), ("shipper", "shipper"), ("admin", "admin"), ("manager", "manager")):
        login(r_, u)
    cu = pages["customer"]
    go(cu, "C01_home", "customer", "Home", "/")
    go(cu, "C02_hubs", "customer", "Choose a kitchen hub", "/order/hubs")
    go(cu, "C03_menu", "customer", "Menu of District 1 hub", "/order/hubs/1")

    def fill_and_quote(hub, qtys):
        cu.goto(f"{BASE}/order/hubs/{hub}")
        for i, q in qtys.items():
            cu.fill(f"input[name=qty_{i}]", str(q))
        if cu.locator("#address_id option").count() > 1:
            cu.select_option("#address_id", "1")
        return click_nav(cu, "button:has-text('See the quote')")

    # order A: COD, Pho ga x2 (item 2) + item 1 -> used for the kitchen board and the replacement offer
    cu.goto(f"{BASE}/order/hubs/1")
    cu.fill("input[name=qty_2]", "2")
    cu.fill("input[name=qty_1]", "1")
    measure(cu, "C03b_menu_filled", "customer", "Menu with quantities typed (summary bar)")
    if cu.locator("#address_id option").count() > 1:
        cu.select_option("#address_id", "1")
    resp = click_nav(cu, "button:has-text('See the quote')")
    measure(cu, "C04_quote", "customer", "Quote / cart", resp.status)
    resp = click_nav(cu, "button:has-text('Confirm order')")
    measure(cu, "C05_confirmation", "customer", "Order confirmation (COD)", resp.status)
    m = re.search(r"/order/(\d+)", cu.url)
    order_a = int(m.group(1)) if m else None
    go(cu, "C06_detail", "customer", "Order detail (Placed)", f"/order/{order_a}")

    # order B: online payment simulator
    resp = fill_and_quote(1, {4: 1})
    online = cu.locator("input[name=payment][value^='ONLINE']")
    if online.count():
        online.first.check()
    measure(cu, "C07_quote_online", "customer", "Quote with online payment chosen", resp.status)
    resp = click_nav(cu, "button:has-text('Confirm order')")
    measure(cu, "C08_payment_sim", "customer", "Payment simulator", resp.status)
    resp = click_nav(cu, "button:has-text('Approve payment')")
    m = re.search(r"/order/(\d+)", cu.url)
    order_b = int(m.group(1)) if m else None
    measure(cu, "C09_confirmation_online", "customer", "Order confirmation (online)", resp.status)

    # kitchen
    ki = pages["kitchen"]
    go(ki, "K01_board", "kitchen", "Order board", "/kitchen/")
    go(ki, "K02_order_placed", "kitchen", "Order detail (Placed, confirm/reject/offer forms)", f"/kitchen/orders/{order_a}")
    go(ki, "K03_availability", "kitchen", "Availability list", "/kitchen/availability")
    # replacement offer: mark Pho ga (item 2) sold out, then offer a replacement
    ki.goto(BASE + "/kitchen/availability")
    if ki.locator("#item-2 button:has-text('Mark sold out')").count():
        click_nav(ki, "#item-2 button:has-text('Mark sold out')")
    ki.goto(f"{BASE}/kitchen/orders/{order_a}")
    if ki.locator("#replacement").count():
        val = ki.eval_on_selector_all("#replacement option", "els => (els.find(e => e.textContent.includes('Pho ga') && e.textContent.includes('Goi cuon')) || els[els.length-1] || {}).value")
        ki.select_option("#replacement", val)
        click_nav(ki, "button:has-text('Send the offer')")
    measure(ki, "K04_order_offered", "kitchen", "Order detail after replacement offered", 200)
    # customer sees the offer
    go(cu, "C10_detail_offer", "customer", "Order detail with replacement offer (Accept / Decline)", f"/order/{order_a}")
    if cu.locator("button:has-text('Accept')").count():
        click_nav(cu, "button:has-text('Accept')")
    # kitchen processes order A and order B to ready
    for oid in (order_a, order_b):
        for label in ("Confirm order", "Start preparing", "Mark ready"):
            ki.goto(f"{BASE}/kitchen/orders/{oid}")
            if ki.locator(f"button:has-text('{label}')").count():
                click_nav(ki, f"button:has-text('{label}')")
    go(ki, "K05_order_ready", "kitchen", "Order detail (Ready)", f"/kitchen/orders/{order_a}")
    go(ki, "K06_board_busy", "kitchen", "Order board with orders in several columns", "/kitchen/")

    # shipper
    sh = pages["shipper"]
    go(sh, "S01_board", "shipper", "Delivery board", "/delivery/")
    go(sh, "S02_detail", "shipper", "Delivery detail (awaiting pickup)", f"/delivery/orders/{order_a}")
    if sh.locator("button:has-text('Pick up')").count():
        click_nav(sh, "button:has-text('Pick up')")
    measure(sh, "S03_detail_picked", "shipper", "Delivery detail (picked up: Delivered / Could not deliver)", 200)
    go(sh, "S04_board_active", "shipper", "Delivery board with an active delivery", "/delivery/")

    # customer: finished screens
    go(cu, "C11_detail_progress", "customer", "Order detail (delivery in progress)", f"/order/{order_a}")
    go(cu, "C12_receipt", "customer", "Receipt", f"/order/{order_a}/receipt")
    go(cu, "C13_my_orders", "customer", "My orders", "/order/mine")
    go(cu, "C14_account", "customer", "Account / profile", "/account")
    go(cu, "C15_address_new", "customer", "New address form", "/account/addresses/new")

    # admin
    ad = pages["admin"]
    go(ad, "A01_hubs", "admin", "Hubs and capacity", "/admin/hubs")
    go(ad, "A02_hub_form", "admin", "Edit hub form", "/admin/hubs/1")
    go(ad, "A03_hub_menu", "admin", "Hub menu", "/admin/hubs/1/menu")
    go(ad, "A04_catalogue", "admin", "Catalogue (brands and dishes)", "/admin/menu")
    go(ad, "A05_item_form", "admin", "Edit dish form", "/admin/items/1")
    go(ad, "A06_item_new", "admin", "New dish form", "/admin/items/new")
    go(ad, "A07_vouchers", "admin", "Vouchers", "/admin/vouchers")
    go(ad, "A08_voucher_form", "admin", "Edit voucher form", "/admin/vouchers/1")
    go(ad, "A09_users", "admin", "Accounts", "/admin/users")
    go(ad, "A10_user_form", "admin", "Edit account form", "/admin/users/1")
    go(ad, "A11_archive", "admin", "Archive of old orders", "/admin/archive")

    # manager
    mg = pages["manager"]
    go(mg, "M01_reports", "manager", "Reports index", "/reports/")
    rng = "?from=2026-01-01&to=2026-12-31"
    go(mg, "M02_sales", "manager", "Sales report (2026)", "/reports/sales" + rng)
    go(mg, "M03_workload", "manager", "Workload report (2026)", "/reports/workload" + rng)
    go(mg, "M04_delivery", "manager", "Delivery report (2026)", "/reports/delivery" + rng)

    version = browser.version
    for c in ctxs.values():
        c.close()
    browser.close()
    return version, {"order_a": order_a, "order_b": order_b}


def main():
    proc, db = start_server()
    started = datetime.now().isoformat(timespec="seconds")
    try:
        with sync_playwright() as pw:
            version, orders = run(pw)
    finally:
        stop_server(proc)
    from importlib.metadata import version as pkgver
    commit = subprocess.run(["git", "-C", str(REPO), "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip()
    meta = {"date": args.date, "started": started, "commit": commit, "browser": f"Chromium {version} (driven by Playwright {pkgver('playwright')}, headless)",
            "viewport": f"{VW}x{VH}, deviceScaleFactor {DSF}, isMobile true, hasTouch true", "min_target_px": MIN_TARGET,
            "server": f"flask run on 127.0.0.1:{args.port}, debug off, throwaway DB from init_db.py (demo seed)", "orders_created": orders,
            "confirm_dialogs_accepted": DIALOGS}
    (OUT / "results.json").write_text(json.dumps({"meta": meta, "pages": RESULTS}, indent=1, ensure_ascii=False), encoding="utf-8")
    cols = ["id", "role", "page", "url", "http_status", "scrollWidth", "clientWidth", "result", "scrollXAfterScrollTo", "elements_wider_than_viewport",
            "elements_clipped_by_scroll_wrapper", "interactive_visible", "small_targets_total", "small_targets_non_inline", "small_targets_inline_text_links", "small_target_examples"]
    with open(OUT / "results.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(cols)
        for r in RESULTS:
            ex = "; ".join(f"{s['el']} '{s['text']}' {s['w']}x{s['h']}" + (" [inline]" if s["inline"] else "") for s in r["small_targets"][:6])
            w.writerow([r["id"], r["role"], r["page"], r["url"], r["http_status"], r["scrollWidth"], r["clientWidth"], r["result"], r["scrollXAfterScrollTo"],
                        len(r["elements_wider_than_viewport"]), len(r["elements_clipped_by_scroll_wrapper"]), r["interactive_visible"],
                        r["small_targets_total"], r["small_targets_non_inline"], r["small_targets_inline_text_links"], ex])
    fails = [r["id"] for r in RESULTS if r["result"] == "FAIL"]
    print("pages:", len(RESULTS), "FAIL:", fails)


if __name__ == "__main__":
    main()
