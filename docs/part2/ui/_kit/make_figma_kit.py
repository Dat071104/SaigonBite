"""Prepare docs/part2/ui/figma_kit/ for the owner: frames named 'UC0x-Snn <screen name>', flows.csv, FIGMA_STEPS.md.

Author: 722I0004 · AI-assisted (Claude Sonnet 5.5)

No tool in this session can write to Figma, so the Figma file is the owner's step. The wireframes and mockups were authored as
HTML/CSS (AI-assisted); in Figma they are only imported, assembled and linked. They were not drawn natively in Figma.
"""
import csv
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
UI = HERE.parent
OUT = UI / "figma_kit"
screens = list(csv.DictReader((UI / "screens.csv").open(encoding="utf-8")))
name = {s["screen_id"]: f"{s['screen_id'].replace('UC-', 'UC')} {s['name']}".replace(":", " -").replace("/", "-") for s in screens}

if OUT.exists():
    shutil.rmtree(OUT)
for page, kind in (("2_Wireframe", "wireframes"), ("3_Mockup", "mockups"), ("4_Prototype", "mockups")):
    (OUT / page).mkdir(parents=True)
    for s in screens:
        src = UI / s["uc"] / kind / f"{s['screen_id']}.png"
        shutil.copy(src, OUT / page / f"{name[s['screen_id']]}.png")
(OUT / "1_Sketch").mkdir()
(OUT / "1_Sketch" / "README.md").write_text(
    "OWNER-PENDING. This page is for your own sketches (paper photos or Figma freehand), one per `UC-0x/sketch_brief.md` row. "
    "No sketch image has been generated or imitated. Put your photos in `docs/part2/ui/UC-0x/sketch/` as well, with the real date.\n", encoding="utf-8")

rows = []
for uc in sorted({s["uc"] for s in screens}):
    with (HERE / "reports" / f"hotspots_{uc}.csv").open(encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f):
            if r["goto"] not in name:
                continue
            rows.append({"UC": uc, "from frame": name[r["from"]], "hotspot label": r["label"], "x": r["x"], "y": r["y"], "w": r["w"], "h": r["h"],
                         "to frame": name[r["goto"]], "trigger": r["trigger"]})
with (OUT / "flows.csv").open("w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader()
    w.writerows(rows)

starts = {}
for s in screens:
    starts.setdefault(s["uc"], name[s["screen_id"]])
steps = f"""# Build the Figma prototype (owner step, about 45 minutes)

Author: 722I0004 · AI-assisted (Claude Sonnet 5.5). The frames in this folder are **HTML/CSS wireframes and mockups authored with AI assistance and exported to PNG**.
In Figma you only import, assemble and link them; do not describe them as drawn natively in Figma. Dates of each artifact: `UC-0x/trace.md`.

1. In Figma create a file `SaigonBite Part 2 UI`, with four pages: **Sketch**, **Wireframe**, **Mockup**, **Prototype**.
2. Sketch: draw (paper or freehand) the screens listed in each `UC-0x/sketch_brief.md` and put the photos on this page. Nothing is generated for you.
3. Wireframe and Mockup: drag the PNG files of `2_Wireframe` and `3_Mockup` onto the page (File > Place image). Keep the file names: they are the frame names. Phone frames are 390 wide, staff frames 1440 wide; keep 1x.
4. Prototype: drag the files of `4_Prototype` (the mockup frames) onto the page, one row per use case.
5. For every row of `flows.csv` (UC, from frame, x, y, w, h in frame pixels, to frame, trigger): in the Prototype page add a rectangle at (x, y) with size (w, h) inside the *from frame*, no fill, then in Prototype mode drag its handle to the *to frame* (On click, Navigate to, instant). There are {len(rows)} hotspots.
6. Start frame of each use case (Prototype settings > Flow starting point):
""" + "\n".join(f"   - {uc}: `{n}`" for uc, n in starts.items()) + """
7. Share: Share > General access **Anyone with the link** > **Can view**; copy the link of the Prototype (Share prototype).
8. Paste the link into `Part2/content/links.json` under `figma_prototype` (replace `PENDING`), then tell Claude to run the logged-out check: it opens the link in a fresh private context, confirms each start frame, and saves dated screenshots to `Part2/evidence/figma/`.

Until step 8 is done, the report says `PENDING (owner)` for the prototype link.
"""
(OUT / "FIGMA_STEPS.md").write_text(steps, encoding="utf-8", newline="\n")
print(len(screens) * 3, "frames,", len(rows), "hotspots,", len(starts), "start frames")
