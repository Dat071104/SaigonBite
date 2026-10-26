# UI critique of the draft screens (before refinement)

Author: 722I0004 · AI-assisted (Claude Sonnet 5.5). Written 27/10/2026 after the draft screens (I1–P4) were photographed.

**What was looked at.** All 47 in-scope screens of `../screens.csv`, photographed from the running app (local Flask development
server, Edge 156, Playwright 1.64.1) at their own viewport: customer and shipper at 390×844, kitchen, admin and manager at 1440×900
(`UC-0x-Snn.png` in this folder; the case and the order ids are in `../_kit/captured/before/run.json`). Staff screens were
also measured at 768 px and phone screens at 360 px (`../_kit/captured/before/width_check.csv`).
**Rules used.** The A6 subset of tasteskill v2 for transactional app screens: one ground, ink and accent; 16/20/28 px; flat 8 px
buttons 48 px tall; contrast ≥ 4.5:1; focus visible; tap targets ≥ 44 px; phone has its own composition (390 px, one column, no
sideways scroll); every state designed. What must survive any change is in `must_survive.md`.

## Measurements (all 47 screens, one script, `../_kit/render.py` rules)

| Check | Result | Note |
|---|---|---|
| Text contrast | **Pass.** Lowest ratio 5.25:1 (muted text on a tone-step surface), nothing under 4.5:1 | `captured/before/measure.csv` |
| One `h1` per screen | **Pass** on 47 of 47 | |
| Visible label on every field | **Pass** | |
| Horizontal overflow at the screen's viewport | **2 fail**: UC-01-S11 and UC-05-S05 (My orders on a phone) are 449 px wide on a 390 px screen | table with 5 columns |
| Overflow at the other widths | **2 fail**: Sales report 967 px at 768 px; My orders 450 px at 360 px | `width_check.csv` |
| Tap targets under 44 px | **fail on every screen**: top-bar role links 34 px, wordmark 30 px, "Printable receipt" link 24 px, kitchen card links 24 px and card buttons 40 px, admin row link-buttons 32 px (up to 20 on one admin page) | the 48 px primary buttons pass |

Defects found while doing this (all fixed with a regression test, see `docs/part2/test_report/integration_2026-10-27/defects.csv`):
P5-D01 the dish price field refused every seed price in a browser; P5-D02 choosing online payment always showed a false
"price changed" notice; P5-D03 a shipper who lost the pick-up race landed on a 403 page with only "Back to the home page";
P5-D04 the quote table printed a raw distance (0.38971718085988794 km).

## The three changes that would help most, per use case

| UC | Screen(s) | 1 | 2 | 3 |
|---|---|---|---|---|
| UC-01 Place an order (customer, 390) | S01–S12 | **My orders overflows** (449 px on 390; 450 on 360): one row per order on a phone. | **Payment names read like codes** ("e wallet", "bank qr"): show "E-wallet", "Bank QR code", "International card". | **Tap targets**: role links 34 px, "Printable receipt" 24 px: 44 px. |
| UC-05 Confirm or reject (kitchen 1440; customer 390) | S01–S09 | **Kitchen card controls are small** (Confirm 40 px, order link 24 px): 44 px, same label. | **Customer's My orders** (S05) has the same overflow and hides "Your answer needed" off screen: fixed by the one-row layout. | Offer panel (S06) is clear; keep. The decline consequence ("order is not cooked") stays as written (the app rejects the order). |
| UC-02 Deliver an order (shipper, 390) | S01–S07 | **Cards read as loose text**: the card is white on white with padding inside padding; make it a surface (tone step). | **The cash to collect is the key figure but is body text**: 20 px bold, tabular. The primary action "Pick up this order" is 40 px and not full width: full width, 48 px. | **"Order 3" wraps onto two lines** in My recent deliveries: no wrapping on the order link. |
| UC-03 Manage hubs and capacity (admin 1440) | S01–S06 | **Row actions 32 px** (Edit, Menu, Archive): 44 px. | Capacity range ("1 to 500") is already shown beside the field; keep. | Sales/hub tables are fine at 1440; hub screens fit at 768. |
| UC-06 Brands and menu (admin 1440) | S01–S08 | **20+ "Archive" link-buttons at 32 px** on one page: 44 px. | Archived rows stay visible and muted: keep. | The dish form's price field refused valid prices (P5-D01, fixed). |
| UC-04 Management reports (manager 1440) | S01–S05 | **Sales table overflows at 768** (967 px): the table scrolls inside its own labelled box, the page does not. | The empty period and the invalid filter are already designed ("n/a", error next to the filter): keep. | Contrast, h1 and labels pass; top-bar links 34 px: 44 px. |

## What was decided

Refinement is limited to what the measurements justify and what an SSD result or a use-case goal needs (A6 "bounded refinement"):
R1 tap targets ≥ 44 px, R2 My orders without sideways scroll on a phone, R3 wide report table scrolls in its own box,
R4 shipper cards (surface, cash figure, full-width action), R5 payment option names. All are CSS or template changes; no route, field
name, id, `data-*` hook or asserted text changes. The rest of the critique items are "keep". After the refinement the
screens are photographed again and compared (`../refinement_log.md`).
