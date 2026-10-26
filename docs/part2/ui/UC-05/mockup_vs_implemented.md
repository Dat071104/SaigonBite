Author: 722I0004 · AI-assisted (Claude Sonnet 5.5). Compared on 27/10/2026 at runtime commit 252ada1 (`_kit/compare.py`, `_kit/reports/mockup_vs_implemented.csv`).

The mockups were authored after the draft screens existed and show the refined target; the implemented screenshots were taken from the real app after the refinement commits. A mockup uses the case of the 'before' run, the implemented screen the case of the final run, so order numbers and clock times can differ; they are masked in the comparison.

| Screen | Text identical to the real screen | Measured on the real screen (overflow, lowest contrast, taps under 44 px) | Difference |
|---|---|---|---|
| UC-05-S01 | yes | no overflow, 5.71:1, 0 | none |
| UC-05-S02 | yes | no overflow, 5.71:1, 0 | none |
| UC-05-S03 | yes | no overflow, 5.43:1, 0 | none |
| UC-05-S04 | yes | no overflow, 5.43:1, 0 | none |
| UC-05-S05 | yes | no overflow, 5.71:1, 0 | none |
| UC-05-S06 | yes | no overflow, 5.71:1, 0 | none |
| UC-05-S07 | yes | no overflow, 5.43:1, 0 | none |
| UC-05-S08 | yes | no overflow, 5.43:1, 0 | none |
| UC-05-S09 | yes | no overflow, 5.71:1, 0 | none |

Differences between the draft and the implemented screens that were **implemented** (commit on branch `part2`):

| Change | Commit | Screens |
|---|---|---|
| R1 kitchen card buttons and order links at least 44 px | 36dc8f0, 4298973 | UC-05-S01 |
| R2 My orders one row per order; the 'Your answer needed' badge stays on the screen (the table was 449 px wide) | a160bf5 | UC-05-S05 |
| R6 'Cancel this order' danger outline | c749dce | UC-05-S06 to S09 |
| R5 readable payment option names on the order pages | d86eb3b | order pages of online orders |
| P5-D05 a rejected online payment is a 'refund owed, payout pending' | 252ada1 | order page of a rejected online order |

Kept as **design notes** (not implemented, reason):

- P5-D06 (open, owner decision): the decline banner always speaks of an online refund, also for a cash order. The text is in `order.py`, sealed by the G4 dependency policy.
- The offer panel wording is kept (the app rejects the order when the customer declines).
