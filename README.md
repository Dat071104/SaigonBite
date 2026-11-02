# SaigonBite – Online Food Delivery Hub Platform

Course project for Requirements Analysis and Design (RAD), Sem01 2026-27, Team 02.
SaigonBite runs delivery-only kitchens (hubs) in Ho Chi Minh City. The platform takes customer orders with a full price
quote, lets each hub's kitchen confirm, reject or offer a replacement, lets shippers deliver and collect cash, lets the
admin maintain hubs and the catalogue, and gives the manager sales, workload and delivery reports — all from one shared
order record.

| Member | Student ID | Main use cases (owner) |
|---|---|---|
| Nguyen Thanh Dat | 722I0004 | UC-01 Place an order, UC-03 Maintain hubs and kitchen capacity |
| Le Minh Quan | 523K0049 | UC-02 Deliver an order, UC-04 Produce management reports |
| Nguyen Minh Quan | 523K0050 | UC-05 Decide an incoming order, UC-06 Maintain brands, menu items and hub listings |

All Part 2 artifacts and code were authored by 722I0004 with AI assistance; see the Contribution Statement and the
Generative AI Usage Log in the report (Appendices 4 and 5).

**Status:** Part 2 release `v0.9-part2` — six main use cases and nine supporting use cases, **928 automated tests
passing**, seven cross-role browser scenarios (60/60 steps), deployed at **https://saigonbite.io.vn**
(fallback https://34-21-141-239.sslip.io).

**Documents:** Part 2 report sources `docs/part2/report/` · models `models/` (draw.io, Graphviz, PNG, SVG) ·
UI design `docs/part2/ui/` · test evidence `docs/part2/test_report/` · deployment `deploy/RUNBOOK.md` ·
Part 1 `docs/part1/`.

Stack: Python 3.13, Flask + Jinja2, Flask-Login, hand-written SQL in data-access objects (no ORM), SQLite (WAL),
pytest; gunicorn and Caddy in production.

## Run with Docker (recommended)

```
git clone https://github.com/Dat071104/SaigonBite.git
cd SaigonBite
git checkout v0.9-part2
docker compose up --build -d                  # open http://127.0.0.1:5000/
docker compose down                           # stop (add -v to delete the demo database and reseed next start)
```

## Run without Docker

Windows:

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python init_db.py
flask --app app run
```

macOS / Linux: use `python3 -m venv .venv` and `source .venv/bin/activate`; the other commands are the same.
`python init_db.py` creates `instance/saigonbite.db` with the schema, seed data and demo history
(`--no-demo` omits the history, `--force` recreates the file). Production needs `SAIGONBITE_SECRET_KEY` and
`SAIGONBITE_ENV=production`; the development server uses a development key.

## Run the tests

```
python -m pytest -q
```

Run from a full Git checkout (some tests read the Git history, so they are not run inside the Docker image).
Each test builds its own temporary database from `db/schema.sql` and `db/seed.sql`.

## Demo accounts

Every seeded account uses the demo password `123456` (stored as a PBKDF2-SHA256 hash). The data is demo data only.

| Role | Username | Password |
|---|---|---|
| Customer (local, with one address) | `customer` | `123456` |
| Kitchen staff, District 1 hub | `kitchen` | `123456` |
| Kitchen staff, Binh Thanh hub | `kitchen_bt` | `123456` |
| Shipper | `shipper` | `123456` |
| Admin | `admin` | `123456` |
| Manager | `manager` | `123456` |

Seed data: two hubs (`HUB-D1` District 1, base delivery fee 12,000 VND, capacity 12; `HUB-BT` Binh Thanh, base fee
10,000 VND, capacity 8), brands, menu items, vouchers and a short demo order history. Section 5.3 of the report gives a
ten-step demonstration through all six use cases.

## Project layout (three layers)

| Layer | Location |
|---|---|
| Presentation (views) | `saigonbite/presentation/` — Flask blueprints `main`, `auth`, `account`, `order`, `kitchen`, `delivery`, `admin`, `reports`; Jinja2 templates and one stylesheet |
| Business — controllers | `saigonbite/business/controllers/` — one controller per use case (`PlaceOrderController`, `DeliveryController`, `HubController`, `ReportController`, `KitchenController`, `MenuController`, …) |
| Business — domain | `saigonbite/business/domain/` — entities and state machines (`Order`, `Payment`, `Delivery`, `ReplacementOffer`, `Hub`, …) and pricing rules |
| Data access | `saigonbite/data_access/` — one DAO per table group; all SQL lives here |

Other files: `db/schema.sql` (13 tables, schema version 2), `db/seed.sql`, `init_db.py`, `app.py`, `tests/`,
`deploy/` (production Compose, Caddy, backup/restore, runbook), `models/`, `docs/`.

## Scope notes

Online payment is a simulator (no real provider or card data). Complaint handling, refund payout and rating are
deferred; a refund owed is recorded but not paid out. Business figures such as the 25 % quiet threshold and the 8 km
radius are team defaults until the client answers the open questions (report 1.4.2).
