Author: 722I0004 · AI-assisted (Claude Sonnet 5.5). Compared on 27/10/2026 at runtime commit 252ada1 (`_kit/compare.py`, `_kit/reports/mockup_vs_implemented.csv`).

The mockups were authored after the draft screens existed and show the refined target; the implemented screenshots were taken from the real app after the refinement commits. A mockup uses the case of the 'before' run, the implemented screen the case of the final run, so order numbers and clock times can differ; they are masked in the comparison.

| Screen | Text identical to the real screen | Measured on the real screen (overflow, lowest contrast, taps under 44 px) | Difference |
|---|---|---|---|
| UC-02-S01 | yes | no overflow, 5.71:1, 0 | none |
| UC-02-S02 | yes | no overflow, 5.71:1, 0 | none |
| UC-02-S03 | yes | no overflow, 5.43:1, 0 | none |
| UC-02-S04 | yes | no overflow, 5.71:1, 0 | none |
| UC-02-S05 | yes | no overflow, 5.71:1, 0 | none |
| UC-02-S06 | yes | no overflow, 5.43:1, 0 | none |
| UC-02-S07 | yes | no overflow, 5.43:1, 0 | none |

Differences between the draft and the implemented screens that were **implemented** (commit on branch `part2`):

| Change | Commit | Screens |
|---|---|---|
| R4 shipper cards are surfaces, the cash to collect is a 20 px bold figure, the action is full width on a phone, 'Order 3' no longer wraps | d053ca5 | UC-02-S01 |
| The order number on a waiting card opens the delivery page (OP-22 viewDelivery was not reachable from the board) | 0a594bf | UC-02-S01 to S02 |
| A finished delivery no longer says 'Collect 70,000 VND in cash' | 6970f0f | UC-02-S06, S07 |
| P5-D03 the error page after a lost pick-up links to 'Back to deliveries' | 1776293 | UC-02-S04 |
| R1 44 px targets | 36dc8f0, 4298973 | all screens |

Kept as **design notes** (not implemented, reason):

- P5-D03 (remainder, open, owner decision): after a lost pick-up the red banner and the 403 box are both shown, because the redirect lives in `delivery.py`, sealed by the G4 dependency policy.
