"""P5 regression: a value the server accepts and the seed data contains must also pass the browser's own
constraint check (min / step / max of <input type=number>) on the admin forms.

P5-D01 (found in the browser run): the dish price field had min="1" step="1000", so the browser only
accepted 1, 1001, 2001 ... and refused every seed price (all multiples of 1000), blocking Save dish.

Author: 722I0004 · AI-assisted (Claude Sonnet 5.5)
"""
import re
from decimal import Decimal

import pytest

from .conftest import login

INPUT = re.compile(r"<input\b[^>]*\btype=\"number\"[^>]*>", re.I)
ATTR = re.compile(r"([\w-]+)=\"([^\"]*)\"")


def number_inputs(html: str):
    for tag in INPUT.findall(html):
        attrs = dict(ATTR.findall(tag))
        yield attrs.get("name"), attrs


def passes_browser_constraints(value: str, attrs: dict) -> bool:
    """HTML constraint validation for a number input: min, max, and step counted from min (or value)."""
    v = Decimal(value)
    if "min" in attrs and v < Decimal(attrs["min"]):
        return False
    if "max" in attrs and v > Decimal(attrs["max"]):
        return False
    step = attrs.get("step", "1")
    if step == "any":
        return True
    base = Decimal(attrs["min"]) if "min" in attrs else Decimal(attrs.get("value") or 0)
    return (v - base) % Decimal(step) == 0


def test_dish_price_field_accepts_every_seed_price(client):
    login(client, "admin")
    new_page = client.get("/admin/items/new").get_data(as_text=True)
    price = dict(number_inputs(new_page))["price"]
    for item_id, seed_price in enumerate((55000, 50000, 35000, 60000, 55000, 10000, 30000, 25000, 30000, 28000), 1):
        page = client.get(f"/admin/items/{item_id}").get_data(as_text=True)
        edit = dict(number_inputs(page))["price"]
        assert edit["value"] == str(seed_price)
        assert passes_browser_constraints(str(seed_price), edit), f"item {item_id}: {seed_price} refused by the browser"
        assert passes_browser_constraints(str(seed_price), price), f"new dish form refuses {seed_price}"


@pytest.mark.parametrize("url", ["/admin/hubs/1", "/admin/hubs/2", "/admin/vouchers/1", "/admin/vouchers/2"])
def test_saved_values_on_edit_forms_pass_the_browser_check(client, url):
    login(client, "admin")
    page = client.get(url).get_data(as_text=True)
    for name, attrs in number_inputs(page):
        value = attrs.get("value")
        if value:
            assert passes_browser_constraints(value, attrs), f"{url}: {name}={value} refused by the browser"
