# NFR-09 check: key pages at a 360 CSS-pixel viewport (two runs)

Date: 09/11/2026 for both runs. Author: 722I0004 · AI-assisted (Claude Sonnet 5.5)

Requirement (I_1-7, NFR-09): at 360 CSS pixels each key page has document scroll width no greater than the viewport width; primary controls are visible and operable without horizontal page scrolling. Touch targets of at least 44 px are the R1 rule of 4.3.3.

| Run | Commit / code state | Folder | Result |
|---|---|---|---|
| Before fix | commit `7670e8b` | `before_fix/` | 37 of 45 pages PASS, 8 FAIL (K03_availability, A01_hubs, A03_hub_menu, A04_catalogue, A07_vouchers, A09_users, M03_workload, M04_delivery) |
| After fix | working tree after `7670e8b` with refinement R7 (last rule block of `style.css`, uncommitted when run) | this folder (root) | 45 of 45 pages PASS, 0 FAIL |

Refinement R7 (09/11/2026, final form): under 600 px `table.data:not(.my-orders)` becomes `display:block; overflow-x:auto; max-width:100%` with scroll-edge shadows, so each data table scrolls inside its own box; `table.data td a`, `.hint a` and `ul.plain > li > a` get `min-height:44px`; `select` gets `max-width:100%`. The after run is the third run of the sweep on the working tree; the two intermediate runs (partial R7) were discarded.

## Setup (same for both runs)

- Browser: Chromium 149.0.7827.55 (driven by Playwright 1.64.1, headless). Viewport: 360x800, deviceScaleFactor 2, isMobile true, hasTouch true.
- Server: flask run on 127.0.0.1:5109, debug off, throwaway DB from init_db.py (demo seed). Seeded demo accounts, password `123456`. No production VM and no real data file used. Application code, templates and CSS were not edited by the runs.
- Data: the demo seed plus two orders created through the UI (order 9 cash on delivery with a replacement offer sent by the kitchen and accepted by the customer, picked up by the shipper; order 10 paid through the payment simulator and made ready), so boards, tables and forms are not empty. Reports use 2026-01-01 to 2026-12-31.
- Per page: `document.documentElement.scrollWidth` and `clientWidth`. PASS when scrollWidth <= clientWidth, clientWidth = 360 and `window.scrollTo(200,0)` leaves `scrollX` at 0 (rules out overflow hidden by `overflow-x`). A table that scrolls inside its own box counts as PASS when the page itself does not scroll (like the sales report table). Elements outside the viewport are listed in `results.json` (`elements_wider_than_viewport`; `elements_clipped_by_scroll_wrapper` when an `overflow-x` ancestor inside the viewport clips them).
- Touch targets: every visible `a`, `button`, `input`, `select` whose box (checkbox or radio: its label box) is under 44 px high or wide (`small_targets`). No link inside a sentence was under 44 px. The "Skip to content" link sits above the screen until keyboard focus (131 x 40 px when focused) and is listed in `offscreen_until_focus`, not counted.
- Screenshots are full page, 720 px wide (360 x 2).

## How to re-run

Needs Playwright for Python, a Chromium-family browser and a Python with the app requirements. From the repository root:

```
<tools venv>/python docs/part2/test_report/nfr09_360_2026-11-09/run_nfr09.py --repo . --out <output folder> --port 5109 --server-python .venv/Scripts/python.exe --scratch <empty scratch dir> [--chromium <path to chrome.exe>]
```

It creates a fresh database with `init_db.py --db`, starts `flask run` on the port, drives the pages, writes screenshots, `results.json` and `results.csv`, and stops the server. The Playwright-pinned browser build was not installed here, so `--chromium` pointed at `chromium-1228` in `%LOCALAPPDATA%\ms-playwright`. The before run is reproduced by running the script on a checkout of commit `7670e8b` (or with `saigonbite/presentation/static/style.css` at that commit); `before_fix/run_nfr09.py` is the script as it was then (it needs absolute `--repo`/`--server-python` paths).

## Results per page

| Id | Role | Page | URL | Before: scrollWidth / clientWidth | After: scrollWidth / clientWidth | Targets under 44 px, before | Targets under 44 px, after | Note (after) |
|---|---|---|---|---|---|---|---|---|
| L01_login | anonymous | Login | `/login` | 360 / 360 **PASS** | 360 / 360 **PASS** | 0 | 0 |  |
| L02_register | anonymous | Register | `/register` | 360 / 360 **PASS** | 360 / 360 **PASS** | 0 | 0 |  |
| L03_home_anon | anonymous | Home (logged out) | `/` | 360 / 360 **PASS** | 360 / 360 **PASS** | 0 | 0 |  |
| L04_login_error | anonymous | Login, wrong password (error banner) | `/login` | 360 / 360 **PASS** | 360 / 360 **PASS** | 0 | 0 |  |
| C01_home | customer | Home | `/` | 360 / 360 **PASS** | 360 / 360 **PASS** | 0 | 0 |  |
| C02_hubs | customer | Choose a kitchen hub | `/order/hubs` | 360 / 360 **PASS** | 360 / 360 **PASS** | 0 | 0 |  |
| C03_menu | customer | Menu of District 1 hub | `/order/hubs/1` | 360 / 360 **PASS** | 360 / 360 **PASS** | 1 (Add an address 95.9x19) | 0 |  |
| C03b_menu_filled | customer | Menu with quantities typed (summary bar) | `/order/hubs/1` | 360 / 360 **PASS** | 360 / 360 **PASS** | 1 (Add an address 95.9x19) | 0 |  |
| C04_quote | customer | Quote / cart | `/order/quote` | 360 / 360 **PASS** | 360 / 360 **PASS** | 0 | 0 |  |
| C05_confirmation | customer | Order confirmation (COD) | `/order/9/confirmation` | 360 / 360 **PASS** | 360 / 360 **PASS** | 0 | 0 |  |
| C06_detail | customer | Order detail (Placed) | `/order/9` | 360 / 360 **PASS** | 360 / 360 **PASS** | 0 | 0 |  |
| C07_quote_online | customer | Quote with online payment chosen | `/order/quote` | 360 / 360 **PASS** | 360 / 360 **PASS** | 0 | 0 |  |
| C08_payment_sim | customer | Payment simulator | `/order/confirm` | 360 / 360 **PASS** | 360 / 360 **PASS** | 0 | 0 |  |
| C09_confirmation_online | customer | Order confirmation (online) | `/order/10/confirmation` | 360 / 360 **PASS** | 360 / 360 **PASS** | 0 | 0 |  |
| K01_board | kitchen | Order board | `/kitchen/` | 360 / 360 **PASS** | 360 / 360 **PASS** | 0 | 0 |  |
| K02_order_placed | kitchen | Order detail (Placed, confirm/reject/offer forms) | `/kitchen/orders/9` | 360 / 360 **PASS** | 360 / 360 **PASS** | 0 | 0 |  |
| K03_availability | kitchen | Availability list | `/kitchen/availability` | 388 / 360 **FAIL** | 360 / 360 **PASS** | 0 | 0 | table scrolls inside itself (R7) |
| K04_order_offered | kitchen | Order detail after replacement offered | `/kitchen/orders/9` | 360 / 360 **PASS** | 360 / 360 **PASS** | 0 | 0 |  |
| C10_detail_offer | customer | Order detail with replacement offer (Accept / Decline) | `/order/9` | 360 / 360 **PASS** | 360 / 360 **PASS** | 0 | 0 |  |
| K05_order_ready | kitchen | Order detail (Ready) | `/kitchen/orders/9` | 360 / 360 **PASS** | 360 / 360 **PASS** | 0 | 0 |  |
| K06_board_busy | kitchen | Order board with orders in several columns | `/kitchen/` | 360 / 360 **PASS** | 360 / 360 **PASS** | 0 | 0 |  |
| S01_board | shipper | Delivery board | `/delivery/` | 360 / 360 **PASS** | 360 / 360 **PASS** | 2 (Order 3 54x21; Order 1 54x21) | 0 |  |
| S02_detail | shipper | Delivery detail (awaiting pickup) | `/delivery/orders/9` | 360 / 360 **PASS** | 360 / 360 **PASS** | 0 | 0 |  |
| S03_detail_picked | shipper | Delivery detail (picked up: Delivered / Could not deliver) | `/delivery/orders/9` | 360 / 360 **PASS** | 360 / 360 **PASS** | 0 | 0 |  |
| S04_board_active | shipper | Delivery board with an active delivery | `/delivery/` | 360 / 360 **PASS** | 360 / 360 **PASS** | 2 (Order 3 54x21; Order 1 54x21) | 0 |  |
| C11_detail_progress | customer | Order detail (delivery in progress) | `/order/9` | 360 / 360 **PASS** | 360 / 360 **PASS** | 0 | 0 |  |
| C12_receipt | customer | Receipt | `/order/9/receipt` | 360 / 360 **PASS** | 360 / 360 **PASS** | 0 | 0 |  |
| C13_my_orders | customer | My orders | `/order/mine` | 360 / 360 **PASS** | 360 / 360 **PASS** | 0 | 0 |  |
| C14_account | customer | Account / profile | `/account` | 360 / 360 **PASS** | 360 / 360 **PASS** | 0 | 0 |  |
| C15_address_new | customer | New address form | `/account/addresses/new` | 360 / 360 **PASS** | 360 / 360 **PASS** | 0 | 0 |  |
| A01_hubs | admin | Hubs and capacity | `/admin/hubs` | 701 / 360 **FAIL** | 360 / 360 **PASS** | 0 | 0 | table scrolls inside itself (R7) |
| A02_hub_form | admin | Edit hub form | `/admin/hubs/1` | 360 / 360 **PASS** | 360 / 360 **PASS** | 0 | 0 |  |
| A03_hub_menu | admin | Hub menu | `/admin/hubs/1/menu` | 577 / 360 **FAIL** | 360 / 360 **PASS** | 0 | 0 | table scrolls inside itself (R7) |
| A04_catalogue | admin | Catalogue (brands and dishes) | `/admin/menu` | 389 / 360 **FAIL** | 360 / 360 **PASS** | 2 (SaigonBite District 1 Hub 176.4x21; SaigonBite Binh Thanh Hub 193x21) | 0 | table scrolls inside itself (R7) |
| A05_item_form | admin | Edit dish form | `/admin/items/1` | 360 / 360 **PASS** | 360 / 360 **PASS** | 0 | 0 |  |
| A06_item_new | admin | New dish form | `/admin/items/new` | 360 / 360 **PASS** | 360 / 360 **PASS** | 0 | 0 |  |
| A07_vouchers | admin | Vouchers | `/admin/vouchers` | 501 / 360 **FAIL** | 360 / 360 **PASS** | 0 | 0 | table scrolls inside itself (R7) |
| A08_voucher_form | admin | Edit voucher form | `/admin/vouchers/1` | 360 / 360 **PASS** | 360 / 360 **PASS** | 0 | 0 |  |
| A09_users | admin | Accounts | `/admin/users` | 520 / 360 **FAIL** | 360 / 360 **PASS** | 0 | 0 | table scrolls inside itself (R7) |
| A10_user_form | admin | Edit account form | `/admin/users/1` | 360 / 360 **PASS** | 360 / 360 **PASS** | 0 | 0 |  |
| A11_archive | admin | Archive of old orders | `/admin/archive` | 360 / 360 **PASS** | 360 / 360 **PASS** | 0 | 0 |  |
| M01_reports | manager | Reports index | `/reports/` | 360 / 360 **PASS** | 360 / 360 **PASS** | 0 | 0 | table scrolls inside `div.table-scroll` (R3) |
| M02_sales | manager | Sales report (2026) | `/reports/sales?from=2026-01-01&to=2026-12-31` | 360 / 360 **PASS** | 360 / 360 **PASS** | 0 | 0 | table scrolls inside `div.table-scroll` (R3) |
| M03_workload | manager | Workload report (2026) | `/reports/workload?from=2026-01-01&to=2026-12-31` | 743 / 360 **FAIL** | 360 / 360 **PASS** | 0 | 0 | table scrolls inside itself (R7) |
| M04_delivery | manager | Delivery report (2026) | `/reports/delivery?from=2026-01-01&to=2026-12-31` | 656 / 360 **FAIL** | 360 / 360 **PASS** | 0 | 0 | table scrolls inside itself (R7) |

## Findings

- Before the fix, 8 table pages scrolled sideways (388 to 743 px) because `table.data` had no scroll box and `nowrap` row actions and first-column links kept each table at its natural width.
- After R7 all 45 pages have scrollWidth 360 and `scrollX` stays 0 when a sideways scroll is tried. On 10 pages a data table scrolls inside itself: kitchen availability, admin hubs, hub menu, catalogue, vouchers, accounts, the workload and delivery reports (R7), and the reports index and sales report (R3 box).
- The admin hub menu was 362 px in the intermediate run because of the add-a-dish `select` (346 px); `select { max-width: 100% }` fixes it.
- Touch targets after R7: no visible `a`, `button`, `input` or `select` is under 44 px (before: 5 links, "Add an address", two shipper "Order N" links, two catalogue hub-name links; the first three groups now 44 px). The skip link is off-screen until focus (131 x 40 px when focused) and is not counted.
- Visual check (`A01_hubs.png`, `A03_hub_menu.png`): the right-edge shadow of the scrolling table is visible; on the hubs page it is a soft grey band at the right edge of the table, on the hub menu page it is fainter and a cut-off "A" of the action link shows at the edge. The row actions (Edit, Menu, Archive; Sold out, Remove from menu) are still off-screen to the right until the table is scrolled sideways. The select fits the column. Nothing else looked broken.
