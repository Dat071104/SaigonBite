"""Deployment copies: Vercel serves static files from public/, so it must match the app's static folder."""
import filecmp
import os
import subprocess

from init_db import ROOT

STATIC = os.path.join(ROOT, "saigonbite", "presentation", "static")
PUBLIC = os.path.join(ROOT, "public", "static")


def test_T_DEP_01_public_static_matches_the_app_static_folder(client):
    """D-5 retires Vercel: preserve its G3 bytes; running Flask serves current app assets."""
    names = sorted(os.listdir(STATIC))
    assert sorted(os.listdir(PUBLIC)) == names
    for name in names:
        historical = subprocess.check_output(['git','show',f'6e8cafe245c87d3aab7f99535960ad5d7111d320:public/static/{name}'], cwd=ROOT)
        with open(os.path.join(PUBLIC,name),'rb') as source:
            assert source.read() == historical
        with open(os.path.join(STATIC,name),'rb') as source:
            response = client.get('/static/'+name)
            assert response.status_code == 200 and response.data == source.read()


def test_T_DEP_02_pages_name_a_favicon_and_favicon_ico_resolves(client):
    assert "favicon.svg" in client.get("/").get_data(as_text=True)
    resp = client.get("/favicon.ico")
    assert resp.status_code == 301
    assert client.get(resp.headers["Location"]).status_code == 200
