"""P5-009 smoke: every role profile logs in and opens its home screen on a fresh demo DB."""
import json, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from p5lib import *
from playwright.sync_api import sync_playwright

out = NOTES / "smoke"
db = new_db(NOTES / "db" / "smoke" / f"smoke_{int(time.time())}.db", demo=True)
srv = start_server(db, 5100, out / "server.log")
res = {}
try:
    with sync_playwright() as pw:
        res["versions"] = versions(pw)
        r = Roles(pw, "http://127.0.0.1:5100", NOTES / "profiles" / "smoke", ROLES.keys(), out)
        for name in ROLES:
            pg = r.login(name)
            res[name] = {"url": pg.url, "h1": pg.inner_text("h1"), "title": pg.title()}
            r.shot(name, f"smoke_{name}.png", full_page=False)
        res["events"] = {k: v for k, v in r.events.items() if v}
        r.close()
finally:
    stop_server(srv)
res["db"] = str(db)
json.dump(res, open(out / "smoke.json", "w", indent=1) if False else open(out / "smoke.json", "w"), indent=1)
print(json.dumps(res, indent=1))
