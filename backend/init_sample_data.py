# Sample Data Initialization Script
# This file shows how to populate the database with sample data

import requests
import json

API_BASE = "http://localhost:8000/api"

# Login as admin
def login():
    response = requests.post(f"{API_BASE}/auth/login", json={
        "username": "admin",
        "password": "admin123"
    })
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

# Create sample tables
def create_tables(headers):
    for i in range(1, 11):
        requests.post(f"{API_BASE}/tables", json={"table_number": i}, headers=headers)
    print("Created 10 tables")

# Create sample products
def create_products(headers):
    products = [
        {"name": "Lahmacun", "price": 15.0},
        {"name": "Ayran", "price": 5.0},
        {"name": "Cola", "price": 7.0},
        {"name": "Pizza", "price": 45.0},
        {"name": "Salad", "price": 20.0},
        {"name": "Soup", "price": 12.0},
        {"name": "Kebab", "price": 35.0},
        {"name": "Coffee", "price": 10.0},
        {"name": "Tea", "price": 3.0},
        {"name": "Baklava", "price": 18.0}
    ]
    for product in products:
        requests.post(f"{API_BASE}/products", json=product, headers=headers)
    print(f"Created {len(products)} products")

# Create sample raw materials
def create_materials(headers):
    materials = [
        {"name": "Meat", "unit": "g", "stock_quantity": 5000},
        {"name": "Flour", "unit": "kg", "stock_quantity": 50},
        {"name": "Tomato", "unit": "kg", "stock_quantity": 20},
        {"name": "Onion", "unit": "kg", "stock_quantity": 15},
        {"name": "Yogurt", "unit": "L", "stock_quantity": 10},
        {"name": "Cheese", "unit": "kg", "stock_quantity": 8},
        {"name": "Olive Oil", "unit": "L", "stock_quantity": 5}
    ]
    for material in materials:
        requests.post(f"{API_BASE}/raw-materials", json=material, headers=headers)
    print(f"Created {len(materials)} raw materials")

if __name__ == "__main__":
    print("Initializing sample data...")
    headers = login()
    create_tables(headers)
    create_products(headers)
    create_materials(headers)
    print("Sample data initialization complete!")
