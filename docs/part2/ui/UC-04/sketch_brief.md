# UC-04 Produce management reports: sketch brief (for Dat to draw)

Author: 722I0004 · AI-assisted (Claude Sonnet 5.5). This is the brief only. The sketch itself is the owner's own paper or Figma-freehand drawing;
no image imitating a hand-drawn sketch is generated. Put the photos in `sketch/` and write the real date you drew them in the file name
or in `sketch/README.md`. Until then `trace.md` says `OWNER-PENDING`.

Device: a desktop browser (1440 × 900 landscape). Report screens use the wide 1120 px width. Draw one rectangle per screen, about 10 minutes for all of them.

| Sketch | Screen it becomes | Draw these controls | SSD operation it serves |
|---|---|---|---|
| 1 | UC-04-S01 Sales report | three links Sales, Workload, Delivery (Sales underlined); title and grey help line; filter row From, To (inclusive), Hub, "Show"; table Hub, Orders, Dishes, Vouchers, Delivery fees, Total, Refunds owed, Net with a bold "All hubs" row; grey note; "Best-selling dishes" table | OP-26 salesReport (BR-21, BR-24) |
| 2 | UC-04-S02 Hub workload now | "As of <time>"; table Hub, New, Confirmed, Preparing, Load / capacity, Load %, Status badge, Ready, On the way | OP-27 workloadReport (BR-22) |
| 3 | UC-04-S03 Delivery performance | filter row; "By hub" and "By shipper" tables: Delivered, Failed, Failure rate, Avg wait and Avg ride with (n=...) | OP-28 deliveryReport (BR-23) |
| 4 | UC-04-S04 Empty period | filter with a future period; one row "No delivered orders in this period." and a totals row of zeros | OP-26, OP-28 |
| 5 | UC-04-S05 Filter refused | filter row and a red box "The first day must be on or before the last day."; nothing else below | OP-26 (invalid filter) |

Keep: labels in words (no icons), one main button per screen, the refusal message in a box above the form or table.
