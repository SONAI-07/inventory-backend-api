from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal
from uuid import UUID
from datetime import datetime
from typing import Optional # Add this import

class ProductBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, example="Wireless Mouse")
    sku: str = Field(..., min_length=3, max_length=20, example="WM-10293")
    price: Decimal = Field(..., gt=0, description="Price must be strictly positive")
    stock: int = Field(..., ge=0, description="Stock cannot be negative")

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: UUID
    created_at: datetime
    # Change 'datetime | None' to 'Optional[datetime]'
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)