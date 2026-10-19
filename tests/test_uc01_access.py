"""AC-8: login and customer role are enforced on the server."""
import pytest

from saigonbite.business.controllers import AuthorizationError, PlaceOrderController
from saigonbite.data_access import connect

from .conftest import ADDRESS_HOME, HUB_D1, PHO, add_second_customer, checkout_form, count, login

PROTECTED_GETS = ["/order/hubs", f"/order/hubs/{HUB_D1}", "/order/1/confirmation"]
PROTECTED_POSTS = ["/order/quote", "/order/confirm"]


@pytest.mark.parametrize("path", PROTECTED_GETS)
def test_T_UC01_40_anonymous_get_redirects_to_login(client, path):
    resp = client.get(path)
    assert resp.status_code == 302
    assert resp.headers["Location"].startswith("/login")


@pytest.mark.parametrize("path", PROTECTED_POSTS)
def test_T_UC01_41_anonymous_post_redirects_to_login_and_creates_no_order(client, db_path, path):
    resp = client.post(path, data=checkout_form())
    assert resp.status_code == 302
    assert resp.headers["Location"].startswith("/login")
    assert count(db_path, "orders") == 0


@pytest.mark.parametrize("username", ["kitchen", "shipper", "admin", "manager"])
def test_T_UC01_42_non_customer_roles_get_403_and_cannot_place_an_order(client, db_path, username):
    login(client, username)
    for path in PROTECTED_GETS:
        assert client.get(path).status_code == 403
    for path in PROTECTED_POSTS:
        assert client.post(path, data=checkout_form(token=f"t-{username}")).status_code == 403
    assert count(db_path, "orders") == 0


@pytest.mark.parametrize("user_id", [2, 3, 4, 5])
def test_T_UC01_43_controller_refuses_non_customer_users_even_if_the_view_is_bypassed(db_path, user_id):
    conn = connect(db_path)
    with pytest.raises(AuthorizationError):
        PlaceOrderController(conn).confirm_order(user_id, HUB_D1, ADDRESS_HOME, {PHO: "1"}, "tok-bypass")
    conn.close()
    assert count(db_path, "orders") == 0


def test_T_UC01_44_a_customer_cannot_open_another_customers_order(client, db_path):
    add_second_customer(db_path)
    login(client, "customer")
    client.post("/order/confirm", data=checkout_form(token="owner-token"))
    other = client.application.test_client()
    other.post("/login", data={"username": "other", "password": "dev-other"})
    assert other.get("/order/1/confirmation").status_code == 403
    assert client.get("/order/1/confirmation").status_code == 200
    assert client.get("/order/999/confirmation").status_code == 404


def test_T_UC01_45_login_with_wrong_password_is_refused(client):
    resp = client.post("/login", data={"username": "customer", "password": "wrong"})
    assert resp.status_code == 401
    assert "Wrong username or password" in resp.get_data(as_text=True)
    assert client.get("/order/hubs").status_code == 302


def test_T_UC01_46_login_redirects_back_to_the_requested_page_but_only_on_this_site(client):
    resp = client.post("/login", data={"username": "customer", "password": "dev-customer",
                                       "next": "http://evil.example/"})
    assert resp.headers["Location"] == "/order/hubs"
    client.post("/logout")
    resp = client.post("/login", data={"username": "customer", "password": "dev-customer",
                                       "next": f"/order/hubs/{HUB_D1}"})
    assert resp.headers["Location"] == f"/order/hubs/{HUB_D1}"


def test_T_UC01_47_logout_ends_the_session(customer_client):
    assert customer_client.get("/order/hubs").status_code == 200
    customer_client.post("/logout")
    assert customer_client.get("/order/hubs").status_code == 302


def test_T_UC01_48_home_page_is_public(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert "SaigonBite" in resp.get_data(as_text=True)
