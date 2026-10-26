Author: 722I0004 · AI-assisted (Claude Sonnet 5.5). Compared on 27/10/2026 at runtime commit 252ada1 (`_kit/compare.py`, `_kit/reports/mockup_vs_implemented.csv`).

The mockups were authored after the draft screens existed and show the refined target; the implemented screenshots were taken from the real app after the refinement commits. A mockup uses the case of the 'before' run, the implemented screen the case of the final run, so order numbers and clock times can differ; they are masked in the comparison.

| Screen | Text identical to the real screen | Measured on the real screen (overflow, lowest contrast, taps under 44 px) | Difference |
|---|---|---|---|
| UC-04-S01 | yes | no overflow, 5.71:1, 0 | none |
| UC-04-S02 | yes | no overflow, 5.43:1, 0 | none |
| UC-04-S03 | yes | no overflow, 5.71:1, 0 | none |
| UC-04-S04 | yes | no overflow, 5.71:1, 0 | none |
| UC-04-S05 | yes | no overflow, 5.71:1, 0 | none |

Differences between the draft and the implemented screens that were **implemented** (commit on branch `part2`):

| Change | Commit | Screens |
|---|---|---|
| R3 the sales table scrolls inside its own labelled box (967 px wide at 768 px) | 7baeb74 | UC-04-S01, S04 |
| A zero voucher total is '0 VND', not '-0 VND' | dc87741 | UC-04-S04 |
| R1 44 px targets for the report links | 36dc8f0, 4298973 | all screens |

Kept as **design notes** (not implemented, reason):

- Empty period and invalid filter are kept as built (n/a figures, error next to the filter).
