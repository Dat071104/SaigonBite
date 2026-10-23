"""Create the Phase 1 contract records from the locked local sources."""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import openpyxl

ROOT = Path(r"D:\RAD\FINAL")
REPO = ROOT / "SaigonBite"
DOC = REPO / "docs/part2"
PLAN = (ROOT / "PLAN_SaigonBite_Part2_Final.md").read_text(encoding="utf-8")
AUTHOR = "Author: 722I0004 · AI-assisted (Codex)"


def write(name, value):
    target = DOC / name
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(value, encoding="utf-8")


def section(start, end):
    return PLAN.split(start, 1)[1].split(end, 1)[0].strip()


def main():
    rules = section("## 3. Business rules (frozen contracts)", "## 4. State contracts")
    lines = []
    for line in rules.splitlines():
        if line.startswith("| ID |"):
            line = line.rstrip("|") + " Q link | Tests |"
        elif line.startswith("|---"):
            line = line.rstrip("|") + "---|---|"
        elif line.startswith("| BR-"):
            rid = line.split("|")[1].strip()
            q = {"BR-01":"Q1", "BR-02":"Q1", "BR-03":"Q1", "BR-04":"Q1; Q2",
                 "BR-05":"Q2", "BR-06":"Q2", "BR-07":"Q2", "BR-14":"Q4; L2",
                 "BR-15":"Q3", "BR-17":"Q3", "BR-20":"Q5", "BR-21":"Q5",
                 "BR-22":"Q1; Q5", "BR-23":"Q5", "BR-24":"Q5"}.get(rid, "—")
            line = line.rstrip("|") + f" {q} | |"
        lines.append(line)
    write("rules.md", "# Part 2 business rules\n\n" + AUTHOR + "\n\nSource: locked plan §3. Tests remain blank until P4. Q links identify open questions, not client confirmation.\n\n" + "\n".join(lines) + "\n")
    decisions = section("## 1. Decisions (final)", "## 2. Scope, ownership and CRUD")
    qa = openpyxl.load_workbook(ROOT / "Part1_v2/drive_upload/Team02_RAD_Sem01_2627_Team_Workbook.xlsx", data_only=False)["Client Q&A"]
    qlines = ["| ID | Status in frozen workbook | Submitted date | Answer |", "|---|---|---|---|"]
    for row in qa.iter_rows(min_row=5, max_row=9, values_only=True):
        qlines.append(f"| {row[0]} | {row[7]} | ⟦PENDING: original submission date, Dat to confirm by 31/10⟧ | no answer yet |")
    decisions = decisions.replace("— asked 26/10", "— planned for 26/10; not yet asked as of 23/10")
    decisions = decisions.replace("On 31/10 write one entry", "Checkpoint entry: ⟦PENDING: answers and replan assessment, due 31/10⟧.\n\nOn 31/10 write one entry")
    j = "\n".join(line for line in PLAN.splitlines() if line.startswith("| J"))
    write("decision_log.md", "# Part 2 decision log\n\n" + AUTHOR + "\n\nRecorded 23/10/2026 from the locked plan. Plan evidence claims are attributed to the plan; no new approval is inferred.\n\n" + decisions + "\n\n## Client answer status at Phase 1\n\n" + "\n".join(qlines) + "\n\n## Accepted plan changes J1–J9\n\n| ID | Earlier position | Locked decision | Reason |\n|---|---|---|---|\n" + j + "\n\n## Phase 1 interpretations\n\n- A-08 is Superseded by D-4 (23/10, team decision), never lecturer approval.\n- Checklist identifiers 11/12/13/41 are values in marking Checklist column B, at Excel rows 24/25/26/56. Literal rows 11/12/13/41 do not describe the requested four items.\n- The template heading I. Business Requirements (1 point) is retained verbatim; the requirements PDF and marking rubric allocate 5 marks. No score is claimed.\n- The plan P1.2 future test linkage is completed in P2–P4; Phase 1 test/result cells remain blank per its checklist.\n")
    write("ai_usage_log.md", "# Part 2 Generative AI Usage Log\n\n" + AUTHOR + "\n\n| Tool + date | Purpose | Prompt summary | Kept / changed | How verified |\n|---|---|---|---|---|\n| Claude Opus, 23/10/2026 (plan attribution) | Initial Part 2 plan | Scope, phases, build/test/deploy strategy | Historical input; final locked plan supersedes it | Locked plan input list and §0; no claim of independent prompt recovery |\n| Sol, 23/10/2026 (plan attribution) | Plan reviews and acceptance | Audit code findings, contracts, authorship, scope | Accepted decisions recorded in locked plan | Review files in Part2_Plan_Review; source authorities |\n| Codex root, 23/10/2026 | Phase 1 preflight and integration | Execute P0/P1 only; preserve Part 1 and app bytes | Contract copies, baseline, workbook and final integration | Binary SHA-256, primary source inspection, trace checks, independent reviewer; results recorded at closure |\n\nFull Phase 1 prompt: D:/RAD/FINAL/Part2/codex/P1_PROMPT.md. Worker prompts and outputs are archived in Part2/notes; earlier full prompts not recovered remain pending for Dat if requested within 48 hours.\n")
    before = subprocess.check_output(["git", "rev-parse", "HEAD^"], cwd=REPO, text=True).strip()
    wip = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=REPO, text=True).strip()
    changes = subprocess.check_output(["git", "diff", "--name-status", "HEAD^", "HEAD"], cwd=REPO, text=True)
    manifest = json.loads((ROOT / "Part2/notes/P1_start_hashes.json").read_text())
    canonical = ROOT / "Part1_v2/drive_upload/eLearning/Team02_Proposal_for_SaigonBite.pdf"
    repo_copy = REPO / "docs/part1/Team02_Proposal_for_SaigonBite.pdf"
    equal = canonical.read_bytes() == repo_copy.read_bytes()
    write("baseline_2026-10-23.md", f"# Phase 1 baseline\n\n{AUTHOR}\n\nRecorded 23/10/2026 (Asia/Bangkok). Starting branch main; starting HEAD `{before}`. WIP baseline on part2: `{wip}`. The 81 existing draft changes were staged as explicit paths, inspected with staged diff/check, and scanned for prohibited artifacts and obvious secret signatures. No flagged paths/signatures were printed; diff --check exited 0. This preserves a red draft and does not qualify it.\n\nThe historical 8 accounts / 40 pages returning 200 result is **Reachable only**, not UC correctness. Historical 96 passing I1 tests at a3feb72 and F-01 collection failure are plan-attributed; pytest was not rerun or repaired in this phase.\n\nCanonical source is the eLearning staging proposal. Repository proposal byte equality: **{equal}**. Dat reports Part 1 submitted (plan P0.0); actual eLearning receipt remains ⟦PENDING: Dat supplies receipt outside frozen Part1_v2, before submission audit⟧.\n\nStart binary manifest: D:/RAD/FINAL/Part2/notes/P1_start_hashes.json. Boundary file counts: `{json.dumps({k:len(v) for k,v in manifest.items()})}`. Frozen Part1_v2 scope is broader than the required deliverables/models subset.\n\n## Preserved pre-existing draft\n\n```text\n{changes}```\n")
    source = ROOT / "Part1_v2/drive_upload/Team02_RAD_Sem01_2627_Team_Workbook.xlsx"
    target = ROOT / "Part2/workbook" / source.name
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        raise RuntimeError("Working workbook already exists; do not overwrite")
    shutil.copyfile(source, target)
    print("Preflight records created; canonical proposal equality:", equal)


if __name__ == "__main__":
    main()
