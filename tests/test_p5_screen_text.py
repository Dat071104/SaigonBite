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
