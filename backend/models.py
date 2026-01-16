from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class Table(Base):
    __tablename__ = "tables"
    
    id = Column(Integer, primary_key=True, index=True)
    table_number = Column(Integer, unique=True, nullable=False)
    is_occupied = Column(Boolean, default=False)
    orders = relationship("Order", back_populates="table")


class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    price = Column(Float, nullable=False)
    order_items = relationship("OrderItem", back_populates="product")
    recipe_items = relationship("RecipeItem", back_populates="product")


class RawMaterial(Base):
    __tablename__ = "raw_materials"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    unit = Column(String, nullable=False)  # e.g., "g", "kg", "L", "piece"
    stock_quantity = Column(Float, default=0.0)
    recipe_items = relationship("RecipeItem", back_populates="raw_material")


class RecipeItem(Base):
    __tablename__ = "recipe_items"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    raw_material_id = Column(Integer, ForeignKey("raw_materials.id"))
    quantity = Column(Float, nullable=False)
    
    product = relationship("Product", back_populates="recipe_items")
    raw_material = relationship("RawMaterial", back_populates="recipe_items")


class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    table_id = Column(Integer, ForeignKey("tables.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    closed_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    total_amount = Column(Float, default=0.0)
    
    table = relationship("Table", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order")


class OrderItem(Base):
    __tablename__ = "order_items"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, default=1)
    unit_price = Column(Float, nullable=False)
    is_paid = Column(Boolean, default=False)
    
    order = relationship("Order", back_populates="order_items")
    product = relationship("Product", back_populates="order_items")


class Admin(Base):
    __tablename__ = "admins"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
