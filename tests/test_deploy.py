"""Deployment copies: Vercel serves static files from public/, so it must match the app's static folder."""
import filecmp
import os

from init_db import ROOT

STATIC = os.path.join(ROOT, "saigonbite", "presentation", "static")
PUBLIC = os.path.join(ROOT, "public", "static")


def test_T_DEP_01_public_static_matches_the_app_static_folder():
    names = sorted(os.listdir(STATIC))
    assert sorted(os.listdir(PUBLIC)) == names
    match, mismatch, errors = filecmp.cmpfiles(STATIC, PUBLIC, names, shallow=False)
    assert not mismatch and not errors


def test_T_DEP_02_pages_name_a_favicon_and_favicon_ico_resolves(client):
    assert "favicon.svg" in client.get("/").get_data(as_text=True)
    resp = client.get("/favicon.ico")
    assert resp.status_code == 301
    assert client.get(resp.headers["Location"]).status_code == 200
