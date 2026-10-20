"""Review findings of 20/10: C-01 price change between quote and confirm, C-02 archived hub in history."""
from .conftest import PHO, checkout_form, count, new_connection


def _raise_pho_price(db_path, price):
    conn = new_connection(db_path)
    conn.execute("UPDATE menu_item SET price = ? WHERE id = ?", (price, PHO))
    conn.commit()
    conn.close()


def test_T_UC01_49_quote_page_carries_the_total_the_customer_saw(customer_client):
    page = customer_client.post("/order/quote", data=checkout_form()).get_data(as_text=True)
    assert 'name="quoted_total" value="160000"' in page


def test_T_UC01_50_changed_price_shows_new_quote_and_writes_nothing(customer_client, db_path):
    _raise_pho_price(db_path, 65000)
    resp = customer_client.post("/order/confirm", data={**checkout_form(), "quoted_total": "160000"})
    assert resp.status_code == 409
    page = resp.get_data(as_text=True)
    assert 'id="quote-changed"' in page
    assert 'id="total">180,000 VND' in page                  # 2 x 65,000 + 35,000 + 15,000
    assert 'name="quoted_total" value="180000"' in page
    assert count(db_path, "orders") == 0 and count(db_path, "payment") == 0


def test_T_UC01_51_confirming_the_new_quote_saves_the_new_price(customer_client, db_path):
    _raise_pho_price(db_path, 65000)
    resp = customer_client.post("/order/confirm",
                                data={**checkout_form(token="tok-new"), "quoted_total": "180000"})
    assert resp.status_code == 303
    conn = new_connection(db_path)
    assert conn.execute("SELECT unit_price FROM order_line WHERE menu_item_id = ?", (PHO,)).fetchone()[0] == 65000
    assert conn.execute("SELECT amount FROM payment").fetchone()[0] == 180000


def test_T_UC01_52_confirmation_still_names_an_archived_hub(customer_client, db_path):
    """Review finding C-02: archiving a hub (UC-03, I2) must not blank out order history."""
    resp = customer_client.post("/order/confirm", data=checkout_form())
    conn = new_connection(db_path)
    conn.execute("UPDATE hub SET archived_at = '2026-10-20T00:00:00+00:00' WHERE id = 1")
    conn.commit()
    conn.close()
    page = customer_client.get(resp.headers["Location"]).get_data(as_text=True)
    assert "Hub: SaigonBite District 1 Hub" in page
