"""Before / after of the refined screens at several widths (360, 390, 768, 1440 px).

Author: 722I0004 · AI-assisted (Claude Sonnet 5.5)

Two local servers run on identical copies of one database: the worktree of the commit before the refinements (5394cee, port 5104)
and the final code (port 5105). Same pages, same widths, same measurement rules as render.py. Output: docs/part2/ui/_after/*.png and
_kit/reports/width_before_after.csv.  Usage (tools venv): compare_width.py
"""
import csv
import glob
import os
import shutil
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
UI = HERE.parent
REPO = UI.parents[2]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(REPO / "docs/part2/test_report/integration_2026-10-27/scripts"))
import p5lib  # noqa: E402
from p5lib import NOTES, ROLES, start_server, stop_server  # noqa: E402
from render import measure, summary  # noqa: E402
from playwright.sync_api import sync_playwright  # noqa: E402

WORKTREE = NOTES / "worktree_before"
src = sorted(glob.glob(str(NOTES / "db" / "capture_implemented_*.db")))[-1]
ts = int(time.time())
dbs = {}
for label in ("before", "after"):
    dst = NOTES / "db" / f"width_{label}_{ts}.db"
    shutil.copy(src, dst)
    dbs[label] = dst
# (role, page, widths)
PAGES = [("customer", "/order/mine", [360, 390]), ("manager", "/reports/sales", [768, 1440]), ("kitchen", "/kitchen/", [768, 1440]),
         ("admin", "/admin/menu", [768, 1440]), ("shipper", "/delivery/", [390]), ("customer", "/order/hubs", [390])]
OUT = UI / "_after"
OUT.mkdir(exist_ok=True)
rows = []
procs = {}
try:
    p5lib.APP_DIR = WORKTREE
    procs["before"] = start_server(dbs["before"], 5104, NOTES / "logs" / "width_before_server.log")
    p5lib.APP_DIR = REPO
    procs["after"] = start_server(dbs["after"], 5105, NOTES / "logs" / "width_after_server.log")
    with sync_playwright() as pw:
        browser = pw.chromium.launch(channel="msedge")
        for label, port in (("before", 5104), ("after", 5105)):
            for role, page_url, widths in PAGES:
                for w in widths:
                    ctx = browser.new_context(viewport={"width": w, "height": 900}, device_scale_factor=1, is_mobile=w < 600, has_touch=w < 600)
                    pg = ctx.new_page()
                    pg.goto(f"http://127.0.0.1:{port}/login")
                    pg.fill("input[name=username]", ROLES[role][0])
                    pg.fill("input[name=password]", "123456")
                    with pg.expect_navigation():
                        pg.click("button[type=submit]")
                    pg.goto(f"http://127.0.0.1:{port}{page_url}")
                    pg.add_style_tag(content=".summary-bar{position:static !important}")
                    stem = f"{role}{page_url.replace('/', '_')}_{w}_{label}"
                    pg.screenshot(path=str(OUT / f"{stem}.png"), full_page=True)
                    m = measure(pg)
                    rows.append({"page": page_url, "role": role, "width": w, "version": label, "overflow": m["overflow"], "scrollWidth": m["scrollWidth"],
                                 "tap_under_44": len(m["tap_small"]), "contrast_min": m["contrast_min"], "png": f"_after/{stem}.png"})
                    ctx.close()
        browser.close()
finally:
    for pr in procs.values():
        stop_server(pr)
with (HERE / "reports" / "width_before_after.csv").open("w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader()
    w.writerows(rows)
for r in rows:
    print(r["version"], r["role"], r["page"], r["width"], "overflow" if r["overflow"] else "ok", r["scrollWidth"], "tap<44:", r["tap_under_44"])
