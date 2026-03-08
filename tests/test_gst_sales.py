import requests
from tests.utils import BASE_URL, get_auth_headers


def test_gst_sales_flow():
    headers = get_auth_headers()

    # ── Step 1: Create an item with GST ──────────────────────────────────────
    item_payload = {
        "name": "GST Test Chair",
        "category": "Furniture",
        "price": 1000.0,
        "stock_quantity": 10,
        "hsn_code": "9403",
        "gst_percent": 18.0
    }
    item_response = requests.post(f"{BASE_URL}/items/", json=item_payload, headers=headers)
    assert item_response.status_code in (200, 201), (
        f"Expected 200/201 creating item, got {item_response.status_code}: {item_response.text}"
    )

    item = item_response.json()
    assert "id" in item, "Response missing 'id'"
    assert item.get("hsn_code") == "9403", f"Expected hsn_code='9403', got {item.get('hsn_code')}"
    assert item.get("gst_percent") == 18.0, f"Expected gst_percent=18.0, got {item.get('gst_percent')}"

    item_id = item["id"]
    initial_stock = item["stock_quantity"]  # 10

    # ── Step 2: Create a sale with the GST-enabled item ───────────────────────
    sale_payload = {
        "items": [
            {
                "item_id": item_id,
                "quantity": 2
            }
        ]
    }
    sale_response = requests.post(f"{BASE_URL}/sales/", json=sale_payload, headers=headers)
    assert sale_response.status_code in (200, 201), (
        f"Expected 200/201 creating sale, got {sale_response.status_code}: {sale_response.text}"
    )

    sale = sale_response.json()

    # ── Step 3: Validate GST calculations ─────────────────────────────────────
    # base_price = 1000 × 2 = 2000
    # gst_amount = 2000 × 0.18 = 360
    # cgst = 180, sgst = 180
    # total_price = 2360

    assert "items" in sale, "Sale response missing 'items'"
    assert len(sale["items"]) == 1, "Expected exactly one sale item"

    sale_item = sale["items"][0]

    assert sale_item.get("cgst_amount") == 180.0, (
        f"Expected cgst_amount=180.0, got {sale_item.get('cgst_amount')}"
    )
    assert sale_item.get("sgst_amount") == 180.0, (
        f"Expected sgst_amount=180.0, got {sale_item.get('sgst_amount')}"
    )
    assert sale_item.get("total_price") == 2360.0, (
        f"Expected total_price=2360.0, got {sale_item.get('total_price')}"
    )

    # The overall sale total_amount must include GST
    assert sale.get("total_amount") == 2360.0, (
        f"Expected sale total_amount=2360.0, got {sale.get('total_amount')}"
    )

    # ── Step 4: Verify inventory was reduced ──────────────────────────────────
    stock_response = requests.get(f"{BASE_URL}/items/{item_id}", headers=headers)
    assert stock_response.status_code == 200

    updated_stock = stock_response.json()["stock_quantity"]
    assert updated_stock == initial_stock - 2, (
        f"Expected stock={initial_stock - 2}, got {updated_stock}"
    )


def test_gst_stored_on_item():
    """Verify that hsn_code and gst_percent are persisted correctly."""
    headers = get_auth_headers()

    item_payload = {
        "name": "HSN Verify Item",
        "category": "Test",
        "price": 500.0,
        "stock_quantity": 5,
        "hsn_code": "4407",
        "gst_percent": 12.0
    }
    create_resp = requests.post(f"{BASE_URL}/items/", json=item_payload, headers=headers)
    assert create_resp.status_code in (200, 201)

    item_id = create_resp.json()["id"]

    # Fetch item and confirm GST fields are stored
    fetch_resp = requests.get(f"{BASE_URL}/items/{item_id}", headers=headers)
    assert fetch_resp.status_code == 200

    fetched = fetch_resp.json()
    assert fetched.get("hsn_code") == "4407", f"hsn_code mismatch: {fetched.get('hsn_code')}"
    assert fetched.get("gst_percent") == 12.0, f"gst_percent mismatch: {fetched.get('gst_percent')}"


def test_gst_zero_percent():
    """Items with 0% GST should produce zero tax and no inflated total."""
    headers = get_auth_headers()

    item_payload = {
        "name": "Zero GST Item",
        "category": "Exempt",
        "price": 200.0,
        "stock_quantity": 5,
        "hsn_code": "0000",
        "gst_percent": 0.0
    }
    item_resp = requests.post(f"{BASE_URL}/items/", json=item_payload, headers=headers)
    assert item_resp.status_code in (200, 201)
    item_id = item_resp.json()["id"]

    sale_payload = {"items": [{"item_id": item_id, "quantity": 1}]}
    sale_resp = requests.post(f"{BASE_URL}/sales/", json=sale_payload, headers=headers)
    assert sale_resp.status_code in (200, 201)

    sale = sale_resp.json()
    sale_item = sale["items"][0]

    assert sale_item.get("cgst_amount") == 0.0, f"Expected cgst=0, got {sale_item.get('cgst_amount')}"
    assert sale_item.get("sgst_amount") == 0.0, f"Expected sgst=0, got {sale_item.get('sgst_amount')}"
    assert sale_item.get("total_price") == 200.0, f"Expected total=200.0, got {sale_item.get('total_price')}"
    assert sale.get("total_amount") == 200.0, f"Expected sale total=200.0, got {sale.get('total_amount')}"
