"""Write UC-0x/mockup_vs_implemented.md from reports/mockup_vs_implemented.csv and captured/implemented/measure.csv.
Author: 722I0004 · AI-assisted (Claude Sonnet 5.5)"""
import csv
from pathlib import Path

HERE = Path(__file__).resolve().parent
UI = HERE.parent
cmp_rows = {r["screen"]: r for r in csv.DictReader((HERE / "reports" / "mockup_vs_implemented.csv").open(encoding="utf-8"))}
meas = {r["screen"]: r for r in csv.DictReader((HERE / "captured" / "implemented" / "measure.csv").open(encoding="utf-8"))}
screens = list(csv.DictReader((UI / "screens.csv").open(encoding="utf-8")))

SHORT = {  # screens where the mockup deliberately shows a subset of a long real list
    "UC-01-S03": "the mockup shows the Com Tam Corner brand only (3 of the 8 dishes); the real menu lists all three brands",
    "UC-01-S11": "the mockup shows 5 of the 9 real orders",
    "UC-06-S01": "the mockup shows 5 dishes of the real catalogue",
    "UC-06-S02": "the mockup shows a subset of the real dish rows",
    "UC-06-S06": "the mockup shows 4 hub-menu rows of the real list",
    "UC-06-S07": "the mockup shows a subset of the real hub-menu rows",
    "UC-06-S08": "the mockup shows a subset of the real dish rows",
}
IMPLEMENTED = {
    "UC-01": [
        ("R1 tap targets of at least 44 px (role links, wordmark, action links)", "36dc8f0, 4298973", "all screens"),
        ("R2 My orders is one row per order on a phone; the table was 449 px wide on a 390 px screen", "a160bf5", "UC-01-S11"),
        ("R5 online options named E-wallet, Bank QR code, International card instead of 'e wallet', 'bank qr'", "d86eb3b", "UC-01-S04, S05, S06, S07"),
        ("R6 'Cancel this order' is an outline in the danger colour, still behind a confirmation", "c749dce", "UC-01-S09"),
        ("P5-D04 the quote table prints 0.39 km, not 0.38971718085988794 km", "5466f6a", "UC-01-S04, S05, S07"),
        ("P5-D02 choosing online payment goes straight to the simulator, without a false 'price changed' notice", "ce18bf6", "UC-01-S04 to S06"),
    ],
    "UC-05": [
        ("R1 kitchen card buttons and order links at least 44 px", "36dc8f0, 4298973", "UC-05-S01"),
        ("R2 My orders one row per order; the 'Your answer needed' badge stays on the screen (the table was 449 px wide)", "a160bf5", "UC-05-S05"),
        ("R6 'Cancel this order' danger outline", "c749dce", "UC-05-S06 to S09"),
        ("R5 readable payment option names on the order pages", "d86eb3b", "order pages of online orders"),
        ("P5-D05 a rejected online payment is a 'refund owed, payout pending'", "252ada1", "order page of a rejected online order"),
    ],
    "UC-02": [
        ("R4 shipper cards are surfaces, the cash to collect is a 20 px bold figure, the action is full width on a phone, 'Order 3' no longer wraps", "d053ca5", "UC-02-S01"),
        ("The order number on a waiting card opens the delivery page (OP-22 viewDelivery was not reachable from the board)", "0a594bf", "UC-02-S01 to S02"),
        ("A finished delivery no longer says 'Collect 70,000 VND in cash'", "6970f0f", "UC-02-S06, S07"),
        ("P5-D03 the error page after a lost pick-up links to 'Back to deliveries'", "1776293", "UC-02-S04"),
        ("R1 44 px targets", "36dc8f0, 4298973", "all screens"),
    ],
    "UC-03": [("R1 44 px targets for the role links and the Edit, Menu and Archive row actions", "36dc8f0, 4298973", "UC-03-S01, S03, S06"),
              ("P5-D01 the numeric fields of the hub form accept their saved values (checked in the browser run)", "b68bfef (dish form; hub form was already correct)", "UC-03-S02")],
    "UC-06": [("R1 44 px targets for the 20 or more Edit and Archive row actions", "36dc8f0, 4298973", "UC-06-S01, S02, S06, S07, S08"),
              ("P5-D01 the dish price field accepts 60,000 VND and every other seed price", "b68bfef", "UC-06-S03, S04, S05")],
    "UC-04": [("R3 the sales table scrolls inside its own labelled box (967 px wide at 768 px)", "7baeb74", "UC-04-S01, S04"),
              ("A zero voucher total is '0 VND', not '-0 VND'", "dc87741", "UC-04-S04"),
              ("R1 44 px targets for the report links", "36dc8f0, 4298973", "all screens")],
}
KEPT = {
    "UC-01": ["Cancel stays a plain button with a browser confirmation (no custom dialog): enough for the SSD result.",
              "The step bar and the sticky total bar are kept as built; the figure shows the total bar in the flow of the page."],
    "UC-05": ["P5-D06 (open, owner decision): the decline banner always speaks of an online refund, also for a cash order. The text is in `order.py`, sealed by the G4 dependency policy.",
              "The offer panel wording is kept (the app rejects the order when the customer declines)."],
    "UC-02": ["P5-D03 (remainder, open, owner decision): after a lost pick-up the red banner and the 403 box are both shown, because the redirect lives in `delivery.py`, sealed by the G4 dependency policy."],
    "UC-03": ["The capacity range ('1 to 500') stays as hint text beside the field; the refusal screen (S05) needs a request that skips the browser's own max check."],
    "UC-06": ["Archived brands and dishes stay listed and muted; no reparenting of a dish (the form pins the brand)."],
    "UC-04": ["Empty period and invalid filter are kept as built (n/a figures, error next to the filter)."],
}


def write(uc):
    own = [s for s in screens if s["uc"] == uc]
    L = [f"Author: 722I0004 · AI-assisted (Claude Sonnet 5.5). Compared on 27/10/2026 at runtime commit 252ada1 (`_kit/compare.py`, `_kit/reports/mockup_vs_implemented.csv`).", "",
         "The mockups were authored after the draft screens existed and show the refined target; the implemented screenshots were taken from the real app after the refinement commits. "
         "A mockup uses the case of the 'before' run, the implemented screen the case of the final run, so order numbers and clock times can differ; they are masked in the comparison.", "",
         "| Screen | Text identical to the real screen | Measured on the real screen (overflow, lowest contrast, taps under 44 px) | Difference |", "|---|---|---|---|"]
    for s in own:
        sid = s["screen_id"]
        c, m = cmp_rows[sid], meas[sid]
        same = not c["only_in_mockup"] and not c["only_in_implemented"]
        note = "none" if same else SHORT.get(sid, "see comparison csv")
        L.append(f"| {sid} | {'yes' if same else 'no, see Difference'} | {'overflow' if m['overflow'] == 'True' else 'no overflow'}, {m['contrast_min']}:1, {m['tap_small']} | {note} |")
    L += ["", "Differences between the draft and the implemented screens that were **implemented** (commit on branch `part2`):", "",
          "| Change | Commit | Screens |", "|---|---|---|"]
    L += [f"| {a} | {b} | {c} |" for a, b, c in IMPLEMENTED[uc]]
    L += ["", "Kept as **design notes** (not implemented, reason):", ""] + [f"- {x}" for x in KEPT[uc]]
    (UI / uc / "mockup_vs_implemented.md").write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")


for uc in sorted(IMPLEMENTED):
    write(uc)
print("written")
