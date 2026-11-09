# NFR-09 check: key pages at a 360 CSS-pixel viewport

Date: 09/11/2026 (run started 2026-11-09T10:53:15). Commit: `7670e8b` (working tree not modified by this run; application code, templates and CSS untouched).
Author: 722I0004 · AI-assisted (Claude Sonnet 5.5)

Requirement (I_1-7, NFR-09): at 360 CSS pixels each key page has document scroll width no greater than the viewport width; primary controls are visible and operable without horizontal page scrolling. Touch targets of at least 44 px are the R1 rule of 4.3.3.

## Setup

- Browser: Chromium 149.0.7827.55 (driven by Playwright 1.64.1, headless). Viewport: 360x800, deviceScaleFactor 2, isMobile true, hasTouch true.
- Server: flask run on 127.0.0.1:5109, debug off, throwaway DB from init_db.py (demo seed). Seeded demo accounts, password `123456`. No production VM and no real data file used.
- Data: the demo seed plus two orders created through the UI (order 9 cash on delivery with a replacement offer sent by the kitchen and accepted by the customer, picked up by the shipper; order 10 paid through the payment simulator and made ready), so boards, tables and forms are not empty. Reports use the range 2026-01-01 to 2026-12-31.
- Per page: `document.documentElement.scrollWidth` and `clientWidth`; PASS when scrollWidth <= clientWidth, clientWidth = 360 and `window.scrollTo(200, 0)` leaves `scrollX` at 0 (this rules out overflow hidden by `overflow-x`). Elements whose box leaves the viewport are listed in `results.json` (`elements_wider_than_viewport`; `elements_clipped_by_scroll_wrapper` for those inside an `overflow-x` wrapper).
- Touch targets: every visible `a`, `button`, `input`, `select` whose box (for a checkbox or radio: its label box) is under 44 px high or wide (`small_targets`; `small_targets_inline_text_links` counts links inside a sentence, none were found). The "Skip to content" link sits above the screen (top -48 px) and appears on keyboard focus only (131 x 40 px when focused); it is listed per page in `offscreen_until_focus`, not counted here.
- Screenshots are full page, 720 px wide (360 x 2).

## How to re-run

Needs Playwright for Python and a Chromium-family browser, and a Python with the app requirements to start the server. From the repository root:

```
<tools venv>/python run_nfr09.py --repo . --out docs/part2/test_report/nfr09_360_2026-11-09 --port 5109 --server-python .venv/Scripts/python.exe --scratch <empty scratch dir> [--chromium <path to chrome.exe>]
```

It creates a fresh database with `init_db.py --db`, starts `flask run` on the port, drives the pages, writes screenshots, `results.json` and `results.csv`, and stops the server. In this run the Playwright-pinned build was not installed, so `--chromium` pointed at `chromium-1228` in `%LOCALAPPDATA%\ms-playwright`.

## Result

37 of 45 pages PASS and 8 FAIL. Failing pages: K03_availability, A01_hubs, A03_hub_menu, A04_catalogue, A07_vouchers, A09_users, M03_workload, M04_delivery.

| Id | Role | Page | URL | scrollWidth / clientWidth | Result | Targets under 44 px | Cause / note |
|---|---|---|---|---|---|---|---|
| L01_login | anonymous | Login | `/login` | 360 / 360 | **PASS** | 0  |  |
| L02_register | anonymous | Register | `/register` | 360 / 360 | **PASS** | 0  |  |
| L03_home_anon | anonymous | Home (logged out) | `/` | 360 / 360 | **PASS** | 0  |  |
| L04_login_error | anonymous | Login, wrong password (error banner) | `/login` | 360 / 360 | **PASS** | 0  |  |
| C01_home | customer | Home | `/` | 360 / 360 | **PASS** | 0  |  |
| C02_hubs | customer | Choose a kitchen hub | `/order/hubs` | 360 / 360 | **PASS** | 0  |  |
| C03_menu | customer | Menu of District 1 hub | `/order/hubs/1` | 360 / 360 | **PASS** | 1 (Add an address 95.9x19) |  |
| C03b_menu_filled | customer | Menu with quantities typed (summary bar) | `/order/hubs/1` | 360 / 360 | **PASS** | 1 (Add an address 95.9x19) |  |
| C04_quote | customer | Quote / cart | `/order/quote` | 360 / 360 | **PASS** | 0  |  |
| C05_confirmation | customer | Order confirmation (COD) | `/order/9/confirmation` | 360 / 360 | **PASS** | 0  |  |
| C06_detail | customer | Order detail (Placed) | `/order/9` | 360 / 360 | **PASS** | 0  |  |
| C07_quote_online | customer | Quote with online payment chosen | `/order/quote` | 360 / 360 | **PASS** | 0  |  |
| C08_payment_sim | customer | Payment simulator | `/order/confirm` | 360 / 360 | **PASS** | 0  |  |
| C09_confirmation_online | customer | Order confirmation (online) | `/order/10/confirmation` | 360 / 360 | **PASS** | 0  |  |
| K01_board | kitchen | Order board | `/kitchen/` | 360 / 360 | **PASS** | 0  |  |
| K02_order_placed | kitchen | Order detail (Placed, confirm/reject/offer forms) | `/kitchen/orders/9` | 360 / 360 | **PASS** | 0  |  |
| K03_availability | kitchen | Availability list | `/kitchen/availability` | 388 / 360 | **FAIL** | 0  | `table.data` is wider than the viewport, no scroll wrapper |
| K04_order_offered | kitchen | Order detail after replacement offered | `/kitchen/orders/9` | 360 / 360 | **PASS** | 0  |  |
| C10_detail_offer | customer | Order detail with replacement offer (Accept / Decline) | `/order/9` | 360 / 360 | **PASS** | 0  |  |
| K05_order_ready | kitchen | Order detail (Ready) | `/kitchen/orders/9` | 360 / 360 | **PASS** | 0  |  |
| K06_board_busy | kitchen | Order board with orders in several columns | `/kitchen/` | 360 / 360 | **PASS** | 0  |  |
| S01_board | shipper | Delivery board | `/delivery/` | 360 / 360 | **PASS** | 2 (Order 3 54x21; Order 1 54x21) |  |
| S02_detail | shipper | Delivery detail (awaiting pickup) | `/delivery/orders/9` | 360 / 360 | **PASS** | 0  |  |
| S03_detail_picked | shipper | Delivery detail (picked up: Delivered / Could not deliver) | `/delivery/orders/9` | 360 / 360 | **PASS** | 0  |  |
| S04_board_active | shipper | Delivery board with an active delivery | `/delivery/` | 360 / 360 | **PASS** | 2 (Order 3 54x21; Order 1 54x21) |  |
| C11_detail_progress | customer | Order detail (delivery in progress) | `/order/9` | 360 / 360 | **PASS** | 0  |  |
| C12_receipt | customer | Receipt | `/order/9/receipt` | 360 / 360 | **PASS** | 0  |  |
| C13_my_orders | customer | My orders | `/order/mine` | 360 / 360 | **PASS** | 0  |  |
| C14_account | customer | Account / profile | `/account` | 360 / 360 | **PASS** | 0  |  |
| C15_address_new | customer | New address form | `/account/addresses/new` | 360 / 360 | **PASS** | 0  |  |
| A01_hubs | admin | Hubs and capacity | `/admin/hubs` | 701 / 360 | **FAIL** | 0  | `table#hub-table.data` is wider than the viewport, no scroll wrapper |
| A02_hub_form | admin | Edit hub form | `/admin/hubs/1` | 360 / 360 | **PASS** | 0  |  |
| A03_hub_menu | admin | Hub menu | `/admin/hubs/1/menu` | 577 / 360 | **FAIL** | 0  | `table#listing-table.data` is wider than the viewport, no scroll wrapper |
| A04_catalogue | admin | Catalogue (brands and dishes) | `/admin/menu` | 389 / 360 | **FAIL** | 2 (SaigonBite District 1 Hub 176.4x21; SaigonBite Binh Thanh Hub 193x21) | `table#brand-table.data, table#item-table.data` is wider than the viewport, no scroll wrapper |
| A05_item_form | admin | Edit dish form | `/admin/items/1` | 360 / 360 | **PASS** | 0  |  |
| A06_item_new | admin | New dish form | `/admin/items/new` | 360 / 360 | **PASS** | 0  |  |
| A07_vouchers | admin | Vouchers | `/admin/vouchers` | 501 / 360 | **FAIL** | 0  | `table#voucher-table.data` is wider than the viewport, no scroll wrapper |
| A08_voucher_form | admin | Edit voucher form | `/admin/vouchers/1` | 360 / 360 | **PASS** | 0  |  |
| A09_users | admin | Accounts | `/admin/users` | 520 / 360 | **FAIL** | 0  | `table#user-table.data` is wider than the viewport, no scroll wrapper |
| A10_user_form | admin | Edit account form | `/admin/users/1` | 360 / 360 | **PASS** | 0  |  |
| A11_archive | admin | Archive of old orders | `/admin/archive` | 360 / 360 | **PASS** | 0  |  |
| M01_reports | manager | Reports index | `/reports/` | 360 / 360 | **PASS** | 0  | table inside `div.table-scroll` (overflow-x:auto) is wider than the page; the page itself does not scroll |
| M02_sales | manager | Sales report (2026) | `/reports/sales?from=2026-01-01&to=2026-12-31` | 360 / 360 | **PASS** | 0  | table inside `div.table-scroll` (overflow-x:auto) is wider than the page; the page itself does not scroll |
| M03_workload | manager | Workload report (2026) | `/reports/workload?from=2026-01-01&to=2026-12-31` | 743 / 360 | **FAIL** | 0  | `table#workload-table.data` is wider than the viewport, no scroll wrapper |
| M04_delivery | manager | Delivery report (2026) | `/reports/delivery?from=2026-01-01&to=2026-12-31` | 656 / 360 | **FAIL** | 0  | `table#delivery-by-hub.data, table#delivery-by-shipper.data` is wider than the viewport, no scroll wrapper |

## Findings

- All six customer screens named in the requirement (hubs, menu, quote, confirmation, order detail, My orders), the receipt, the kitchen board and order detail (including the replacement-offer form), the shipper board and delivery detail, the login and register pages, and the admin edit forms pass: scrollWidth 360.
- The pages that fail are table pages: `table.data` has no scroll wrapper (only the sales report table is wrapped in `div.table-scroll`, style rule R3), the row-action cells are `white-space: nowrap` and first-column links are `nowrap` (`.row-actions`, `table.data td:first-child a` in `style.css`), so the table keeps its natural width and the document scrolls sideways. Overflow: kitchen availability 388 px, admin catalogue 389 px, hub menu 577 px, vouchers 501 px, accounts 520 px, hubs 701 px, workload report 743 px, delivery report 656 px.
- On the sales report (M02) and the reports index (M01) the table is wider than the screen but scrolls inside `div.table-scroll`; the page does not scroll (PASS).
- Touch targets: the main controls (buttons, nav links, form fields, actions) are 44 px or more. Under 44 px, outside paragraphs: "Add an address" link on the menu (19 px high), "Order N" links in the shipper board tables (21 px high, in a table cell), hub name links in the admin catalogue (21 px high). No link inside a sentence is under 44 px.
