"""AC-4 (one transaction: Order PLACED + lines + COD Payment PENDING) and AC-5 (read back via a new connection)."""
import pytest

from saigonbite.business.controllers import PlaceOrderController
from saigonbite.business.domain import OrderState
from saigonbite.data_access import OrderDAO, PaymentDAO, connect
from saigonbite.data_access import payment_dao

from .conftest import GOI_CUON, HUB_D1, PHO, ADDRESS_HOME, checkout_form, count, new_connection
from .p4_helpers import place


def _place(client, **kw):
    resp = client.post("/order/confirm", data=checkout_form(client=client, **kw))
    assert resp.status_code == 303
    return resp


def test_T_UC01_10_confirm_creates_placed_order_lines_and_pending_cod_payment(customer_client, db_path):
    resp = _place(customer_client)
    conn = new_connection(db_path)
    order = conn.execute("SELECT * FROM orders").fetchone()
    assert order["state"] == "PLACED" == OrderState.PLACED.value
    assert order["customer_id"] == 1 and order["hub_id"] == HUB_D1 and order["address_id"] == ADDRESS_HOME
    lines = conn.execute("SELECT menu_item_id, unit_price, quantity FROM order_line ORDER BY menu_item_id").fetchall()
    assert [(r["menu_item_id"], r["unit_price"], r["quantity"]) for r in lines] == [(PHO, 55000, 2), (GOI_CUON, 35000, 1)]
    pay = conn.execute("SELECT * FROM payment").fetchall()
    assert len(pay) == 1
    assert (pay[0]["order_id"], pay[0]["method"], pay[0]["state"], pay[0]["amount"]) == (order["id"], "COD", "PENDING", 155000)
    assert resp.headers["Location"].endswith(f"/order/{order['id']}/confirmation")


def test_T_UC01_11_confirmation_page_shows_order_id_and_total(customer_client, db_path):
    resp = _place(customer_client)
    page = customer_client.get(resp.headers["Location"]).get_data(as_text=True)
    order_id = new_connection(db_path).execute("SELECT id FROM orders").fetchone()["id"]
    assert f'<strong id="order-id">{order_id}</strong>' in page
    assert 'id="order-total">155,000 VND' in page
    assert 'id="order-state">PLACED' in page
    assert 'id="payment-method">COD' in page and 'id="payment-state">PENDING' in page


def test_T_UC01_12_transaction_is_begin_immediate_then_commit(db_path):
    conn = connect(db_path)
    statements = []
    conn.set_trace_callback(statements.append)
    place(conn,lines={PHO:'1'},token='tok-trace')
    conn.close()
    begin = statements.index("BEGIN IMMEDIATE")
    commit = statements.index("COMMIT")
    inserts = [i for i, s in enumerate(statements) if s.lstrip().upper().startswith("INSERT")]
    assert len(inserts) == 3                       # orders, one order_line, payment
    assert begin < min(inserts) and max(inserts) < commit


def test_T_UC01_13_failure_while_saving_payment_rolls_back_order_and_lines(db_path, monkeypatch):
    def boom(self, payment):
        raise RuntimeError("simulated disk error")
    monkeypatch.setattr(payment_dao.PaymentDAO, "insert", boom)
    conn = connect(db_path)
    with pytest.raises(RuntimeError):
        place(conn,lines={PHO:'2',GOI_CUON:'1'},token='tok-fail')
    conn.close()
    assert count(db_path, "orders") == 0
    assert count(db_path, "order_line") == 0
    assert count(db_path, "payment") == 0


def test_T_UC01_14_read_back_through_new_connection_same_lines_and_total(customer_client, db_path):
    """AC-5"""
    shown_total = 155000
    _place(customer_client)

    fresh = new_connection(db_path)                 # a NEW connection, nothing shared with the app
    header = fresh.execute("SELECT id, item_subtotal, delivery_fee, total_amount FROM orders").fetchone()
    lines = fresh.execute("SELECT item_name, unit_price, quantity FROM order_line WHERE order_id = ? ORDER BY id",
                          (header["id"],)).fetchall()
    assert [(r["item_name"], r["unit_price"], r["quantity"]) for r in lines] == [
        ("Pho bo tai", 55000, 2), ("Goi cuon", 35000, 1)]
    assert sum(r["unit_price"] * r["quantity"] for r in lines) == header["item_subtotal"] == 145000
    assert header["total_amount"] == header["item_subtotal"] + header["delivery_fee"] - 5000 == shown_total
    fresh.close()

    dao_conn = connect(db_path)                     # and through the DAO on another new connection
    order = OrderDAO(dao_conn).get_by_id(header["id"])
    assert order.total == shown_total and len(order.lines) == 2 and order.state is OrderState.PLACED
    assert PaymentDAO(dao_conn).get_by_order_id(order.id).amount == shown_total
    dao_conn.close()
