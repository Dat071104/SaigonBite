"""P5-D04 regression: the quote table printed the raw distance ("Delivery fee (0.38971718085988794 km)");
every other screen shows two decimals.

Author: 722I0004 · AI-assisted (Claude Sonnet 5.5)
"""
import re

from .conftest import ADDRESS_HOME, HUB_D1, PHO, login


def test_quote_table_shows_the_distance_with_two_decimals(client):
    login(client, "customer")
    page = client.post("/order/quote", data={"hub_id": HUB_D1, "address_id": ADDRESS_HOME,
                                             f"qty_{PHO}": "1"}).get_data(as_text=True)
    assert "Delivery fee (0.39 km)" in page
    assert not re.search(r"\(\d+\.\d{3,} km\)", page)


def test_sales_report_shows_a_zero_voucher_total_without_a_minus_sign(client):
    """P5.1: an empty period printed "-0 VND" in the Vouchers column."""
    login(client, "manager")
    page = client.get("/reports/sales?from=2030-01-01&to=2030-01-31").get_data(as_text=True)
    assert "-0 VND" not in page and "0 VND" in page
    seeded = client.get("/reports/sales?from=2026-10-20&to=2026-10-20").get_data(as_text=True)
    assert "-0 VND" not in seeded


def test_rejected_online_order_names_the_amount_a_refund_owed(client, db_path):
    """P5-D05: the order page said "65,000 VND to be refunded"; BR-13/BR-17 and the receipt say refund owed,
    payout pending (the money is an obligation, not a payout)."""
    from saigonbite.business.controllers import KitchenController, PaymentChoice
    from saigonbite.business.controllers.presentation_contract import APPROVE, OnlineOption, PaymentMethod
    from saigonbite.data_access import connect
    from .p4_helpers import place
    conn = connect(db_path)
    result = place(conn, lines={PHO: "1"}, payment=PaymentChoice(method=PaymentMethod.ONLINE, option=OnlineOption.E_WALLET, outcome=APPROVE))
    KitchenController(conn).reject_order(2, result.order.id, "Out of broth")
    login(client, "customer")
    page = client.get(f"/order/{result.order.id}").get_data(as_text=True)
    assert "refund owed" in page and "payout pending" in page
    assert "to be refunded" not in page
