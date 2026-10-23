"""Validate the Phase 1 evidence structure, not the application."""
from pathlib import Path
import csv
import json
import re
import xml.etree.ElementTree as ET
from PIL import Image
from pypdf import PdfReader

ROOT = Path(r"D:\RAD\FINAL")
REPO = ROOT / "SaigonBite"
DOC = REPO / "docs/part2"


def words(value):
    return re.findall(r"[a-z0-9]+", value.lower())


def main():
    with (DOC / "traceability.csv").open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        assert reader.fieldnames == ["Req ID", "source", "UC/SUC", "PC/MG ID", "activity/SSD/state ref",
                                     "design operation", "screen/control", "code method", "test ID",
                                     "result evidence", "report section", "actual author", "status"]
        rows = list(reader)
    assert len({r["Req ID"] for r in rows}) == len(rows)
    fr = [r for r in rows if r["Req ID"].startswith("FR-")]
    nfr = [r for r in rows if r["Req ID"].startswith("NFR-")]
    assert 30 <= len(fr) <= 45, len(fr)
    assert 8 <= len(nfr) <= 12, len(nfr)
    for row in rows:
        assert row["source"] and row["UC/SUC"], row
        assert re.search(r"(?:SUC|UC)-\d{2}", row["UC/SUC"]), row
        assert row["actual author"] == "722I0004" and row["status"] == "Planned", row
        for col in list(reader.fieldnames)[3:10]:
            assert row[col] == "", (row["Req ID"], col, row[col])
    corpus = "\n".join(r["UC/SUC"] for r in fr)
    for prefix, count in [("UC", 6), ("SUC", 9)]:
        for num in range(1, count + 1):
            assert re.search(rf"(?<![A-Z]){prefix}-{num:02d}(?!\d)", corpus), (prefix, num)
    sources = "\n".join(r["source"] for r in fr)
    for num in range(1, 27):
        assert f"BR-{num:02d}" in sources, f"BR-{num:02d} missing"
    parts = sorted((DOC / "report").glob("I_1*.md"))
    for path in parts:
        text = path.read_text(encoding="utf-8")
        assert "Author: 722I0004" in text and "AI-assisted" in text, path
        assert not re.search(r"[\u3400-\u9fff]", text), path
        if "⟦ACTUAL" in text:
            assert path.name == "I_1-4_narrative_assumptions.md", path
            assert text.count("⟦ACTUAL") == 1 and "Part 1 wording (historical)" in text, path
            assert "The placeholder above is not a current fact" in text and "523K0050 Nguyen Minh Quan" in text, path
    assembly = (DOC / "report/I_business_requirements.md").read_text(encoding="utf-8")
    headings = ["1.1 System Vision and Approval Record", "1.2 Organization Chart / Project Chart / Gantt Chart",
                "1.3 Iteration Plan, User Story Backlog and Risks", "1.4 Business Modelling / Requirements",
                "1.5 Business Processes / Flowchart of Requirements", "1.6 Activity Diagram", "1.7 List of Requirements"]
    offsets = [assembly.index(h) for h in headings]
    assert offsets == sorted(offsets)
    case = words(" ".join(p.extract_text() for p in PdfReader(ROOT / "Lec_re/RAD_Sem01_2627_Case_Study_SaigonBite.pdf").pages))
    grams = {tuple(case[i:i + 9]) for i in range(len(case) - 8)}
    overlaps = {}
    for path in parts:
        w = words(path.read_text(encoding="utf-8"))
        matches = sorted({" ".join(w[i:i + 9]) for i in range(len(w)-8) if tuple(w[i:i+9]) in grams})
        if matches:
            overlaps[path.name] = matches
    images = []
    for path in sorted((REPO / "models/shared").glob("*.png")):
        with Image.open(path) as img:
            images.append({"name": path.name, "size": list(img.size)})
    for path in (REPO / "models/shared").glob("*.drawio"):
        ET.parse(path)
    result = {"FR": len(fr), "NFR": len(nfr), "trace_rows": len(rows),
              "all_6_UCs_and_9_SUCs": True, "BR_01_to_26_in_FR_sources": True,
              "future_trace_fields_blank": True, "assembly_headings_in_order": True,
              "case_9_word_overlap_candidates": overlaps, "images": images,
              "note": "Overlap candidates require human review. PNG dimensions are not a visual signoff."}
    (ROOT / "Part2/notes/P1_structure_check.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
