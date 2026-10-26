"""AC-6: invalid input gives a clear message and creates no order."""
import pytest

from .conftest import (ADDRESS_HOME, GOI_CUON, HUB_D1, NOT_AT_D1, PHO, SOLD_OUT_AT_D1, add_second_customer,
                       checkout_form, count)

CASES = [
    ("empty_cart", dict(quantities={}), "Your cart is empty"),
    ("blank_quantities", dict(quantities={PHO: "", GOI_CUON: " "}), "Your cart is empty"),
    ("quantity_zero", dict(quantities={PHO: "0"}), "must be at least 1"),
    ("quantity_negative", dict(quantities={PHO: "-3"}), "must be at least 1"),
    ("quantity_not_a_number", dict(quantities={PHO: "two"}), "must be a whole number"),
    ("quantity_too_large", dict(quantities={PHO: "100"}), "must be at most 99"),
    ("item_sold_out_at_hub", dict(quantities={SOLD_OUT_AT_D1: "1"}), "not available at SaigonBite District 1 Hub"),
    ("item_not_sold_at_hub", dict(quantities={NOT_AT_D1: "1"}), "not available at SaigonBite District 1 Hub"),
    ("item_does_not_exist", dict(quantities={999: "1"}), "not available"),
    ("missing_address", dict(address_id=None), "Please choose a delivery address"),
    ("unknown_hub", dict(hub_id=999), "Please choose a hub"),
]


def _assert_nothing_written(db_path):
    assert count(db_path, "orders") == 0
    assert count(db_path, "order_line") == 0
    assert count(db_path, "payment") == 0


@pytest.mark.parametrize("name,overrides,message", CASES, ids=[c[0] for c in CASES])
def test_T_UC01_20_confirm_rejects_invalid_input_without_creating_an_order(
        customer_client, db_path, name, overrides, message):
    resp = customer_client.post("/order/confirm", data=checkout_form(client=customer_client, token=f"tok-{name}", **overrides))
    page = resp.get_data(as_text=True)
    assert resp.status_code == 400
    assert message in page
    assert 'class="flash error"' in page
    _assert_nothing_written(db_path)


@pytest.mark.parametrize("name,overrides,message", CASES, ids=[c[0] for c in CASES])
def test_T_UC01_21_quote_rejects_the_same_invalid_input(customer_client, db_path, name, overrides, message):
    data = checkout_form(client=customer_client, token="unused", **overrides)
    del data["idempotency_token"]
    resp = customer_client.post("/order/quote", data=data)
    assert resp.status_code == 400
    assert message in resp.get_data(as_text=True)
    _assert_nothing_written(db_path)


def test_T_UC01_22_another_customers_address_is_refused(customer_client, db_path):
    add_second_customer(db_path)
    resp = customer_client.post("/order/confirm", data=checkout_form(client=customer_client, address_id=10))
    assert resp.status_code == 400
    assert "delivery address is not valid" in resp.get_data(as_text=True)
    _assert_nothing_written(db_path)


def test_T_UC01_23_missing_idempotency_token_creates_no_order(customer_client, db_path):
    data = checkout_form(client=customer_client)
    del data["idempotency_token"]
    resp = customer_client.post("/order/confirm", data=data)
    assert resp.status_code == 400
    assert "form has expired" in resp.get_data(as_text=True)
    _assert_nothing_written(db_path)


def test_T_UC01_24_entered_quantities_are_kept_when_the_form_is_shown_again(customer_client):
    resp = customer_client.post("/order/quote", data={"hub_id": HUB_D1, f"qty_{PHO}": "2"})
    page = resp.get_data(as_text=True)
    assert "Please choose a delivery address" in page
    assert f'name="qty_{PHO}" value="2"' in page
