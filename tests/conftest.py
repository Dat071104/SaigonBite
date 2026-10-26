"""Shared fixtures. Every test gets its own temporary SQLite database built from schema.sql + seed.sql."""
import os
import sqlite3
import sys
import secrets
from flask.testing import FlaskClient

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from init_db import build_database  # noqa: E402
from saigonbite import create_app   # noqa: E402

# Seeded dev accounts (README.md): every account uses the demo password below.
DEMO_PASSWORD = "123456"
SEED_USERS = ("customer", "kitchen", "shipper", "admin", "manager")
HUB_D1, HUB_BT = 1, 2
ADDRESS_HOME = 1
# Menu items (seed.sql): 1 Pho bo tai 55000, 3 Goi cuon 35000, 5 sold out at hub 1, 9 not sold at hub 1
PHO, GOI_CUON, SOLD_OUT_AT_D1, NOT_AT_D1 = 1, 3, 5, 9


@pytest.fixture
def db_path(tmp_path):
    path = str(tmp_path / "test.db")
    build_database(path)
    return path


@pytest.fixture
def app(db_path):
    application = create_app({"TESTING": True, "DATABASE": db_path, "SECRET_KEY": "test-secret"})
    application.test_client_class = SessionFormClient
    return application


class SessionFormClient(FlaskClient):
    """Explicit valid-token requests by default; csrf=False exercises missing-token denial."""
    def open(self, *args, **kwargs):
        attach = kwargs.pop('csrf', True)
        if kwargs.get('method', 'GET').upper() in ('POST', 'PUT', 'PATCH', 'DELETE') and attach:
            with self.session_transaction() as state:
                token = state.setdefault('csrf_token', secrets.token_urlsafe(32))
            kwargs['data'] = {**(kwargs.get('data') or {})}
            kwargs['data'].setdefault('csrf_token', token)
        return super().open(*args, **kwargs)


@pytest.fixture
def client(app):
    return app.test_client()


def login(client, username):
    resp = client.post("/login", data={"username": username, "password": DEMO_PASSWORD})
    assert resp.status_code == 302, resp.get_data(as_text=True)
    return client


@pytest.fixture
def customer_client(client):
    return login(client, "customer")


def new_connection(db_path):
    """A brand-new sqlite3 connection (used to read persisted data back, AC-5)."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def count(db_path, table):
    conn = new_connection(db_path)
    try:
        return conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
    finally:
        conn.close()


def _seed_prices():
    """Independent fixed seed oracle, evaluated lazily; no production-pricing call or DB query.

    BR-07: D1 12000+3000*1=15000; BT 10000+3000*5=25000.
    Both seeded hubs are initially quiet: BR-03 subtracts 5000 at checkout.
    """
    return {1:55000,2:50000,3:35000,4:60000,5:55000,6:10000,7:30000,8:25000,9:30000,10:28000}, {1:15000,2:25000}


def quoted_total(hub_id, quantities):
    """The total the quote page shows for valid quantities (seed prices)."""
    prices, fees = _seed_prices()
    return fees[hub_id] - 5000 + sum(prices[i] * int(q) for i, q in quantities.items() if str(q).strip())


def checkout_form(token="tok-1", hub_id=HUB_D1, address_id=ADDRESS_HOME, quantities=None, client=None):
    """Form data as the quote page would post it to /order/confirm (with the quoted total when it can be computed)."""
    data = {"hub_id": hub_id, "idempotency_token": token}
    if address_id is not None:
        data["address_id"] = address_id
    quantities = quantities if quantities is not None else {PHO: "2", GOI_CUON: "1"}
    for item_id, qty in quantities.items():
        data[f"qty_{item_id}"] = qty
    try:
        data["quoted_total"] = quoted_total(hub_id, quantities)
    except (KeyError, ValueError, TypeError):
        pass                            # invalid input: the request is refused before the totals are compared
    if client is not None:
        import re
        page = client.post('/order/quote',data=data)
        match = re.search(r'name="quote_fingerprint" value="([^"]+)"',page.get_data(as_text=True))
        if match:
            data['quote_fingerprint'] = match[1]
    return data


def add_second_customer(db_path):
    """Insert a second customer (user 'other') with its own address, for ownership tests."""
    from werkzeug.security import generate_password_hash
    conn = new_connection(db_path)
    conn.execute("INSERT INTO user_account (id, username, password_hash, display_name, role) "
                 "VALUES (10, 'other', ?, 'Other Customer', 'CUSTOMER')",
                 (generate_password_hash("dev-other", method="pbkdf2:sha256:1000"),))
    conn.execute("INSERT INTO customer (id, user_id, full_name, phone, customer_type) "
                 "VALUES (10, 10, 'Other Customer', '0900000000', 'LOCAL')")
    conn.execute("INSERT INTO address (id, customer_id, label, full_address, district, latitude, longitude) "
                 "VALUES (10, 10, 'Home', '1 Other Street, District 3, Ho Chi Minh City', 'District 3', 10.7843, 106.6844)")
    conn.commit()
    conn.close()
