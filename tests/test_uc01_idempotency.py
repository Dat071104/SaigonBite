"""AC-7: pressing confirm twice creates exactly one order."""
import threading

from saigonbite.business.controllers import PlaceOrderController
from saigonbite.data_access import connect

from .conftest import ADDRESS_HOME, GOI_CUON, HUB_D1, PHO, checkout_form, count
from saigonbite.business.domain import PaymentMethod


def test_T_UC01_30_double_submit_creates_exactly_one_order(customer_client, db_path):
    first = customer_client.post("/order/confirm", data=checkout_form(client=customer_client, token="same-token"))
    second = customer_client.post("/order/confirm", data=checkout_form(client=customer_client, token="same-token"))
    assert first.status_code == second.status_code == 303
    assert first.headers["Location"] == second.headers["Location"]       # same order shown again
    assert count(db_path, "orders") == 1
    assert count(db_path, "order_line") == 2
    assert count(db_path, "payment") == 1


def test_T_UC01_31_quote_page_issues_a_fresh_token_each_time(customer_client):
    data = {"hub_id": HUB_D1, "address_id": ADDRESS_HOME, f"qty_{PHO}": "1"}
    tokens = []
    for _ in range(2):
        page = customer_client.post("/order/quote", data=data).get_data(as_text=True)
        marker = 'name="idempotency_token" value="'
        tokens.append(page.split(marker)[1].split('"')[0])
    assert tokens[0] and tokens[1] and tokens[0] != tokens[1]


def test_T_UC01_32_end_to_end_quote_then_double_click_on_confirm(customer_client, db_path):
    quote_page = customer_client.post("/order/quote", data={
        "hub_id": HUB_D1, "address_id": ADDRESS_HOME, f"qty_{PHO}": "1", f"qty_{GOI_CUON}": "3"}).get_data(as_text=True)
    token = quote_page.split('name="idempotency_token" value="')[1].split('"')[0]
    total = quote_page.split('name="quoted_total" value="')[1].split('"')[0]
    form = {"hub_id": HUB_D1, "address_id": ADDRESS_HOME, "idempotency_token": token, "quoted_total": total,
            'quote_fingerprint':quote_page.split('name="quote_fingerprint" value="')[1].split('"')[0],
            f"qty_{PHO}": "1", f"qty_{GOI_CUON}": "3"}
    for _ in range(2):
        assert customer_client.post("/order/confirm", data=form).status_code == 303
    assert count(db_path, "orders") == 1


def test_T_UC01_33_different_tokens_create_different_orders(customer_client, db_path):
    customer_client.post("/order/confirm", data=checkout_form(client=customer_client, token="a"))
    customer_client.post("/order/confirm", data=checkout_form(client=customer_client, token="b"))
    assert count(db_path, "orders") == 2


def test_T_UC01_34_concurrent_submits_with_one_token_still_create_one_order(db_path):
    results, errors = [], []
    barrier = threading.Barrier(5, timeout=10)

    def submit():
        conn = None
        try:
            conn = connect(db_path)
            controller = PlaceOrderController(conn)
            consent = controller.request_quote(1,HUB_D1,ADDRESS_HOME,{PHO:'1'}).fingerprint(PaymentMethod.COD)
            barrier.wait()
            results.append(PlaceOrderController(conn).confirm_order(
                1, HUB_D1, ADDRESS_HOME, {PHO: "1"}, "race-token", 65000,quote_fingerprint=consent))
        except Exception as exc:        # pragma: no cover - would fail the assertions below
            errors.append(exc)
            barrier.abort()
        finally:
            if conn is not None:
                conn.close()

    threads = [threading.Thread(target=submit) for _ in range(5)]
    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=20)
        assert not t.is_alive()
    assert not errors
    assert len({r.order.id for r in results}) == 1
    assert sum(1 for r in results if r.created) == 1
    assert count(db_path, "orders") == 1 and count(db_path, "payment") == 1
