from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class TableBase(BaseModel):
    table_number: int


class TableCreate(TableBase):
    pass


class TableResponse(TableBase):
    id: int
    is_occupied: bool
    
    class Config:
        from_attributes = True


class ProductBase(BaseModel):
    name: str
    price: float


class ProductCreate(ProductBase):
    pass


class ProductResponse(ProductBase):
    id: int
    
    class Config:
        from_attributes = True


class RawMaterialBase(BaseModel):
    name: str
    unit: str
    stock_quantity: float = 0.0


class RawMaterialCreate(RawMaterialBase):
    pass


class RawMaterialResponse(RawMaterialBase):
    id: int
    
    class Config:
        from_attributes = True


class RecipeItemBase(BaseModel):
    raw_material_id: int
    quantity: float


class RecipeItemCreate(RecipeItemBase):
    pass


class RecipeItemResponse(RecipeItemBase):
    id: int
    product_id: int
    
    class Config:
        from_attributes = True


class OrderItemBase(BaseModel):
    product_id: int
    quantity: int


class OrderItemCreate(OrderItemBase):
    pass


class OrderItemResponse(OrderItemBase):
    id: int
    order_id: int
    unit_price: float
    is_paid: bool
    
    class Config:
        from_attributes = True


class OrderBase(BaseModel):
    table_id: int


class OrderCreate(OrderBase):
    pass


class OrderResponse(OrderBase):
    id: int
    created_at: datetime
    closed_at: Optional[datetime]
    is_active: bool
    total_amount: float
    order_items: List[OrderItemResponse] = []
    
    class Config:
        from_attributes = True


class AdminLogin(BaseModel):
    username: str
    password: str


class AdminCreate(AdminLogin):
    pass


class Token(BaseModel):
    access_token: str
    token_type: str


class SplitPaymentRequest(BaseModel):
    order_id: int
    item_ids: List[int]
