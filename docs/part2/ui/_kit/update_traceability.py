"""Append the P5 screen ids and browser evidence to docs/part2/traceability.csv (screen/control and result evidence cells only).

Author: 722I0004 · AI-assisted (Claude Sonnet 5.5)

Only rows that P5 really covers are touched: functional rows whose screen/control names an endpoint of the 41-row SSD map (the screen
ids come from screens.csv), and the non-functional rows 01, 06, 09, 11, 12 that the browser run or the width measurements show.
Statuses are not changed (the status vocabulary stays); the original file is snapshotted in Part2/notes/P5/traceability_original.csv.
Run once; it refuses to append twice.
"""
import csv
import re
from pathlib import Path

UI = Path(__file__).resolve().parents[1]
TRACE = UI.parent / "traceability.csv"
MAP = Path(r"D:\RAD\FINAL\Part2\notes\P4_B02\actual_route_controller_SSD_map.csv")
EV = "docs/part2/test_report/integration_2026-10-27/README.md"
TAG = "P5 (final run at 252ada1, 60 of 60 steps)"

screens = list(csv.DictReader((UI / "screens.csv").open(encoding="utf-8")))
smap = list(csv.DictReader(MAP.open(encoding="utf-8")))
by_endpoint = {}
for r in smap:
    occ = r["UC"] + "#" + r["SSD_identity"].rsplit("#", 1)[1]
    for s in screens:
        if occ in s["occurrences"].split():
            by_endpoint.setdefault(r["actual_endpoint"], set()).add(s["screen_id"])

STEPS = {
    "UC-01": "S1 1.4-1.9, S2 2.2-2.5, S3 3.1, S6 6a-6c, S7 7.8",
    "UC-02": "S5 5.1-5.5, S6 6d.1-6d.3",
    "UC-03": "S1 1.1-1.2, S2 2.1-2.3 and 2.7",
    "UC-04": "S7 7.1-7.5 (oracle figures), 7.6 and 7.8",
    "UC-05": "S3 3.2-3.6, S4 4.1-4.7, S6 6b.2",
    "UC-06": "S1 1.3 and 1.5-1.8, S4 4.1 and 4.7",
}
OVERRIDE = {"FR-35": "S1 1.3 and 1.5-1.8, S4 4.1 and 4.7", "FR-36": "S1 1.3 and 1.5-1.8", "FR-37": "S1 1.3 and 1.5-1.8, S4 4.1 and 4.7"}
NFR = {
    "NFR-01": (None, f"{TAG}: S3 3.4-3.5 (the other hub's kitchen refused with 403, nothing changed), S5 5.2 (the second shipper refused), {EV}"),
    "NFR-06": (None, f"{TAG}: S8 8.1-8.5, 340 post forms seen all with a CSRF token, a missing or changed token gives HTTP 400 and changes nothing, {EV}"),
    "NFR-09": ("Phone screens UC-01-S01..S12, UC-05-S05..S09, UC-02-S01..S07 at 390 px (docs/part2/ui/UC-0x/implemented/)",
               f"P5.1: no horizontal overflow at 390 px on any phone screen and at 360 px on My orders, all targets at least 44 px (docs/part2/ui/_kit/captured/implemented/measure.csv, docs/part2/ui/_kit/reports/width_before_after.csv); status unchanged"),
    "NFR-11": (None, f"{TAG}: S7 7.7-7.9 (archive a closed order; history, receipt and totals kept; an open order refused), {EV}"),
    "NFR-12": (None, f"{TAG}: S3, S4 and S5 follow one order across customer, kitchen and two shippers in their own profiles (same order id 11), {EV}"),
}

with TRACE.open(encoding="utf-8", newline="") as f:
    rows = list(csv.reader(f))
head = rows[0]
iS, iE, iU = head.index("screen/control"), head.index("result evidence"), head.index("UC/SUC")
changed = 0
for r in rows[1:]:
    if "docs/part2/ui/" in r[iS] or "P5 (final run" in r[iE] or "P5.1:" in r[iE]:
        raise SystemExit("already applied")
    rid = r[0]
    if rid in NFR:
        screen_text, evidence = NFR[rid]
        if screen_text:
            r[iS] = r[iS] + " | " + screen_text
        r[iE] = r[iE] + "; " + evidence
        changed += 1
        continue
    if not rid.startswith("FR-"):
        continue
    ends = sorted({e for e in re.findall(r"\b(?:order|kitchen|delivery|admin|reports)\.\w+", r[iS])})
    ids = sorted({sid for e in ends for sid in by_endpoint.get(e, ())})
    if not ids:
        continue
    uc = next((u for u in re.findall(r"\bUC-0\d\b", r[iU])), None)
    steps = OVERRIDE.get(rid) or STEPS.get(uc)
    r[iS] = r[iS] + " | UI screens: " + ", ".join(ids) + " (docs/part2/ui/screens.csv; trace in docs/part2/ui/UC-0x/trace.md)"
    r[iE] = r[iE] + f"; Demonstrated in the browser, {TAG}: {steps}, {EV}"
    changed += 1
with TRACE.open("w", encoding="utf-8", newline="") as f:
    csv.writer(f, lineterminator="\r\n").writerows(rows)
print(changed, "rows updated")
