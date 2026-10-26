Author: 722I0004 · AI-assisted (Claude Sonnet 5.5). Compared on 27/10/2026 at runtime commit 252ada1 (`_kit/compare.py`, `_kit/reports/mockup_vs_implemented.csv`).

The mockups were authored after the draft screens existed and show the refined target; the implemented screenshots were taken from the real app after the refinement commits. A mockup uses the case of the 'before' run, the implemented screen the case of the final run, so order numbers and clock times can differ; they are masked in the comparison.

| Screen | Text identical to the real screen | Measured on the real screen (overflow, lowest contrast, taps under 44 px) | Difference |
|---|---|---|---|
| UC-01-S01 | yes | no overflow, 5.43:1, 0 | none |
| UC-01-S02 | yes | no overflow, 5.71:1, 0 | none |
| UC-01-S03 | no, see Difference | no overflow, 5.24:1, 0 | the mockup shows the Com Tam Corner brand only (3 of the 8 dishes); the real menu lists all three brands |
| UC-01-S04 | yes | no overflow, 5.71:1, 0 | none |
| UC-01-S05 | yes | no overflow, 5.71:1, 0 | none |
| UC-01-S06 | yes | no overflow, 5.71:1, 0 | none |
| UC-01-S07 | yes | no overflow, 5.71:1, 0 | none |
| UC-01-S08 | yes | no overflow, 5.71:1, 0 | none |
| UC-01-S09 | yes | no overflow, 5.71:1, 0 | none |
| UC-01-S10 | yes | no overflow, 5.71:1, 0 | none |
| UC-01-S11 | no, see Difference | no overflow, 5.71:1, 0 | the mockup shows 5 of the 9 real orders |
| UC-01-S12 | yes | no overflow, 5.43:1, 0 | none |

Differences between the draft and the implemented screens that were **implemented** (commit on branch `part2`):

| Change | Commit | Screens |
|---|---|---|
| R1 tap targets of at least 44 px (role links, wordmark, action links) | 36dc8f0, 4298973 | all screens |
| R2 My orders is one row per order on a phone; the table was 449 px wide on a 390 px screen | a160bf5 | UC-01-S11 |
| R5 online options named E-wallet, Bank QR code, International card instead of 'e wallet', 'bank qr' | d86eb3b | UC-01-S04, S05, S06, S07 |
| R6 'Cancel this order' is an outline in the danger colour, still behind a confirmation | c749dce | UC-01-S09 |
| P5-D04 the quote table prints 0.39 km, not 0.38971718085988794 km | 5466f6a | UC-01-S04, S05, S07 |
| P5-D02 choosing online payment goes straight to the simulator, without a false 'price changed' notice | ce18bf6 | UC-01-S04 to S06 |

Kept as **design notes** (not implemented, reason):

- Cancel stays a plain button with a browser confirmation (no custom dialog): enough for the SSD result.
- The step bar and the sticky total bar are kept as built; the figure shows the total bar in the flow of the page.
