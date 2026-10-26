"""Render wireframe and mockup HTML to PNG and measure them.

Author: 722I0004 · AI-assisted (Claude Sonnet 5.5)

  render.py [--uc UC-01 ...] [--kind wireframes mockups]

For every docs/part2/ui/UC-0x/{wireframes,mockups}/*.html it writes a PNG of the same name at the screen's own
viewport (read from the page's <meta name="viewport-px">), and writes one row per page to
_kit/reports/render_<UC>_<kind>.csv: horizontal overflow, text contrast below the WCAG AA limit (4.5:1 normal text,
3:1 large text), interactive elements smaller than 44 px, inputs without a label, and the number of h1.
For mockups it also collects every [data-goto] element as a hotspot (x, y, w, h in frame pixels) into
_kit/reports/hotspots_<UC>.csv; figma_kit/flows.csv is built from them.

measure(page) is also imported by capture.py to measure the real app screens with the same rules.
Run with the tools venv (Playwright + Edge).
"""
import argparse
import csv
import re
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
UI = HERE.parent

MEASURE_JS = r"""
(expected) => {
  const parse = (c) => { const m = c.match(/rgba?\(([^)]+)\)/); if (!m) return [255,255,255,1];
    const p = m[1].split(/[ ,\/]+/).filter(Boolean).map(Number); return [p[0], p[1], p[2], p.length > 3 ? p[3] : 1]; };
  const over = (top, under) => { const a = top[3]; return [0,1,2].map(i => top[i] * a + under[i] * (1 - a)).concat([1]); };
  const bgOf = (el) => { const chain = []; for (let e = el; e; e = e.parentElement) chain.push(parse(getComputedStyle(e).backgroundColor));
    let bg = [255,255,255,1]; for (let i = chain.length - 1; i >= 0; i--) bg = over(chain[i], bg); return bg; };
  const lum = (c) => { const f = (v) => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); };
    return 0.2126 * f(c[0]) + 0.7152 * f(c[1]) + 0.0722 * f(c[2]); };
  const ratio = (a, b) => { const x = lum(a), y = lum(b); return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05); };
  const visible = (el) => { const r = el.getBoundingClientRect(); const s = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && s.visibility !== 'hidden' && s.display !== 'none' && s.opacity !== '0'; };
  const sel = (el) => { let s = el.tagName.toLowerCase(); if (el.id) s += '#' + el.id; else if (el.className && typeof el.className === 'string') s += '.' + el.className.trim().split(/\s+/)[0]; return s; };
  const out = { overflow: document.documentElement.scrollWidth > expected + 1, scrollWidth: document.documentElement.scrollWidth,
    innerWidth: expected, h1: document.querySelectorAll('h1').length, contrast_fail: [], contrast_min: 99, tap_small: [], unlabeled: [] };
  document.querySelectorAll('body *').forEach((el) => {
    if (!visible(el)) return;
    const own = Array.from(el.childNodes).some(n => n.nodeType === 3 && n.textContent.trim());
    if (!own) return;
    const s = getComputedStyle(el); const fg0 = parse(s.color); const bg = bgOf(el); const fg = over(fg0, bg);
    const r = ratio(fg, bg); const size = parseFloat(s.fontSize); const bold = parseInt(s.fontWeight, 10) >= 700;
    const large = size >= 24 || (size >= 18.66 && bold); const need = large ? 3 : 4.5;
    out.contrast_min = Math.min(out.contrast_min, +r.toFixed(2));
    if (r < need) out.contrast_fail.push({ el: sel(el), text: el.textContent.trim().slice(0, 40), ratio: +r.toFixed(2), need });
  });
  document.querySelectorAll('a[href], button, input:not([type=hidden]), select, textarea, summary').forEach((el) => {
    if (!visible(el)) return;
    const r = el.getBoundingClientRect(); const s = getComputedStyle(el);
    if (el.classList.contains('skip')) return;
    if (el.tagName === 'A' && s.display === 'inline' && el.closest('p, li, dd, td, label, span.hint')) return;   // links inside a sentence
    if (el.type === 'radio' || el.type === 'checkbox') { const l = el.closest('label'); if (l) { const lr = l.getBoundingClientRect(); if (lr.height >= 44) return; } }
    if (r.width < 44 || r.height < 44) out.tap_small.push({ el: sel(el), text: (el.textContent || el.value || el.name || '').trim().slice(0, 30), w: Math.round(r.width), h: Math.round(r.height) });
  });
  document.querySelectorAll('input:not([type=hidden]):not([type=submit]), select, textarea').forEach((el) => {
    if (!visible(el)) return;
    const labelled = (el.id && document.querySelector('label[for="' + el.id + '"]')) || el.closest('label') || el.getAttribute('aria-label') || el.getAttribute('aria-labelledby');
    if (!labelled) out.unlabeled.push(sel(el) + '[name=' + el.name + ']');
  });
  return out;
}
"""

HOTSPOT_JS = r"""
() => Array.from(document.querySelectorAll('[data-goto]')).map((el) => { const r = el.getBoundingClientRect();
  return { goto: el.dataset.goto, trigger: el.dataset.trigger || (el.tagName === 'A' ? 'click link' : 'press button'),
           label: (el.textContent || el.getAttribute('aria-label') || '').trim().replace(/\s+/g, ' ').slice(0, 50),
           x: Math.round(r.left + window.scrollX), y: Math.round(r.top + window.scrollY), w: Math.round(r.width), h: Math.round(r.height) }; })
"""


def measure(page) -> dict:
    return page.evaluate(MEASURE_JS, page.viewport_size["width"])


def summary(m: dict) -> str:
    bits = []
    if m["overflow"]:
        bits.append(f"overflow {m['scrollWidth']}>{m['innerWidth']}")
    if m["contrast_fail"]:
        bits.append("contrast<AA: " + "; ".join(f"{c['el']} {c['ratio']}" for c in m["contrast_fail"][:3]))
    if m["tap_small"]:
        bits.append(f"tap<44px: {len(m['tap_small'])}")
    if m["unlabeled"]:
        bits.append("unlabeled: " + ", ".join(m["unlabeled"][:3]))
    if m["h1"] != 1:
        bits.append(f"h1={m['h1']}")
    return "ok" if not bits else " | ".join(bits)


def viewport_of(html: str):
    m = re.search(r'<meta name="viewport-px" content="(\d+)x(\d+)"', html)
    return (int(m[1]), int(m[2])) if m else (1440, 900)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--uc", nargs="*", default=None)
    ap.add_argument("--kind", nargs="*", default=["wireframes", "mockups"])
    args = ap.parse_args()
    ucs = args.uc or sorted(p.name for p in UI.glob("UC-0*") if p.is_dir())
    rep_dir = HERE / "reports"
    rep_dir.mkdir(exist_ok=True)
    rows, spots = [], []
    with sync_playwright() as pw:
        browser = pw.chromium.launch(channel="msedge")
        for uc in ucs:
            for kind in args.kind:
                for html_path in sorted((UI / uc / kind).glob("*.html")):
                    w, h = viewport_of(html_path.read_text(encoding="utf-8"))
                    ctx = browser.new_context(viewport={"width": w, "height": h}, device_scale_factor=1,
                                              is_mobile=w < 600, has_touch=w < 600)
                    pg = ctx.new_page()
                    pg.goto(html_path.as_uri())
                    pg.add_style_tag(content=".summary-bar{position:static !important}")
                    pg.screenshot(path=str(html_path.with_suffix(".png")), full_page=True)
                    m = measure(pg)
                    rows.append({"uc": uc, "kind": kind, "screen": html_path.stem, "viewport": f"{w}x{h}",
                                 "overflow": m["overflow"], "contrast_min": m["contrast_min"],
                                 "contrast_fail": len(m["contrast_fail"]), "tap_small": len(m["tap_small"]),
                                 "unlabeled": len(m["unlabeled"]), "h1": m["h1"], "summary": summary(m)})
                    if kind == "mockups":
                        for s in pg.evaluate(HOTSPOT_JS):
                            spots.append({"uc": uc, "from": html_path.stem, **s})
                    ctx.close()
        browser.close()
    # one report file per UC and kind, so two renders of different UCs never overwrite each other
    cols = ["uc", "kind", "screen", "viewport", "overflow", "contrast_min", "contrast_fail", "tap_small", "unlabeled", "h1", "summary"]
    scols = ["uc", "from", "goto", "trigger", "label", "x", "y", "w", "h"]
    for uc in ucs:
        for kind in args.kind:
            part = [r for r in rows if r["uc"] == uc and r["kind"] == kind]
            with (rep_dir / f"render_{uc}_{kind}.csv").open("w", encoding="utf-8", newline="") as f:
                wr = csv.DictWriter(f, fieldnames=cols)
                wr.writeheader()
                wr.writerows(part)
        if "mockups" in args.kind:
            with (rep_dir / f"hotspots_{uc}.csv").open("w", encoding="utf-8", newline="") as f:
                wr = csv.DictWriter(f, fieldnames=scols)
                wr.writeheader()
                wr.writerows([x for x in spots if x["uc"] == uc])
    for r in rows:
        print(r["uc"], r["kind"], r["screen"], r["viewport"], r["summary"])


if __name__ == "__main__":
    sys.exit(main())
