import requests
from tests.utils import BASE_URL, get_auth_headers

def _create_item():
    headers = get_auth_headers()
    payload = {
        "name": "Test Chair",
        "category": "Furniture",
        "price": 100.0,
        "stock_quantity": 20
    }
    response = requests.post(f"{BASE_URL}/items", json=payload, headers=headers)
    return response.json()["id"]

def test_create_item():
    headers = get_auth_headers()
    payload = {
        "name": "Test Chair",
        "category": "Furniture",
        "price": 100.0,
        "stock_quantity": 20
    }
    response = requests.post(f"{BASE_URL}/items", json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json()["name"] == "Test Chair"

def test_list_items():
    headers = get_auth_headers()
    response = requests.get(f"{BASE_URL}/items", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_fetch_item_by_id():
    item_id = _create_item()
    headers = get_auth_headers()
    
    response = requests.get(f"{BASE_URL}/items/{item_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["id"] == item_id

def test_update_item():
    item_id = _create_item()
    headers = get_auth_headers()
    
    update_payload = {
        "name": "Updated Chair",
        "category": "Furniture",
        "price": 150.0,
        "stock_quantity": 25
    }
    response = requests.put(f"{BASE_URL}/items/{item_id}", json=update_payload, headers=headers)
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Chair"
    assert response.json()["price"] == 150.0

def test_adjust_stock():
    item_id = _create_item()
    headers = get_auth_headers()
    
    # We started with 20 quantity, let's adjust by -5
    payload = {"quantity": -5}
    response = requests.patch(f"{BASE_URL}/items/{item_id}/stock", json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json()["stock_quantity"] == 15

def test_delete_item():
    item_id = _create_item()
    headers = get_auth_headers()
    
    response = requests.delete(f"{BASE_URL}/items/{item_id}", headers=headers)
    assert response.status_code == 200
    
    # Verify it is deleted
    get_response = requests.get(f"{BASE_URL}/items/{item_id}", headers=headers)
    assert get_response.status_code == 404
