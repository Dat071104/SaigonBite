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
