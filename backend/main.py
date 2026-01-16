from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
import openpyxl
from openpyxl.styles import Font, Alignment
from io import BytesIO
from fastapi.responses import StreamingResponse
from passlib.context import CryptContext
from jose import JWTError, jwt

import models
import schemas
from database import engine, get_db

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Restaurant Automation System")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT configuration
SECRET_KEY = "your-secret-key-change-this-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Initialize default admin on startup
@app.on_event("startup")
def startup_event():
    db = next(get_db())
    admin = db.query(models.Admin).filter(models.Admin.username == "admin").first()
    if not admin:
        admin = models.Admin(
            username="admin",
            password_hash=get_password_hash("admin123")
        )
        db.add(admin)
        db.commit()
    db.close()


# Authentication endpoints
@app.post("/api/auth/login", response_model=schemas.Token)
def login(admin_login: schemas.AdminLogin, db: Session = Depends(get_db)):
    admin = db.query(models.Admin).filter(models.Admin.username == admin_login.username).first()
    if not admin or not verify_password(admin_login.password, admin.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    access_token = create_access_token(data={"sub": admin.username})
    return {"access_token": access_token, "token_type": "bearer"}


# Table endpoints
@app.get("/api/tables", response_model=List[schemas.TableResponse])
def get_tables(db: Session = Depends(get_db)):
    tables = db.query(models.Table).all()
    return tables


@app.post("/api/tables", response_model=schemas.TableResponse)
def create_table(table: schemas.TableCreate, db: Session = Depends(get_db)):
    db_table = models.Table(table_number=table.table_number)
    db.add(db_table)
    db.commit()
    db.refresh(db_table)
    return db_table


@app.put("/api/tables/{table_id}", response_model=schemas.TableResponse)
def update_table(table_id: int, table: schemas.TableCreate, db: Session = Depends(get_db)):
    db_table = db.query(models.Table).filter(models.Table.id == table_id).first()
    if not db_table:
        raise HTTPException(status_code=404, detail="Table not found")
    db_table.table_number = table.table_number
    db.commit()
    db.refresh(db_table)
    return db_table


@app.delete("/api/tables/{table_id}")
def delete_table(table_id: int, db: Session = Depends(get_db)):
    db_table = db.query(models.Table).filter(models.Table.id == table_id).first()
    if not db_table:
        raise HTTPException(status_code=404, detail="Table not found")
    db.delete(db_table)
    db.commit()
    return {"message": "Table deleted"}


# Product endpoints
@app.get("/api/products", response_model=List[schemas.ProductResponse])
def get_products(db: Session = Depends(get_db)):
    products = db.query(models.Product).all()
    return products


@app.post("/api/products", response_model=schemas.ProductResponse)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    db_product = models.Product(name=product.name, price=product.price)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@app.put("/api/products/{product_id}", response_model=schemas.ProductResponse)
def update_product(product_id: int, product: schemas.ProductCreate, db: Session = Depends(get_db)):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    db_product.name = product.name
    db_product.price = product.price
    db.commit()
    db.refresh(db_product)
    return db_product


@app.delete("/api/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(db_product)
    db.commit()
    return {"message": "Product deleted"}


# Raw Material endpoints
@app.get("/api/raw-materials", response_model=List[schemas.RawMaterialResponse])
def get_raw_materials(db: Session = Depends(get_db)):
    materials = db.query(models.RawMaterial).all()
    return materials


@app.post("/api/raw-materials", response_model=schemas.RawMaterialResponse)
def create_raw_material(material: schemas.RawMaterialCreate, db: Session = Depends(get_db)):
    db_material = models.RawMaterial(
        name=material.name,
        unit=material.unit,
        stock_quantity=material.stock_quantity
    )
    db.add(db_material)
    db.commit()
    db.refresh(db_material)
    return db_material


@app.put("/api/raw-materials/{material_id}", response_model=schemas.RawMaterialResponse)
def update_raw_material(material_id: int, material: schemas.RawMaterialCreate, db: Session = Depends(get_db)):
    db_material = db.query(models.RawMaterial).filter(models.RawMaterial.id == material_id).first()
    if not db_material:
        raise HTTPException(status_code=404, detail="Raw material not found")
    db_material.name = material.name
    db_material.unit = material.unit
    db_material.stock_quantity = material.stock_quantity
    db.commit()
    db.refresh(db_material)
    return db_material


@app.delete("/api/raw-materials/{material_id}")
def delete_raw_material(material_id: int, db: Session = Depends(get_db)):
    db_material = db.query(models.RawMaterial).filter(models.RawMaterial.id == material_id).first()
    if not db_material:
        raise HTTPException(status_code=404, detail="Raw material not found")
    db.delete(db_material)
    db.commit()
    return {"message": "Raw material deleted"}


# Recipe endpoints
@app.get("/api/products/{product_id}/recipe", response_model=List[schemas.RecipeItemResponse])
def get_product_recipe(product_id: int, db: Session = Depends(get_db)):
    recipe_items = db.query(models.RecipeItem).filter(models.RecipeItem.product_id == product_id).all()
    return recipe_items


@app.post("/api/products/{product_id}/recipe", response_model=schemas.RecipeItemResponse)
def add_recipe_item(product_id: int, recipe_item: schemas.RecipeItemCreate, db: Session = Depends(get_db)):
    db_recipe_item = models.RecipeItem(
        product_id=product_id,
        raw_material_id=recipe_item.raw_material_id,
        quantity=recipe_item.quantity
    )
    db.add(db_recipe_item)
    db.commit()
    db.refresh(db_recipe_item)
    return db_recipe_item


@app.delete("/api/products/{product_id}/recipe/{recipe_item_id}")
def delete_recipe_item(product_id: int, recipe_item_id: int, db: Session = Depends(get_db)):
    db_recipe_item = db.query(models.RecipeItem).filter(
        models.RecipeItem.id == recipe_item_id,
        models.RecipeItem.product_id == product_id
    ).first()
    if not db_recipe_item:
        raise HTTPException(status_code=404, detail="Recipe item not found")
    db.delete(db_recipe_item)
    db.commit()
    return {"message": "Recipe item deleted"}


# Order endpoints
@app.get("/api/orders/table/{table_id}", response_model=Optional[schemas.OrderResponse])
def get_active_order(table_id: int, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(
        models.Order.table_id == table_id,
        models.Order.is_active == True
    ).first()
    return order


@app.post("/api/orders", response_model=schemas.OrderResponse)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    # Mark table as occupied
    table = db.query(models.Table).filter(models.Table.id == order.table_id).first()
    if not table:
        raise HTTPException(status_code=404, detail="Table not found")
    table.is_occupied = True
    
    db_order = models.Order(table_id=order.table_id)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


@app.post("/api/orders/{order_id}/items", response_model=schemas.OrderItemResponse)
def add_order_item(order_id: int, order_item: schemas.OrderItemCreate, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == order_item.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db_order_item = models.OrderItem(
        order_id=order_id,
        product_id=order_item.product_id,
        quantity=order_item.quantity,
        unit_price=product.price
    )
    db.add(db_order_item)
    
    # Update order total
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    order.total_amount += product.price * order_item.quantity
    
    db.commit()
    db.refresh(db_order_item)
    return db_order_item


@app.delete("/api/orders/{order_id}/items/{item_id}")
def remove_order_item(order_id: int, item_id: int, db: Session = Depends(get_db)):
    order_item = db.query(models.OrderItem).filter(
        models.OrderItem.id == item_id,
        models.OrderItem.order_id == order_id
    ).first()
    if not order_item:
        raise HTTPException(status_code=404, detail="Order item not found")
    
    # Update order total
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    order.total_amount -= order_item.unit_price * order_item.quantity
    
    db.delete(order_item)
    db.commit()
    return {"message": "Order item removed"}


@app.post("/api/orders/{order_id}/close")
def close_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    order.is_active = False
    order.closed_at = datetime.utcnow()
    
    # Mark table as vacant
    table = db.query(models.Table).filter(models.Table.id == order.table_id).first()
    table.is_occupied = False
    
    db.commit()
    return {"message": "Order closed"}


@app.post("/api/orders/{order_id}/payment")
def process_payment(order_id: int, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Mark all items as paid
    for item in order.order_items:
        item.is_paid = True
    
    order.is_active = False
    order.closed_at = datetime.utcnow()
    
    # Mark table as vacant
    table = db.query(models.Table).filter(models.Table.id == order.table_id).first()
    table.is_occupied = False
    
    db.commit()
    return {"message": "Payment received", "total": order.total_amount}


@app.post("/api/orders/{order_id}/split-payment")
def split_payment(order_id: int, split_request: schemas.SplitPaymentRequest, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Mark selected items as paid and remove from order
    paid_total = 0
    for item_id in split_request.item_ids:
        item = db.query(models.OrderItem).filter(
            models.OrderItem.id == item_id,
            models.OrderItem.order_id == order_id
        ).first()
        if item:
            paid_total += item.unit_price * item.quantity
            db.delete(item)
    
    order.total_amount -= paid_total
    
    # If no items left, close the order
    remaining_items = db.query(models.OrderItem).filter(models.OrderItem.order_id == order_id).count()
    if remaining_items == 0:
        order.is_active = False
        order.closed_at = datetime.utcnow()
        table = db.query(models.Table).filter(models.Table.id == order.table_id).first()
        table.is_occupied = False
    
    db.commit()
    return {"message": "Split payment processed", "paid_amount": paid_total}


# Reporting endpoints
@app.get("/api/reports/end-of-day")
def end_of_day_report(start_date: Optional[str] = None, end_date: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(models.Order).filter(models.Order.is_active == False)
    
    if start_date:
        start = datetime.fromisoformat(start_date)
        query = query.filter(models.Order.closed_at >= start)
    
    if end_date:
        end = datetime.fromisoformat(end_date)
        query = query.filter(models.Order.closed_at <= end)
    
    orders = query.all()
    total_revenue = sum(order.total_amount for order in orders)
    
    # Product sales breakdown
    product_sales = {}
    for order in orders:
        for item in order.order_items:
            product_name = item.product.name
            if product_name not in product_sales:
                product_sales[product_name] = {
                    "quantity": 0,
                    "revenue": 0
                }
            product_sales[product_name]["quantity"] += item.quantity
            product_sales[product_name]["revenue"] += item.unit_price * item.quantity
    
    return {
        "total_revenue": total_revenue,
        "total_orders": len(orders),
        "product_sales": product_sales
    }


@app.get("/api/reports/most-sold")
def most_sold_report(db: Session = Depends(get_db)):
    # Get all closed orders
    orders = db.query(models.Order).filter(models.Order.is_active == False).all()
    
    product_stats = {}
    for order in orders:
        for item in order.order_items:
            product_name = item.product.name
            if product_name not in product_stats:
                product_stats[product_name] = {
                    "quantity": 0,
                    "revenue": 0
                }
            product_stats[product_name]["quantity"] += item.quantity
            product_stats[product_name]["revenue"] += item.unit_price * item.quantity
    
    # Sort by quantity
    sorted_products = sorted(product_stats.items(), key=lambda x: x[1]["quantity"], reverse=True)
    
    return {
        "most_sold": sorted_products[:5] if len(sorted_products) > 5 else sorted_products,
        "least_sold": sorted_products[-5:] if len(sorted_products) > 5 else sorted_products
    }


@app.get("/api/reports/export-excel")
def export_excel(start_date: Optional[str] = None, end_date: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(models.Order).filter(models.Order.is_active == False)
    
    if start_date:
        start = datetime.fromisoformat(start_date)
        query = query.filter(models.Order.closed_at >= start)
    
    if end_date:
        end = datetime.fromisoformat(end_date)
        query = query.filter(models.Order.closed_at <= end)
    
    orders = query.all()
    
    # Create workbook
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Sales Report"
    
    # Headers
    headers = ["Order ID", "Table", "Date", "Total Amount", "Product", "Quantity", "Unit Price"]
    for col, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col, value=header)
        cell.font = Font(bold=True)
        cell.alignment = Alignment(horizontal="center")
    
    # Data
    row = 2
    for order in orders:
        for item in order.order_items:
            ws.cell(row=row, column=1, value=order.id)
            ws.cell(row=row, column=2, value=order.table.table_number)
            ws.cell(row=row, column=3, value=order.closed_at.strftime("%Y-%m-%d %H:%M:%S") if order.closed_at else "")
            ws.cell(row=row, column=4, value=order.total_amount)
            ws.cell(row=row, column=5, value=item.product.name)
            ws.cell(row=row, column=6, value=item.quantity)
            ws.cell(row=row, column=7, value=item.unit_price)
            row += 1
    
    # Save to BytesIO
    excel_file = BytesIO()
    wb.save(excel_file)
    excel_file.seek(0)
    
    return StreamingResponse(
        excel_file,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=sales_report.xlsx"}
    )


@app.get("/api/print/order/{order_id}")
def print_order(order_id: int, printer_type: str, db: Session = Depends(get_db)):
    """
    Print order to thermal printer
    printer_type: 'kitchen' or 'oven'
    """
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Generate receipt text
    receipt_text = f"Table: {order.table.table_number}\n"
    receipt_text += f"Order ID: {order.id}\n"
    receipt_text += f"Date: {order.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
    receipt_text += "-" * 32 + "\n"
    
    for item in order.order_items:
        receipt_text += f"{item.product.name}\n"
        receipt_text += f"  Qty: {item.quantity} x {item.unit_price:.2f}\n"
    
    receipt_text += "-" * 32 + "\n"
    receipt_text += f"Total: {order.total_amount:.2f}\n"
    
    # In a real implementation, this would send to the actual printer
    # For now, we'll return the receipt text
    return {
        "message": f"Order sent to {printer_type} printer",
        "receipt": receipt_text
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
