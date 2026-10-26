Author: 722I0004 · AI-assisted (Claude Sonnet 5.5). Compared on 27/10/2026 at runtime commit 252ada1 (`_kit/compare.py`, `_kit/reports/mockup_vs_implemented.csv`).

The mockups were authored after the draft screens existed and show the refined target; the implemented screenshots were taken from the real app after the refinement commits. A mockup uses the case of the 'before' run, the implemented screen the case of the final run, so order numbers and clock times can differ; they are masked in the comparison.

| Screen | Text identical to the real screen | Measured on the real screen (overflow, lowest contrast, taps under 44 px) | Difference |
|---|---|---|---|
| UC-03-S01 | yes | no overflow, 5.43:1, 0 | none |
| UC-03-S02 | yes | no overflow, 5.71:1, 0 | none |
| UC-03-S03 | yes | no overflow, 5.43:1, 0 | none |
| UC-03-S04 | yes | no overflow, 5.71:1, 0 | none |
| UC-03-S05 | yes | no overflow, 5.71:1, 0 | none |
| UC-03-S06 | yes | no overflow, 5.43:1, 0 | none |

Differences between the draft and the implemented screens that were **implemented** (commit on branch `part2`):

| Change | Commit | Screens |
|---|---|---|
| R1 44 px targets for the role links and the Edit, Menu and Archive row actions | 36dc8f0, 4298973 | UC-03-S01, S03, S06 |
| P5-D01 the numeric fields of the hub form accept their saved values (checked in the browser run) | b68bfef (dish form; hub form was already correct) | UC-03-S02 |

Kept as **design notes** (not implemented, reason):

- The capacity range ('1 to 500') stays as hint text beside the field; the refusal screen (S05) needs a request that skips the browser's own max check.
