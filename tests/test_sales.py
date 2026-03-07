import requests
from tests.utils import BASE_URL, get_auth_headers

def _create_item_and_sale():
    headers = get_auth_headers()
    item_payload = {
        "name": "Selling Item",
        "category": "SalesTest",
        "price": 50.0,
        "stock_quantity": 10
    }
    item_response = requests.post(f"{BASE_URL}/items", json=item_payload, headers=headers)
    item_id = item_response.json()["id"]
    
    sale_payload = {
        "items": [
            {
                "item_id": item_id,
                "quantity": 3
            }
        ]
    }
    sale_response = requests.post(f"{BASE_URL}/sales", json=sale_payload, headers=headers)
    return sale_response.json()["id"]

def test_create_item_and_sale():
    headers = get_auth_headers()
    
    # Step 1: Create an item with stock 10
    item_payload = {
        "name": "Selling Item",
        "category": "SalesTest",
        "price": 50.0,
        "stock_quantity": 10
    }
    item_response = requests.post(f"{BASE_URL}/items", json=item_payload, headers=headers)
    assert item_response.status_code == 200
    item_id = item_response.json()["id"]
    
    # Step 2: Create a sale with quantity 3
    sale_payload = {
        "items": [
            {
                "item_id": item_id,
                "quantity": 3
            }
        ]
    }
    sale_response = requests.post(f"{BASE_URL}/sales", json=sale_payload, headers=headers)
    assert sale_response.status_code == 200
    assert sale_response.json()["total_amount"] == 150.0  # 3 * 50
    
    # Step 3: Verify the stock is reduced to 7
    verify_item_response = requests.get(f"{BASE_URL}/items/{item_id}", headers=headers)
    assert verify_item_response.status_code == 200
    assert verify_item_response.json()["stock_quantity"] == 7

def test_list_sales():
    headers = get_auth_headers()
    # Ensure there is at least one sale
    _create_item_and_sale()
    
    response = requests.get(f"{BASE_URL}/sales", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0

def test_fetch_specific_sale():
    sale_id = _create_item_and_sale()
    headers = get_auth_headers()
    
    response = requests.get(f"{BASE_URL}/sales/{sale_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["id"] == sale_id
