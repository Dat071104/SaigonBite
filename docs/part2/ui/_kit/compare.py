"""Compare every mockup with the implemented screen of the same id (visible text of the page body).

Author: 722I0004 · AI-assisted (Claude Sonnet 5.5)

  compare.py        (tools venv)  ->  _kit/reports/mockup_vs_implemented.csv

Per screen: lines that only the mockup shows and lines that only the real screen shows, after masking times and the shared
frame (top bar, footer). Mockups use the case of the 'before' run, the implemented screens the case of the final run, so
order numbers and clock times can differ; they are masked.
"""
import csv
import re
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
UI = HERE.parent
TIME = re.compile(r"\d\d:\d\d, \d\d/\d\d/\d{4}")
FRAME = {"Skip to content", "SaigonBite", "Log out"}


def lines(text: str) -> list[str]:
    out = []
    for raw in re.split(r"[\t\n]+", text):
        s = re.sub(r"\s+", " ", TIME.sub("<time>", raw)).strip()
        if s and s not in FRAME and not s.startswith("SaigonBite ·") and not s.startswith(("Mockup UC-", "Design target:", "Wireframe UC-")):
            out.append(s)
    return out


def main():
    rows = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch(channel="msedge")
        for uc in sorted(p.name for p in UI.glob("UC-0*") if p.is_dir()):
            for html in sorted((UI / uc / "mockups").glob("*.html")):
                sid = html.stem
                vp = re.search(r'viewport-px" content="(\d+)x(\d+)', html.read_text(encoding="utf-8"))
                page = browser.new_page(viewport={"width": int(vp[1]), "height": int(vp[2])}, is_mobile=int(vp[1]) < 600)
                page.goto(html.as_uri())
                m = lines(page.inner_text("body"))
                page.close()
                real = lines((HERE / "captured" / "implemented" / f"{sid}.txt").read_text(encoding="utf-8"))
                # compare as multisets of lines, ignoring the top bar links that both share
                only_m = [x for x in m if x not in real]
                only_r = [x for x in real if x not in m]
                rows.append({"screen": sid, "mockup_lines": len(m), "implemented_lines": len(real),
                             "only_in_mockup": " ¦ ".join(only_m), "only_in_implemented": " ¦ ".join(only_r)})
        browser.close()
    out = HERE / "reports" / "mockup_vs_implemented.csv"
    with out.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    same = sum(1 for r in rows if not r["only_in_mockup"] and not r["only_in_implemented"])
    print(f"{len(rows)} screens compared, {same} identical in text")
    for r in rows:
        if r["only_in_mockup"] or r["only_in_implemented"]:
            print(r["screen"], "| mockup only:", r["only_in_mockup"][:160], "| impl only:", r["only_in_implemented"][:160])


if __name__ == "__main__":
    sys.exit(main())
