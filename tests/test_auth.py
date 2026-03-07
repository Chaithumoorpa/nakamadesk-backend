import requests
from tests.utils import BASE_URL, register_user, login_user

def test_register_new_user():
    response, _, _ = register_user()
    assert response.status_code == 200
    assert "username" in response.json()

def test_register_duplicate_user():
    _, username, password = register_user()
    
    # Try to register again with same username
    payload = {
        "username": username,
        "password": password
    }
    response = requests.post(f"{BASE_URL}/auth/register", json=payload)
    assert response.status_code == 400

def test_login_valid_user():
    _, username, password = register_user()
    response = login_user(username, password)
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_access_protected_endpoint():
    _, username, password = register_user()
    login_response = login_user(username, password)
    token = login_response.json().get("access_token")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
    assert response.status_code == 200
    assert response.json().get("username") == username