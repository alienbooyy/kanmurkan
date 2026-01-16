# API Documentation

## Base URL
```
http://localhost:8000/api
```

## Authentication

### Login
**Endpoint:** `POST /auth/login`

**Request Body:**
```json
{
  "username": "admin",
  "password": "admin123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Note:** Include the token in subsequent requests:
```
Authorization: Bearer <access_token>
```

---

## Tables

### Get All Tables
**Endpoint:** `GET /tables`

**Response:**
```json
[
  {
    "id": 1,
    "table_number": 1,
    "is_occupied": false
  }
]
```

### Create Table
**Endpoint:** `POST /tables`

**Request Body:**
```json
{
  "table_number": 5
}
```

### Update Table
**Endpoint:** `PUT /tables/{table_id}`

### Delete Table
**Endpoint:** `DELETE /tables/{table_id}`

---

## Products

### Get All Products
**Endpoint:** `GET /products`

**Response:**
```json
[
  {
    "id": 1,
    "name": "Lahmacun",
    "price": 15.0
  }
]
```

### Create Product
**Endpoint:** `POST /products`

**Request Body:**
```json
{
  "name": "Pizza",
  "price": 45.0
}
```

### Update Product
**Endpoint:** `PUT /products/{product_id}`

### Delete Product
**Endpoint:** `DELETE /products/{product_id}`

---

## Orders

### Get Active Order for Table
**Endpoint:** `GET /orders/table/{table_id}`

**Response:**
```json
{
  "id": 1,
  "table_id": 1,
  "created_at": "2024-01-16T10:00:00",
  "closed_at": null,
  "is_active": true,
  "total_amount": 60.0,
  "order_items": [
    {
      "id": 1,
      "order_id": 1,
      "product_id": 1,
      "quantity": 2,
      "unit_price": 15.0,
      "is_paid": false
    }
  ]
}
```

### Create Order
**Endpoint:** `POST /orders`

**Request Body:**
```json
{
  "table_id": 1
}
```

### Add Item to Order
**Endpoint:** `POST /orders/{order_id}/items`

**Request Body:**
```json
{
  "product_id": 1,
  "quantity": 2
}
```

### Remove Item from Order
**Endpoint:** `DELETE /orders/{order_id}/items/{item_id}`

### Close Order
**Endpoint:** `POST /orders/{order_id}/close`

### Process Payment
**Endpoint:** `POST /orders/{order_id}/payment`

**Response:**
```json
{
  "message": "Payment received",
  "total": 60.0
}
```

### Split Payment
**Endpoint:** `POST /orders/{order_id}/split-payment`

**Request Body:**
```json
{
  "order_id": 1,
  "item_ids": [1, 2]
}
```

**Response:**
```json
{
  "message": "Split payment processed",
  "paid_amount": 30.0
}
```

---

## Raw Materials

### Get All Raw Materials
**Endpoint:** `GET /raw-materials`

### Create Raw Material
**Endpoint:** `POST /raw-materials`

**Request Body:**
```json
{
  "name": "Meat",
  "unit": "g",
  "stock_quantity": 5000.0
}
```

### Update Raw Material
**Endpoint:** `PUT /raw-materials/{material_id}`

### Delete Raw Material
**Endpoint:** `DELETE /raw-materials/{material_id}`

---

## Recipes

### Get Product Recipe
**Endpoint:** `GET /products/{product_id}/recipe`

**Response:**
```json
[
  {
    "id": 1,
    "product_id": 1,
    "raw_material_id": 1,
    "quantity": 20.0
  }
]
```

### Add Recipe Item
**Endpoint:** `POST /products/{product_id}/recipe`

**Request Body:**
```json
{
  "raw_material_id": 1,
  "quantity": 20.0
}
```

### Delete Recipe Item
**Endpoint:** `DELETE /products/{product_id}/recipe/{recipe_item_id}`

---

## Reports

### End of Day Report
**Endpoint:** `GET /reports/end-of-day`

**Query Parameters:**
- `start_date` (optional): ISO format date (e.g., "2024-01-01T00:00:00")
- `end_date` (optional): ISO format date

**Response:**
```json
{
  "total_revenue": 1250.0,
  "total_orders": 45,
  "product_sales": {
    "Lahmacun": {
      "quantity": 30,
      "revenue": 450.0
    },
    "Pizza": {
      "quantity": 10,
      "revenue": 450.0
    }
  }
}
```

### Most Sold Items
**Endpoint:** `GET /reports/most-sold`

**Response:**
```json
{
  "most_sold": [
    ["Lahmacun", {"quantity": 30, "revenue": 450.0}],
    ["Pizza", {"quantity": 10, "revenue": 450.0}]
  ],
  "least_sold": [
    ["Tea", {"quantity": 2, "revenue": 6.0}]
  ]
}
```

### Export to Excel
**Endpoint:** `GET /reports/export-excel`

**Query Parameters:**
- `start_date` (optional): ISO format date
- `end_date` (optional): ISO format date

**Response:** Excel file download

---

## Printing

### Print Order
**Endpoint:** `GET /print/order/{order_id}`

**Query Parameters:**
- `printer_type`: "kitchen" or "oven"

**Response:**
```json
{
  "message": "Order sent to kitchen printer",
  "receipt": "Table: 5\nOrder ID: 1\n..."
}
```

---

## Error Responses

All endpoints may return error responses:

**400 Bad Request:**
```json
{
  "detail": "Invalid input data"
}
```

**401 Unauthorized:**
```json
{
  "detail": "Incorrect username or password"
}
```

**404 Not Found:**
```json
{
  "detail": "Resource not found"
}
```

**500 Internal Server Error:**
```json
{
  "detail": "Internal server error"
}
```

---

## Interactive API Documentation

Visit `http://localhost:8000/docs` for interactive Swagger UI documentation where you can test all endpoints directly.
