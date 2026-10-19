# SaigonBite – Online Food Delivery Hub Platform

Course project for Requirements Analysis and Design (RAD), Sem01 2026-27, Team02.
SaigonBite runs cloud kitchens across several hubs; this platform spreads lunch-hour orders across hubs,
tracks delivery and cash, and reports from one shared order record.

| Member | Student ID | Use cases |
|---|---|---|
| Nguyen Thanh Dat | 722I0004 | UC-01 Place an order, UC-03 Manage hubs and kitchen capacity |
| Le Minh Quan | 523K0049 | UC-02 Deliver an order, UC-04 Produce management reports |

**Status:** Iteration 1 increment (tag [`i1-evidence`](https://github.com/Dat071104/SaigonBite/tree/i1-evidence)): a persisted cash-on-delivery (COD) order
for one hub (UC-01 subset) on a runnable skeleton, 81 pytest tests.

> The Iteration 1 code was generated with AI assistance (Claude, 19/10/2026) and is being reviewed by the team;
> see Appendix A of the proposal.

**Documents:** [Part 1 proposal, slides and business process](docs/part1/) · [Iteration 1 analysis](docs/i1/)

Stack: Python 3.12 or later (tested on 3.13), Flask + Jinja2, sqlite3 data-access objects with hand-written SQL (no ORM),
SQLite, Flask-Login, pytest. One application, one database file.

## Set up and run (four commands)

Windows (Command Prompt or PowerShell):

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python init_db.py
flask run
```

macOS / Linux:

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python init_db.py
flask run
```

The four steps are: (1) create and activate the virtual environment, (2) install the pinned requirements,
(3) create and seed the database `instance/saigonbite.db`, (4) start the server. Open <http://127.0.0.1:5000/>.

- On Windows with several Pythons installed, use `py -3.13 -m venv .venv` for step 1.
- `python init_db.py` refuses to overwrite an existing database; use `python init_db.py --force` to recreate it.
- Optional: set `SAIGONBITE_SECRET_KEY` to your own value; the default is a development key.

## Run the tests

```
python -m pytest
```

Each test builds its own temporary database from `db/schema.sql` and `db/seed.sql`. Add `-v` to see the test IDs.

## Seeded development accounts

Passwords are stored as PBKDF2-SHA256 hashes in `db/seed.sql`. These accounts are for local development only.

| Role | Username | Password |
|---|---|---|
| Customer (local, with one address) | `customer` | `dev-customer` |
| Kitchen staff | `kitchen` | `dev-kitchen` |
| Shipper | `shipper` | `dev-shipper` |
| Admin | `admin` | `dev-admin` |
| Manager | `manager` | `dev-manager` |

In Iteration 1 only the customer role has screens. The other roles can log in, see their role on the home page,
and are refused (HTTP 403) on the order pages.

Seed data: two hubs (`HUB-D1` District 1, flat fee 15,000 VND, capacity 12; `HUB-BT` Binh Thanh, flat fee 18,000 VND,
capacity 8), four brands and ten menu items. One item is sold out at the District 1 hub (Com tam ga nuong) and some items are
not carried by one hub, so the "item not available" rule can be tried by hand.

## Try the UC-01 subset by hand

1. Log in as `customer` / `dev-customer`.
2. Choose a hub, enter quantities (leave a blank for items you do not want), choose the address, press "See the quote".
3. The quote shows item subtotal, flat delivery fee and total. Press "Confirm order".
4. The confirmation shows the order ID and total. The order is saved with state `PLACED` and a COD payment in state `PENDING`.

Try an empty cart, a quantity of 0 or -1, or a missing address: a message appears and no order is created.
Double-clicking "Confirm order" creates one order.

## Project layout (three layers, four roles)

| Layer | Role | Location |
|---|---|---|
| Presentation | View | `saigonbite/presentation/` (blueprints `main`, `auth`, `order`; Jinja2 templates in `templates/`) |
| Business | Controller | `saigonbite/business/controllers/` (`PlaceOrderController`, `AuthController`) |
| Business | Domain | `saigonbite/business/domain/` (`OrderState`, `Order`, `OrderLine`, `Payment`, `Hub`, ...) |
| Data access | DAO | `saigonbite/data_access/` (`HubDAO`, `CustomerDAO`, `UserDAO`, `OrderDAO`, `PaymentDAO`) |

Other files: `db/schema.sql`, `db/seed.sql`, `init_db.py`, `app.py` (entry point for `flask run`), `tests/`,
`docs/i1/` (UC-01 subset description, domain model v1, Order state machine v1, SSD, CRUD inventory v1),
`docs/part1/` (Part 1 proposal, slides and business process diagram).

## What Iteration 1 covers

Acceptance criteria AC-1 to AC-9 of the plan (section 7.2): clean-checkout setup, seed (AC-2), quote (AC-3),
one-transaction order creation with `BEGIN IMMEDIATE` (AC-4), read-back through a new connection (AC-5),
input validation (AC-6), double-submit protection by an idempotency token (AC-7), login and customer-role checks on the
server (AC-8), pytest and matching names in code, schema and docs (AC-9).

Not in Iteration 1: busy-hub capacity check, vouchers, distance fee, online payment stub, Kitchen board, delivery,
reports, hub CRUD. The Order states are all defined (`PLACED`, `CONFIRMED`, `REJECTED`, `PREPARING`, `READY`,
`OUT_FOR_DELIVERY`, `DELIVERED`, `DELIVERY_FAILED`, `CANCELLED`) but only `PLACED` is created.
No CSRF protection yet (the idempotency token is not a CSRF token).
