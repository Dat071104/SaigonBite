"""Compile the screen sources of every UC into wireframe and mockup pages.

Author: 722I0004 · AI-assisted (Claude Sonnet 5.5)

  build.py [--uc UC-01 ...]

Input : docs/part2/ui/UC-0x/src/<screen id>.html   a header comment (id, title, role, viewport, nav, active, who,
        wide) and the page body, written once.
Output: UC-0x/wireframes/<id>.html   greyscale, `{{p:placeholder||real}}` shows the placeholder
        UC-0x/mockups/<id>.html      app tokens, `{{p:placeholder||real}}` shows the real value taken from the
                                     running app (never an invented number)
The two pages therefore always share one structure, the same frame as base.html (top bar, role links, 720 px
measure, footer) and the same hotspots (`data-goto="UC-01-S03"`, used by render.py for the Figma flows).
Wireframes and mockups are authored as HTML/CSS (AI-assisted); they are assembled and linked in Figma by the owner.
"""
import argparse
import html
import re
import sys
from datetime import date
from pathlib import Path

UI = Path(__file__).resolve().parents[1]
AUTHOR = "722I0004 · AI-assisted (Claude Sonnet 5.5)"
HEADER = re.compile(r"\A<!--screen\n(.*?)\n-->\n", re.S)
PLACEHOLDER = re.compile(r"\{\{p:(.*?)\|\|(.*?)\}\}")


def parse(src: str):
    m = HEADER.match(src)
    if not m:
        raise ValueError("missing <!--screen ... --> header")
    meta = dict(line.split(": ", 1) for line in m[1].splitlines() if ": " in line)
    return meta, src[m.end():]


def page(meta: dict, body: str, kind: str) -> str:
    wireframe = kind == "wireframes"
    body = PLACEHOLDER.sub(lambda m: f'<span class="ph">{m[1]}</span>' if wireframe else m[2], body)
    w, h = meta["viewport"].split("x")
    nav = [n for n in meta.get("nav", "").split("|") if n]
    links = "".join(
        f'<a href="#"{" aria-current=\"page\"" if n == meta.get("active") else ""}>{n}</a>' for n in nav)
    wide = ' class="wide"' if meta.get("wide") == "yes" else ""
    label = "Wireframe" if wireframe else "Mockup"
    note = ("Low-fidelity layout: real labels, placeholder values." if wireframe
            else "Design target: real names and amounts read from the running app.")
    who = meta.get("who", "")
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="viewport-px" content="{w}x{h}">
<meta name="screen-id" content="{meta['id']}">
<meta name="author" content="{AUTHOR}">
<title>{html.escape(meta['id'])} {html.escape(meta['title'])} ({label.lower()})</title>
<link rel="stylesheet" href="../../_kit/{kind[:-1]}.css">
</head>
<body{wide}>
  <header class="topbar">
    <div class="wrap">
      <span class="brand">SaigonBite</span>
      <nav class="account" aria-label="Account"><span class="who">{who}</span><button type="button" class="secondary">Log out</button></nav>
    </div>
    <div class="wrap"><nav class="mainnav" aria-label="Main">{links}</nav></div>
  </header>
  <main id="content">
    <div class="wrap">
{body.rstrip()}
    </div>
  </main>
  <footer>
    <div class="wrap">
      <p>{label} {meta['id']} · {html.escape(meta['title'])}</p>
      <p class="{'wf-note' if wireframe else 'mk-note'}">{note} {AUTHOR}. Authored as HTML/CSS; assembled and linked in Figma by the owner.</p>
    </div>
  </footer>
</body>
</html>
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--uc", nargs="*", default=None)
    args = ap.parse_args()
    ucs = args.uc or sorted(p.name for p in UI.glob("UC-0*") if p.is_dir())
    n = 0
    for uc in ucs:
        for src in sorted((UI / uc / "src").glob("*.html")):
            meta, body = parse(src.read_text(encoding="utf-8"))
            assert meta["id"] == src.stem, f"{src.name}: id {meta['id']}"
            for kind in ("wireframes", "mockups"):
                out = UI / uc / kind
                out.mkdir(exist_ok=True)
                (out / f"{src.stem}.html").write_text(page(meta, body, kind), encoding="utf-8", newline="\n")
                n += 1
    print(f"{n} pages built on {date.today().isoformat()}")


if __name__ == "__main__":
    sys.exit(main())
