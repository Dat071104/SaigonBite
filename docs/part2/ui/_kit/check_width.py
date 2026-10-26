"""Staff screens at 768 px (and the phone screens at 360 px): overflow and tap-size report on a copy of the
latest capture database.  Usage (tools venv): check_width.py <label> [--db path]
Writes docs/part2/ui/_kit/captured/<label>/width_check.csv.  Author: 722I0004 · AI-assisted (Claude Sonnet 5.5)"""
import csv, glob, shutil, sys, time
from pathlib import Path
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
sys.path.insert(0, str(HERE)); sys.path.insert(0, str(REPO / "docs/part2/test_report/integration_2026-10-27/scripts"))
from render import measure, summary
from p5lib import NOTES, Roles, start_server, stop_server
from playwright.sync_api import sync_playwright

label = sys.argv[1]
src = sorted(glob.glob(str(NOTES / "db" / f"capture_{label}_*.db")))[-1]
dst = NOTES / "db" / f"width_{label}_{int(time.time())}.db"
shutil.copy(src, dst)
srv = start_server(dst, 5103, NOTES / "logs" / f"width_{label}_server.log")
rows = []
try:
    with sync_playwright() as pw:
        for role, widths, pages in [
            ("kitchen", [768], ["/kitchen/", "/kitchen/orders/9", "/kitchen/availability"]),
            ("admin", [768], ["/admin/hubs", "/admin/hubs/1", "/admin/menu", "/admin/hubs/2/menu", "/admin/items/4", "/admin/archive"]),
            ("manager", [768], ["/reports/sales", "/reports/workload", "/reports/delivery"]),
            ("customer", [360], ["/order/hubs", "/order/hubs/1", "/order/mine", "/order/9"]),
            ("shipper", [360], ["/delivery/"]),
        ]:
            for w in widths:
                R = Roles(pw, "http://127.0.0.1:5103", NOTES / "profiles" / f"width_{label}_{int(time.time())}", [role])
                R.login(role)
                pg = R.page[role]
                pg.set_viewport_size({"width": w, "height": 1000})
                for u in pages:
                    pg.goto("http://127.0.0.1:5103" + u)
                    m = measure(pg)
                    rows.append([role, w, u, m["overflow"], m["scrollWidth"], len(m["tap_small"]), summary(m)])
                R.close()
finally:
    stop_server(srv)
out = HERE / "captured" / label
out.mkdir(parents=True, exist_ok=True)
with (out / "width_check.csv").open("w", encoding="utf-8", newline="") as f:
    w = csv.writer(f); w.writerow(["role", "width", "page", "overflow", "scrollWidth", "tap_small", "summary"]); w.writerows(rows)
for r in rows: print(r)
