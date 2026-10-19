"""AC-3: a logged-in customer sees item subtotal, flat delivery fee and total before confirming."""
from saigonbite.business.domain import Address, Hub, OrderLine, Quote

from .conftest import ADDRESS_HOME, GOI_CUON, HUB_BT, HUB_D1, PHO, count


def test_T_UC01_01_quote_shows_subtotal_fee_and_total(customer_client, db_path):
    resp = customer_client.post("/order/quote", data={
        "hub_id": HUB_D1, "address_id": ADDRESS_HOME, f"qty_{PHO}": "2", f"qty_{GOI_CUON}": "1"})
    page = resp.get_data(as_text=True)
    assert resp.status_code == 200
    # 2 x 55,000 + 1 x 35,000 = 145,000 ; flat fee of hub 1 = 15,000 ; total = 160,000
    assert '<td class="num" id="item-subtotal">145,000 VND</td>' in page
    assert '<td class="num" id="delivery-fee">15,000 VND</td>' in page
    assert '<td class="num" id="total">160,000 VND</td>' in page
    assert "Pho bo tai" in page and "Goi cuon" in page
    assert count(db_path, "orders") == 0           # a quote writes nothing


def test_T_UC01_02_flat_fee_is_the_seeded_value_of_the_chosen_hub(customer_client):
    resp = customer_client.post("/order/quote", data={
        "hub_id": HUB_BT, "address_id": ADDRESS_HOME, "qty_9": "1"})   # Che thai 30,000 + 18,000
    page = resp.get_data(as_text=True)
    assert resp.status_code == 200
    assert 'id="delivery-fee">18,000 VND' in page and 'id="total">48,000 VND' in page


def test_T_UC01_03_choose_hub_and_item_pages_list_hubs_menu_and_address(customer_client):
    hubs = customer_client.get("/order/hubs").get_data(as_text=True)
    assert "SaigonBite District 1 Hub" in hubs and "SaigonBite Binh Thanh Hub" in hubs
    menu = customer_client.get(f"/order/hubs/{HUB_D1}").get_data(as_text=True)
    assert "Pho bo tai" in menu and "12 Nguyen Hue" in menu
    assert "Sold out" in menu                      # item 5 is unavailable at hub 1


def test_T_UC01_04_domain_quote_arithmetic():
    hub = Hub(id=1, code="H", name="H", address_text="a", max_active_orders=5, delivery_fee_flat=15000)
    quote = Quote(hub=hub, address=Address(1, 1, "Home", "x"),
                  lines=[OrderLine(1, "A", 55000, 2), OrderLine(3, "B", 35000, 1)])
    assert (quote.item_subtotal, quote.delivery_fee, quote.total) == (145000, 15000, 160000)
