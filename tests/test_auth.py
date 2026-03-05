import requests

BASE_URL = "http://127.0.0.1:8000"


def test_register():
    payload = {
        "username": "testuser",
        "password": "test123"
    }

    r = requests.post(f"{BASE_URL}/auth/register", json=payload)

    assert r.status_code == 200


def test_login():

    data = {
        "username": "testuser",
        "password": "test123"
    }

    r = requests.post(f"{BASE_URL}/auth/login", params=data)

    assert r.status_code == 200
    assert "access_token" in r.json()