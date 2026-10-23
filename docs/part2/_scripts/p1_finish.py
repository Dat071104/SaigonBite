"""Assemble and stage Phase 1 documents after the entire drafting wave ends."""
from pathlib import Path
import hashlib
import json
import re
import shutil

ROOT = Path(r"D:\RAD\FINAL")
REPO = ROOT / "SaigonBite"
DOC = REPO / "docs/part2"
AUTHOR = "Author: 722I0004 · AI-assisted (Codex)"


def refresh_rules():
    """Keep the locked rule wording intact and add separate trace columns."""
    plan = (ROOT / "PLAN_SaigonBite_Part2_Final.md").read_text(encoding="utf-8")
    old = (DOC / "rules.md").read_text(encoding="utf-8")
    index = old.split("## Assumption and question index", 1)[1].split("### 3.1", 1)[0]
    # The retained index ends just before the copied rule section.
    index = index.split("All values not fixed", 1)[0].strip()
    links = {}
    for line in index.splitlines():
        if line.startswith("| BR-"):
            cells = [c.strip() for c in line.strip("|").split("|")]
            links[cells[0]] = (cells[1], cells[2])
    source = plan.split("## 3. Business rules (frozen contracts)", 1)[1].split("## 4. State contracts", 1)[0]
    result = []
    for line in source.splitlines():
        if line.startswith("| ID |"):
            line = line.rstrip() + " Question / clarification | Tests |"
        elif line.startswith("|---"):
            line = line.rstrip() + "---|---|"
        elif line.startswith("| BR-"):
            rid = line.split("|")[1].strip()
            line = line.rstrip() + f" {links[rid][1]} | |"
        result.append(line)
    text = f"# Part 2 business rules\n\n{AUTHOR}\n\n"
    text += "Source: locked plan §3. Tests remain blank until P4. Trace links do not imply client confirmation.\n\n"
    text += "## Assumption and question index\n\n" + index + "\n\n" + "\n".join(result).strip() + "\n"
    (DOC / "rules.md").write_text(text, encoding="utf-8")
    print("Rules retained verbatim; separate question and Tests columns restored.")


def assemble():
    report = DOC / "report"
    names = ["I_1-1_vision.md", "I_1-2_org_gantt.md", "I_1-3_iterations_backlog_risks.md",
             "I_1-4_narrative_assumptions.md", "I_1-5_1-6_process.md", "I_1-7_requirements.md"]
    text = "# I. Business Requirements (1 point)\n\n" + AUTHOR + "\n\n"
    text += ("Phase 1 draft dated 23/10/2026. Template wording is retained; the primary marking rubric "
             "allocates 5 marks to this component. Client answers, lecturer feedback and future measurements "
             "remain pending. Analysis, design, implementation and test evidence will be added in their phases.\n\n")
    for name in names:
        part = (report / name).read_text(encoding="utf-8").strip()
        # Included sources live in the same directory, so relative image links remain valid.
        if part.startswith("# "):
            part = re.sub(r"(?m)^(#{1,5}) ", lambda match: "#" + match.group(1) + " ", part)
        text += part + "\n\n"
    (report / "I_business_requirements.md").write_text(text.rstrip() + "\n", encoding="utf-8")
    print("Assembled", len(names), "source parts in template order.")


def stage():
    base = ROOT / "Part2"
    work = base / "workbook/Team02_RAD_Sem01_2627_Team_Workbook.xlsx"
    dest = base / "drive_upload" / work.name
    shutil.copyfile(work, dest)
    target = base / "drive_upload/Part2/models"
    target.mkdir(parents=True, exist_ok=True)
    rows = []
    for source in sorted((REPO / "models/shared").iterdir()):
        if not source.is_file() or source.suffix.lower() not in (".drawio", ".png", ".svg", ".py", ".json"):
            continue
        copied = target / source.name
        shutil.copyfile(source, copied)
        assert copied.read_bytes() == source.read_bytes()
        rows.append({"file": str(copied), "sha256": hashlib.sha256(copied.read_bytes()).hexdigest()})
    data = {"workbook": str(dest), "workbook_sha256": hashlib.sha256(dest.read_bytes()).hexdigest(),
            "workbook_matches_working_copy": work.read_bytes() == dest.read_bytes(), "models": rows,
            "elearning_files": [str(p) for p in (base / "drive_upload/eLearning").rglob("*") if p.is_file()]}
    (base / "notes/P1_staging_manifest.json").write_text(json.dumps(data, indent=2), encoding="utf-8")
    print(json.dumps({"workbook_equal": data["workbook_matches_working_copy"],
                      "model_files": len(rows), "elearning_files": len(data["elearning_files"])}))


if __name__ == "__main__":
    import sys
    {"rules": refresh_rules, "assemble": assemble, "stage": stage}[sys.argv[1]]()
