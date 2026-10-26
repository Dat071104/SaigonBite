"""Review findings of 20/10: price change between quote and confirm (C-01, round 2), archived hub in history (C-02)."""
from .conftest import GOI_CUON, PHO, checkout_form, count, new_connection


def _raise_pho_price(db_path, price):
    conn = new_connection(db_path)
    conn.execute("UPDATE menu_item SET price = ? WHERE id = ?", (price, PHO))
    conn.commit()
    conn.close()


def test_T_UC01_49_quote_page_carries_the_total_the_customer_saw(customer_client):
    page = customer_client.post("/order/quote", data=checkout_form()).get_data(as_text=True)
    assert 'name="quoted_total" value="155000"' in page


def test_T_UC01_50_changed_price_shows_new_quote_and_writes_nothing(customer_client, db_path):
    _raise_pho_price(db_path, 65000)
    resp = customer_client.post("/order/confirm", data={**checkout_form(), "quoted_total": "155000"})
    assert resp.status_code == 409
    page = resp.get_data(as_text=True)
    assert 'id="quote-changed"' in page
    assert 'id="total">175,000 VND' in page                  # 2 x 65,000 + 35,000 + 15,000
    assert 'name="quoted_total" value="175000"' in page
    assert count(db_path, "orders") == 0 and count(db_path, "payment") == 0


def test_T_UC01_51_confirming_the_new_quote_saves_the_new_price(customer_client, db_path):
    _raise_pho_price(db_path, 65000)
    resp = customer_client.post("/order/confirm",
                                data={**checkout_form(token="tok-new"), "quoted_total": "175000"})
    assert resp.status_code == 303
    conn = new_connection(db_path)
    assert conn.execute("SELECT unit_price FROM order_line WHERE menu_item_id = ?", (PHO,)).fetchone()[0] == 65000
    assert conn.execute("SELECT amount FROM payment").fetchone()[0] == 175000


def test_T_UC01_52_confirmation_still_names_an_archived_hub(customer_client, db_path):
    """Review finding C-02: archiving a hub (UC-03, I2) must not blank out order history."""
    resp = customer_client.post("/order/confirm", data=checkout_form())
    conn = new_connection(db_path)
    conn.execute("UPDATE hub SET archived_at = '2026-10-20T00:00:00+00:00' WHERE id = 1")
    conn.commit()
    conn.close()
    page = customer_client.get(resp.headers["Location"]).get_data(as_text=True)
    assert "Hub: SaigonBite District 1 Hub" in page


def test_T_UC01_53_missing_or_broken_quoted_total_shows_the_quote_and_writes_nothing(customer_client, db_path):
    """Review round 2: a request without a usable quoted total must not skip the price check."""
    _raise_pho_price(db_path, 65000)
    for bad in (None, "not-a-number"):
        form = {k: v for k, v in checkout_form(token=f"tok-{bad}").items() if k != "quoted_total"}
        if bad is not None:
            form["quoted_total"] = bad
        resp = customer_client.post("/order/confirm", data=form)
        assert resp.status_code == 409
        assert 'id="total">175,000 VND' in resp.get_data(as_text=True)
    assert count(db_path, "orders") == 0 and count(db_path, "payment") == 0


def test_T_UC01_54_repeated_submit_of_a_placed_order_still_returns_it(customer_client, db_path):
    """The quote check runs only for new orders: a repeat of a saved token shows the first order."""
    first = customer_client.post("/order/confirm", data=checkout_form(token="tok-repeat"))
    assert first.status_code == 303
    form = {k: v for k, v in checkout_form(token="tok-repeat").items() if k != "quoted_total"}
    again = customer_client.post("/order/confirm", data=form)
    assert again.status_code == 303 and again.headers["Location"] == first.headers["Location"]
    assert count(db_path, "orders") == 1


def test_T_UC01_55_change_items_link_brings_the_cart_back(customer_client):
    """UX review: "Change items" on the quote page returns to the menu with the same quantities and address."""
    page = customer_client.post("/order/quote", data=checkout_form()).get_data(as_text=True)
    href = page.split('class="btn link" href="')[1].split('"')[0].replace("&amp;", "&")
    menu = customer_client.get(href).get_data(as_text=True)
    assert f'name="qty_{PHO}" value="2"' in menu and f'name="qty_{GOI_CUON}" value="1"' in menu
    assert '<option value="1" selected>' in menu
