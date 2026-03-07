import requests
import uuid

BASE_URL = "http://127.0.0.1:8000"

def register_user():
    username = f"testuser_{uuid.uuid4().hex[:8]}"
    password = "testpassword123"
    payload = {
        "username": username,
        "password": password
    }
    response = requests.post(f"{BASE_URL}/auth/register", json=payload)
    return response, username, password

def login_user(username, password):
    payload = {
        "username": username,
        "password": password
    }
    response = requests.post(f"{BASE_URL}/auth/login", data=payload)
    return response

def get_auth_headers():
    _, username, password = register_user()
    response = login_user(username, password)
    token = response.json().get("access_token")
    return {"Authorization": f"Bearer {token}"}
