# P5.1 refinement log: UI design refinement after the draft build

Author: 722I0004 · AI-assisted (Claude Sonnet 5.5). 27/10/2026.

The draft screens were built first (I1 to P4). P5.1 photographed them (`_before/`), measured and criticised them (`_before/critique.md`), authored wireframes and
mockups as HTML/CSS (`UC-0x/wireframes`, `UC-0x/mockups`, `_kit/`), and then refined the real app where a measurement or an SSD result called for it. Only templates,
`style.css` and `app.js` changed (no route, form field name, element id, `data-*` hook or asserted text; `_before/must_survive.md`); no dependency, web font or CDN was
added. The full suite ran green after every commit (926 to 928 passed, 0 failed, 0 skipped).

| # | Refinement | Why (measured on the draft) | Commit | Before | After |
|---|---|---|---|---|---|
| R1 | Tap targets at least 44 px: role links, wordmark, links in action rows, kitchen card links and buttons, admin row actions; short labels at least 44 px wide | role links 34 px, wordmark 30, "Printable receipt" 24, kitchen order links 24 and buttons 40, admin row link-buttons 32 (up to 20 on one page); failing on all 47 screens | 36dc8f0, 4298973 | `_before/UC-05-S01.png`, `_before/UC-06-S01.png` | `UC-05/implemented/UC-05-S01.png`, `UC-06/implemented/UC-06-S01.png`; 0 elements under 44 px on all 47 screens |
| R2 | My orders is one row per order on a phone | table 449 px wide on a 390 px screen, 450 px on 360 px (horizontal scroll) | a160bf5 | `_before/UC-01-S11.png`, `_before/UC-05-S05.png` | `UC-01/implemented/UC-01-S11.png`, `_after/customer_order_mine_360_after.png`; no overflow at 360 and 390 |
| R3 | The sales table scrolls inside its own labelled box | 967 px wide at 768 px | 7baeb74 | `_after/manager_reports_sales_768_before.png` | `_after/manager_reports_sales_768_after.png`; page width 768 |
| R4 | Shipper cards are surfaces; the cash to collect is a 20 px bold figure; the action is full width and 48 px on a phone; "Order 3" does not wrap | white-on-white cards with padding inside padding, cash as body text, 40 px action, order link wrapping onto two lines | d053ca5 | `_before/UC-02-S01.png` | `UC-02/implemented/UC-02-S01.png` |
| R5 | Online options read E-wallet, Bank QR code, International card | "e wallet", "bank qr" (raw enum text) | d86eb3b | `_before/UC-01-S04.png` | `UC-01/implemented/UC-01-S04.png` |
| R6 | "Cancel this order" is an outline in the danger colour (still behind a confirmation) | A6: destructive actions use danger | c749dce | `_before/UC-01-S09.png` | `UC-01/implemented/UC-01-S09.png` |
| R7 | The order number on a waiting delivery card opens the delivery page | the SSD operation viewDelivery (OP-22) had no way in from the board | 0a594bf | `_before/UC-02-S01.png` | `UC-02/implemented/UC-02-S01.png`, `UC-02-S02.png` |
| R8 | A finished delivery no longer tells the shipper to collect cash | "Collect 70,000 VND in cash" stayed after delivery | 6970f0f | `_before/UC-02-S06.png` | `UC-02/implemented/UC-02-S06.png` |
| R9 | A zero voucher total prints "0 VND", not "-0 VND" | empty period showed "-0 VND" | dc87741 | `_before/UC-04-S04.png` | `UC-04/implemented/UC-04-S04.png` |

Defects fixed with a regression test (not refinements; see `docs/part2/test_report/integration_2026-10-27/defects.csv`): P5-D01 b68bfef, P5-D02 ce18bf6, P5-D03 1776293, P5-D04 5466f6a, P5-D05 252ada1.

## Comparison at several widths (same data, before commit 5394cee, after 252ada1; `_kit/reports/width_before_after.csv`)

| Page, width | Before | After |
|---|---|---|
| My orders, 360 px | overflow, page 450 px, 4 targets under 44 px | no overflow, 0 under 44 px |
| My orders, 390 px | overflow, page 449 px | no overflow, 0 under 44 px |
| Sales, 768 px | overflow, page 967 px | no overflow (table scrolls in its box), 0 under 44 px |
| Sales, 1440 px | ok, 4 under 44 px | ok, 0 |
| Kitchen board, 768 and 1440 px | ok, 6 under 44 px | ok, 0 |
| Brands and menu (admin), 768 and 1440 px | ok, 20 under 44 px | ok, 0 |
| Deliveries (shipper), 390 px; hubs (customer), 390 px | ok, 3 and 4 under 44 px | ok, 0 |

All screens of `screens.csv` were also re-photographed at their own viewport after the refinement (`UC-0x/implemented/`, measured in `_kit/captured/implemented/measure.csv`): no
overflow, lowest text contrast 5.24:1 (limit 4.5:1), no element under 44 px, one h1 and a label on every field, on 47 of 47 screens. Everything that worked before was clicked
through again in the browser: the integration run (S1 to S8, 60 of 60 steps) was done at the final runtime commit.

## Last critique round (after)

Nothing measured fails any more. Left as they are, on purpose: the plain top bar and one accent colour; flat 8 px buttons; the kitchen board's four columns; the report
tables; "Reject order", "Report failed delivery" and "Archive this hub" as the solid danger button of the final irreversible step. Reported to the owner, not changed
(they live in Python modules sealed by the G4 dependency policy, which only an owner-reviewed seal update can open): P5-D03 remainder (two red boxes after a lost pick-up)
and P5-D06 (the decline banner always mentions an online refund, also for a cash order).
