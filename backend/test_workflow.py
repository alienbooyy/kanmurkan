#!/usr/bin/env python3
"""Test basic workflow of the restaurant system"""

import requests
import json

BASE_URL = "http://localhost:8000/api"

def test_workflow():
    print("Testing Restaurant Automation System Workflow")
    print("=" * 50)
    
    # 1. Test login
    print("\n1. Testing Admin Login...")
    response = requests.post(f"{BASE_URL}/auth/login", json={
        "username": "admin",
        "password": "admin123"
    })
    assert response.status_code == 200
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("✓ Login successful")
    
    # 2. Get tables
    print("\n2. Getting tables...")
    response = requests.get(f"{BASE_URL}/tables")
    assert response.status_code == 200
    tables = response.json()
    print(f"✓ Found {len(tables)} tables")
    
    # 3. Get products
    print("\n3. Getting products...")
    response = requests.get(f"{BASE_URL}/products")
    assert response.status_code == 200
    products = response.json()
    print(f"✓ Found {len(products)} products")
    
    if not tables or not products:
        print("\n⚠ No tables or products found. Run init_sample_data.py first.")
        return
    
    # 4. Create an order
    print("\n4. Creating order for table 1...")
    response = requests.post(f"{BASE_URL}/orders", json={
        "table_id": tables[0]["id"]
    })
    assert response.status_code == 200
    order = response.json()
    print(f"✓ Order created with ID: {order['id']}")
    
    # 5. Add items to order
    print("\n5. Adding items to order...")
    for i in range(3):
        response = requests.post(
            f"{BASE_URL}/orders/{order['id']}/items",
            json={
                "product_id": products[i]["id"],
                "quantity": 2
            }
        )
        assert response.status_code == 200
        print(f"✓ Added {products[i]['name']} x2")
    
    # 6. Get order details
    print("\n6. Getting order details...")
    response = requests.get(f"{BASE_URL}/orders/table/{tables[0]['id']}")
    assert response.status_code == 200
    order_details = response.json()
    print(f"✓ Order total: {order_details['total_amount']:.2f} TL")
    print(f"✓ Items in order: {len(order_details['order_items'])}")
    
    # 7. Test reports
    print("\n7. Testing reports...")
    response = requests.get(f"{BASE_URL}/reports/most-sold")
    assert response.status_code == 200
    print("✓ Most sold report generated")
    
    # 8. Process payment
    print("\n8. Processing payment...")
    response = requests.post(f"{BASE_URL}/orders/{order['id']}/payment")
    assert response.status_code == 200
    print(f"✓ Payment processed: {response.json()['total']:.2f} TL")
    
    # 9. Verify table is now vacant
    print("\n9. Verifying table status...")
    response = requests.get(f"{BASE_URL}/tables")
    tables_after = response.json()
    table_1 = next(t for t in tables_after if t["id"] == tables[0]["id"])
    assert not table_1["is_occupied"]
    print("✓ Table is now vacant")
    
    print("\n" + "=" * 50)
    print("All tests passed! ✓")
    print("=" * 50)

if __name__ == "__main__":
    try:
        test_workflow()
    except Exception as e:
        print(f"\n✗ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        exit(1)
