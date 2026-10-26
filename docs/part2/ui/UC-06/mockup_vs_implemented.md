Author: 722I0004 · AI-assisted (Claude Sonnet 5.5). Compared on 27/10/2026 at runtime commit 252ada1 (`_kit/compare.py`, `_kit/reports/mockup_vs_implemented.csv`).

The mockups were authored after the draft screens existed and show the refined target; the implemented screenshots were taken from the real app after the refinement commits. A mockup uses the case of the 'before' run, the implemented screen the case of the final run, so order numbers and clock times can differ; they are masked in the comparison.

| Screen | Text identical to the real screen | Measured on the real screen (overflow, lowest contrast, taps under 44 px) | Difference |
|---|---|---|---|
| UC-06-S01 | no, see Difference | no overflow, 5.71:1, 0 | the mockup shows 5 dishes of the real catalogue |
| UC-06-S02 | no, see Difference | no overflow, 5.43:1, 0 | the mockup shows a subset of the real dish rows |
| UC-06-S03 | yes | no overflow, 5.71:1, 0 | none |
| UC-06-S04 | yes | no overflow, 5.71:1, 0 | none |
| UC-06-S05 | yes | no overflow, 5.71:1, 0 | none |
| UC-06-S06 | no, see Difference | no overflow, 5.43:1, 0 | the mockup shows 4 hub-menu rows of the real list |
| UC-06-S07 | no, see Difference | no overflow, 5.43:1, 0 | the mockup shows a subset of the real hub-menu rows |
| UC-06-S08 | no, see Difference | no overflow, 5.43:1, 0 | the mockup shows a subset of the real dish rows |

Differences between the draft and the implemented screens that were **implemented** (commit on branch `part2`):

| Change | Commit | Screens |
|---|---|---|
| R1 44 px targets for the 20 or more Edit and Archive row actions | 36dc8f0, 4298973 | UC-06-S01, S02, S06, S07, S08 |
| P5-D01 the dish price field accepts 60,000 VND and every other seed price | b68bfef | UC-06-S03, S04, S05 |

Kept as **design notes** (not implemented, reason):

- Archived brands and dishes stay listed and muted; no reparenting of a dish (the form pins the brand).
