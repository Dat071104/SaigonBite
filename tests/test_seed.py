"""AC-2: init_db.py loads the seed. Also checks the frozen vocabulary against the schema."""
import re

from werkzeug.security import check_password_hash

from init_db import SCHEMA_PATH, main as init_main
from saigonbite.business.domain import OrderState, PaymentState, Role

from .conftest import DEMO_PASSWORD, SEED_USERS, new_connection


def test_T_SEED_01_at_least_two_hubs_with_capacity_and_menu(db_path):
    conn = new_connection(db_path)
    hubs = conn.execute("SELECT id, max_active_orders FROM hub").fetchall()
    assert len(hubs) >= 2
    for hub in hubs:
        assert hub["max_active_orders"] > 0
        available = conn.execute("SELECT COUNT(*) FROM hub_menu_item WHERE hub_id = ? AND is_available = 1",
                                 (hub["id"],)).fetchone()[0]
        assert available >= 1
    assert conn.execute("SELECT COUNT(*) FROM brand").fetchone()[0] >= 2
    assert conn.execute("SELECT COUNT(*) FROM menu_item").fetchone()[0] >= 2


def test_T_SEED_02_one_local_customer_with_an_address(db_path):
    conn = new_connection(db_path)
    rows = conn.execute("SELECT id, customer_type FROM customer").fetchall()
    assert len(rows) == 1 and rows[0]["customer_type"] == "LOCAL"
    assert conn.execute("SELECT COUNT(*) FROM address WHERE customer_id = ?", (rows[0]["id"],)).fetchone()[0] >= 1


def test_T_SEED_03_one_user_per_role_with_hashed_passwords(db_path):
    conn = new_connection(db_path)
    roles = {r["role"] for r in conn.execute("SELECT role FROM user_account")}
    assert roles == {r.value for r in Role} == {"CUSTOMER", "KITCHEN_STAFF", "SHIPPER", "ADMIN", "MANAGER"}
    for username in SEED_USERS:
        row = conn.execute("SELECT password_hash FROM user_account WHERE username = ?", (username,)).fetchone()
        assert row is not None
        assert row["password_hash"] != DEMO_PASSWORD                # not stored in clear
        assert check_password_hash(row["password_hash"], DEMO_PASSWORD)


def test_T_SEED_04_init_db_refuses_to_overwrite_without_force(db_path, capsys):
    assert init_main(["--db", db_path]) == 1
    assert init_main(["--db", db_path, "--force"]) == 0
    assert "Seeded:" in capsys.readouterr().out


def test_T_SEED_05_schema_states_equal_python_enums():
    """Order, payment and role names in schema.sql CHECK constraints are the enum values (AC-9)."""
    sql = open(SCHEMA_PATH, encoding="utf-8").read()

    orders_block = sql[sql.index("CREATE TABLE orders"):sql.index("CREATE TABLE order_line")]
    assert set(re.findall(r"'([A-Z_]+)'", orders_block)) == {s.value for s in OrderState}
    payment_block = sql[sql.index("CREATE TABLE payment"):sql.index("CREATE INDEX")]
    assert {s.value for s in PaymentState} <= set(re.findall(r"'([A-Z_]+)'", payment_block))
    assert {s.value for s in PaymentState} == {"PENDING", "PAID", "FAILED", "VOIDED", "REFUND_PENDING", "REFUNDED"}


def test_T_SEED_06_order_states_are_exactly_the_frozen_nine():
    assert [s.value for s in OrderState] == [
        "PLACED", "CONFIRMED", "REJECTED", "PREPARING", "READY",
        "OUT_FOR_DELIVERY", "DELIVERED", "DELIVERY_FAILED", "CANCELLED"]
