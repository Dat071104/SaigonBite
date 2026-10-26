"""Write docs/part2/report/IV_4-3-3_ui_design.md (report section 4.3.3) from screens.csv, the trace tables and links.json.

Author: 722I0004 · AI-assisted (Claude Sonnet 5.5). The assembled IV_system_requirements_implementation.md is not edited; P7 assembles.
"""
import csv
import json
import re
from pathlib import Path

UI = Path(__file__).resolve().parents[1]
REPORT = UI.parent / "report" / "IV_4-3-3_ui_design.md"
AUTHOR = "722I0004 · AI-assisted (Claude Sonnet 5.5)"
links = json.loads(Path(r"D:\RAD\FINAL\Part2\content\links.json").read_text(encoding="utf-8"))
figma = links.get("figma_prototype", "PENDING")
figma_text = f"[{figma}]({figma})" if figma.startswith("http") else "PENDING (owner): the Figma file is built by the owner from `docs/part2/ui/figma_kit/` (steps in `FIGMA_STEPS.md`); the link is written here and in `Part2/content/links.json` only after it opens without signing in"
screens = list(csv.DictReader((UI / "screens.csv").open(encoding="utf-8")))
UCNAME = {"UC-01": "Place an order", "UC-05": "Confirm or reject an order (kitchen) and answer a replacement (customer)", "UC-02": "Deliver an order",
          "UC-03": "Manage hubs and kitchen capacity", "UC-06": "Manage brands and menu items", "UC-04": "Produce management reports"}
ORDER = ["UC-01", "UC-05", "UC-02", "UC-03", "UC-06", "UC-04"]

L = ["# 4.3.3 User interface design: from the sketch to the prototype and the SSD-to-UI trace", "",
     f"Author: {AUTHOR}", "",
     "**How this section was made, in order.** The first screens of the application were built during the draft build (I1 to P4). Phase P5.1 then photographed all 47 in-scope screens, "
     "measured and criticised them (`docs/part2/ui/_before/critique.md`), authored a wireframe and a mockup for every goal screen and key alternative as HTML/CSS with AI assistance, "
     "refined the real application where a measurement or an SSD result called for it (`docs/part2/ui/refinement_log.md`, 10 commits on branch `part2`) and photographed the real screens again. "
     "This is **UI design refinement after the draft build**; the real creation date of every artifact is in the `trace.md` of its use case (27/10/2026 for all wireframes, mockups and implemented screenshots; the sketches are the owner's and are not yet drawn).", "",
     "**Honest status of the progression.** Sketch: the brief for each use case exists (`UC-0x/sketch_brief.md`); the drawings are the owner's step and are `OWNER-PENDING`. "
     "Wireframe and mockup: authored as HTML/CSS and exported to PNG; they are not drawn natively in Figma. Prototype: " + figma_text + ". "
     "The Figma kit (frames named `UC0x-Snn <screen name>`, `flows.csv` with 148 hotspots measured from the mockup pages, start frames) is ready in `docs/part2/ui/figma_kit/`.", "",
     "**How the SSD became the UI.** Each use case has one table that follows every SSD operation occurrence (41 in all: the three `listCatalogue` occurrences are kept apart) to the screen and control that carries it, "
     "the inputs and the validation rules, the displayed result and the controller method (from the checked route/controller map; every controller call was verified against the view code). "
     "All 41 occurrences have at least one screen (`docs/part2/ui/coverage_check.md`). The implemented screens are Demonstrated by the browser run in `docs/part2/test_report/integration_2026-10-27/README.md` (60 of 60 steps, seven scenarios and the CSRF check).", ""]
for uc in ORDER:
    own = [s for s in screens if s["uc"] == uc]
    trace = (UI / uc / "trace.md").read_text(encoding="utf-8")
    table = trace.split("| SSD op (occurrence)", 1)[1].split("\n\n", 1)[0]
    table = "| SSD op (occurrence)" + table
    mvi = (UI / uc / "mockup_vs_implemented.md").read_text(encoding="utf-8")
    impl_table = re.search(r"\| Change \| Commit \| Screens \|.*?(?=\n\n)", mvi, re.S)
    n = uc.replace("-", "")
    L += [f"## 4.3.3.{ORDER.index(uc) + 1} {uc} {UCNAME[uc]}", "", f"Author: {AUTHOR}. Use case description: `docs/part2/{uc}/description.md`. Package: `docs/part2/ui/{uc}/`.", "",
          f"Progression: sketch (owner, `OWNER-PENDING`; brief `docs/part2/ui/{uc}/sketch_brief.md`) → wireframe → mockup → prototype ({'PENDING (owner)' if not figma.startswith('http') else figma}) → implemented screen. "
          f"{len(own)} screens: " + ", ".join(f"{s['screen_id']} ({s['kind']})" for s in own) + ".", ""]
    for s in own:
        sid = s["screen_id"]
        ref = sid.replace("UC-", "")
        L += [f"### {sid} {s['name']}", "", f"Role {s['role'].lower().replace('_', ' ')}, {s['viewport']}, routes {s['routes']}, SSD operations {s['ssd_ops']}, template `{s['template']}`.", "",
              f"![Wireframe {sid}](../ui/{uc}/wireframes/{sid}.png)", "", f"Figure 4.3.3-W{ref}. Wireframe of {s['name']}. Author: {AUTHOR}", "",
              f"![Mockup {sid}](../ui/{uc}/mockups/{sid}.png)", "", f"Figure 4.3.3-M{ref}. Mockup of {s['name']} (real names and amounts taken from the running app). Author: {AUTHOR}", "",
              f"![Implemented {sid}](../ui/{uc}/implemented/{sid}.png)", "", f"Figure 4.3.3-I{ref}. Implemented screen of {s['name']}, real application, local Flask development server, Edge, commit 252ada1. Author: {AUTHOR}", ""]
    L += [f"### {uc} SSD operation to UI trace", "", table, "", f"### {uc} refinement after the draft build", "",
          "The mockups show the refined design; these differences between the draft and the implemented screens were implemented (commit on branch `part2`):", "",
          (impl_table[0] if impl_table else "see `mockup_vs_implemented.md`"), "", f"Full comparison, design notes and artifact dates: `docs/part2/ui/{uc}/mockup_vs_implemented.md` and `trace.md`.", ""]
L += ["## 4.3.3.7 Prototype link", "", f"Prototype (Figma): {figma_text}.", "",
      "## 4.3.3.8 Integration evidence for the implemented screens", "",
      "The seven integration scenarios of the plan and a CSRF check were run in the browser at commit 252ada1, one browser profile per role, following the same order across roles: "
      "`docs/part2/test_report/integration_2026-10-27/README.md` (60 of 60 steps; label Demonstrated). Five defects found on the way were fixed with a regression test "
      "(P5-D01 to P5-D05); two low items are reported to the owner (P5-D03 remainder, P5-D06). Deployment is not claimed here (phase P6).", ""]
REPORT.write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")
print(len(L), "lines;", REPORT.stat().st_size, "bytes")
