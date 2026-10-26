"""P5 regression (P5-D02): choosing online payment on the quote page must not show a false
"price changed" notice.

The consent fingerprint (BR-10) binds the payment choice. The quote is requested before the customer picks
how to pay, so the hidden quote_fingerprint belongs to cash on delivery; switching the radio to online made
every first online confirmation return 409 "The price changed since your quote" although nothing had changed.
The server contract is unchanged (and sealed by the P4 dependency policy). app.js now asks /order/quote for
the fingerprint of the chosen payment before it sends the form; this file pins the server side of that
exchange and the hooks the script needs. The browser behaviour itself is demonstrated in integration scenario 6.

Author: 722I0004 · AI-assisted (Claude Sonnet 5.5)
"""
import re
from pathlib import Path

from saigonbite.business.controllers import PlaceOrderController
from saigonbite.business.controllers.presentation_contract import OnlineOption, PaymentMethod
from saigonbite.data_access import connect

from .conftest import ADDRESS_HOME, HUB_D1, PHO, login

FORM = {"hub_id": HUB_D1, "address_id": ADDRESS_HOME, f"qty_{PHO}": "2"}


def _fingerprint_of(page: str) -> str:
    return re.search(r'name="quote_fingerprint" value="([0-9a-f]{64})"', page)[1]


def test_quote_page_tells_the_script_which_payment_the_fingerprint_belongs_to(client):
    login(client, "customer")
    page = client.post("/order/quote", data=FORM).get_data(as_text=True)
    assert 'data-quoted-payment="COD"' in page and 'data-requote-url="/order/quote"' in page
    online = client.post("/order/quote", data={**FORM, "payment": "ONLINE:E_WALLET"}).get_data(as_text=True)
    assert 'data-quoted-payment="ONLINE:E_WALLET"' in online
    assert 'value="ONLINE:E_WALLET" checked' in online


def test_requote_for_the_chosen_payment_gives_the_fingerprint_the_confirmation_expects(client, db_path):
    login(client, "customer")
    cod_page = client.post("/order/quote", data=FORM).get_data(as_text=True)
    online_page = client.post("/order/quote", data={**FORM, "payment": "ONLINE:E_WALLET"}).get_data(as_text=True)
    q = PlaceOrderController(connect(db_path)).request_quote(1, HUB_D1, ADDRESS_HOME, {PHO: "2"})
    assert _fingerprint_of(cod_page) == q.fingerprint(PaymentMethod.COD)
    assert _fingerprint_of(online_page) == q.fingerprint(PaymentMethod.ONLINE, OnlineOption.E_WALLET)
    total = re.search(r'name="quoted_total" value="(\d+)"', cod_page)[1]
    confirm = {**FORM, "idempotency_token": "p5-d02", "quoted_total": total, "payment": "ONLINE:E_WALLET"}
    # What the page did before the fix: the COD fingerprint with an online choice is a (false) changed quote
    assert client.post("/order/confirm", data={**confirm, "quote_fingerprint": _fingerprint_of(cod_page)}).status_code == 409
    # What the page does now: the fingerprint of the chosen payment goes to the simulator
    resp = client.post("/order/confirm", data={**confirm, "quote_fingerprint": _fingerprint_of(online_page)})
    assert resp.status_code == 200 and "Payment simulator" in resp.get_data(as_text=True)


def test_script_carries_the_requote_hook():
    js = (Path(__file__).resolve().parents[1] / "saigonbite/presentation/static/app.js").read_text(encoding="utf-8")
    assert "dataset.requoteUrl" in js and "dataset.quotedPayment" in js and "quote_fingerprint" in js
