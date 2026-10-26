"""Shared helpers for the P5 browser runs (Playwright for Python + installed Microsoft Edge).

Author: 722I0004 · AI-assisted (Claude Sonnet 5.5)

Run with the isolated tools venv (Part2/notes/P5/tools/venv). The app server runs with the repo .venv:
a local Flask development server, debug off, a random SAIGONBITE_SECRET_KEY that exists only in the
server process environment.
"""
import json
import os
import secrets
import sqlite3
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

REPO = Path(r"D:\RAD\FINAL\SaigonBite")
NOTES = Path(r"D:\RAD\FINAL\Part2\notes\P5")
REPO_PY = REPO / ".venv" / "Scripts" / "python.exe"
# P5_APP_DIR points the server at another checkout (a git worktree of an earlier commit) for the "before" figures
APP_DIR = Path(os.environ.get("P5_APP_DIR", str(REPO)))

PHONE = {"viewport": {"width": 390, "height": 844}, "is_mobile": True, "has_touch": True}
DESKTOP = {"viewport": {"width": 1440, "height": 900}}

# role -> (login username, device)
ROLES = {
    "customer": ("customer", PHONE), "tourist": ("tourist", PHONE),
    "kitchen": ("kitchen", DESKTOP), "kitchen_bt": ("kitchen_bt", DESKTOP),
    "shipper": ("shipper", PHONE), "shipper2": ("shipper2", PHONE),
    "admin": ("admin", DESKTOP), "manager": ("manager", DESKTOP),
}


def new_db(path: Path, demo: bool = True) -> Path:
    """Create a brand-new database with init_db.py (never overwrites)."""
    path = Path(path)
    if path.exists():
        raise FileExistsError(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [str(REPO_PY), str(REPO / "init_db.py"), "--db", str(path)]
    if not demo:
        cmd.append("--no-demo")
    subprocess.run(cmd, check=True, cwd=str(REPO), capture_output=True)
    return path


def start_server(db: Path, port: int, log: Path) -> subprocess.Popen:
    env = dict(os.environ)
    env["SAIGONBITE_DATABASE"] = str(db)
    env["SAIGONBITE_SECRET_KEY"] = secrets.token_urlsafe(48)
    env.pop("FLASK_DEBUG", None)
    log.parent.mkdir(parents=True, exist_ok=True)
    fh = open(log, "w", encoding="utf-8")
    proc = subprocess.Popen([str(REPO_PY), "-m", "flask", "--app", str(APP_DIR / "app.py"), "run", "--port", str(port)],
                            cwd=str(APP_DIR), env=env, stdout=fh, stderr=subprocess.STDOUT)
    for _ in range(100):
        try:
            urllib.request.urlopen(f"http://127.0.0.1:{port}/", timeout=1).read()
            return proc
        except Exception:
            time.sleep(0.3)
    proc.kill()
    raise RuntimeError("server did not start; see " + str(log))


def stop_server(proc: subprocess.Popen) -> None:
    proc.terminate()
    try:
        proc.wait(timeout=10)
    except subprocess.TimeoutExpired:
        proc.kill()


class Roles:
    """One persistent Edge profile per role; logs console errors and every HTTP response >= 400."""

    def __init__(self, pw, base: str, profile_root: Path, names, shots: Path | None = None):
        self.base, self.shots = base, shots
        self.ctx, self.page, self.events = {}, {}, {}
        for name in names:
            user, device = ROLES[name]
            d = Path(profile_root) / name
            d.mkdir(parents=True, exist_ok=True)
            ctx = pw.chromium.launch_persistent_context(str(d), channel="msedge", headless=True,
                                                        device_scale_factor=1, **device)
            page = ctx.pages[0] if ctx.pages else ctx.new_page()
            ev = []
            page.on("console", lambda m, ev=ev: ev.append(("console." + m.type, m.text)) if m.type in ("error",) else None)
            page.on("response", lambda r, ev=ev: ev.append(("http", f"{r.status} {r.request.method} {r.url}")) if r.status >= 400 else None)
            page.on("pageerror", lambda e, ev=ev: ev.append(("pageerror", str(e))))
            self.ctx[name], self.page[name], self.events[name] = ctx, page, ev

    def login(self, name: str, password: str = "123456"):
        user, _ = ROLES[name]
        pg = self.page[name]
        pg.goto(self.base + "/login")
        pg.fill("input[name=username]", user)
        pg.fill("input[name=password]", password)
        pg.click("button[type=submit]")
        pg.wait_for_load_state("load")
        return pg

    def logout(self, name: str):
        pg = self.page[name]
        pg.click("form[action$='/logout'] button")
        pg.wait_for_load_state("load")

    def shot(self, name: str, fname: str, full_page: bool = True):
        path = Path(self.shots) / fname
        path.parent.mkdir(parents=True, exist_ok=True)
        self.page[name].screenshot(path=str(path), full_page=full_page)
        return str(path.name)

    def close(self):
        for c in self.ctx.values():
            c.close()


def db_rows(db: Path, sql: str, params=()):
    """Read-only corroboration query."""
    conn = sqlite3.connect(Path(db).as_uri() + "?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    try:
        return [dict(r) for r in conn.execute(sql, params).fetchall()]
    finally:
        conn.close()


def versions(pw) -> dict:
    from importlib.metadata import version
    b = pw.chromium.launch(channel="msedge")
    v = b.version
    b.close()
    return {"playwright": version("playwright"), "edge": v, "python": sys.version.split()[0]}
