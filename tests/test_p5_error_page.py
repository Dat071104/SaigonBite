"""P5-D03 regression: a signed-in user who reaches an error page (for example a shipper who lost the pick-up
race and is sent to a delivery that now belongs to someone else) was offered only "Back to the home page";
the error page now links to the user's own first screen.

Author: 722I0004 · AI-assisted (Claude Sonnet 5.5)
"""
from .conftest import login


def test_error_page_links_back_to_the_users_own_first_screen(client):
    login(client, "customer")
    resp = client.get("/admin/hubs")
    page = resp.get_data(as_text=True)
    assert resp.status_code == 403
    assert 'href="/order/hubs"' in page and "Back to order food" in page
    shipper = login(client.application.test_client(), "shipper")
    page = shipper.get("/admin/hubs").get_data(as_text=True)
    assert 'href="/delivery/"' in page and "Back to deliveries" in page


def test_error_page_for_an_anonymous_visitor_still_links_home(client):
    page = client.get("/no-such-page").get_data(as_text=True)
    assert "Back to the home page" in page
