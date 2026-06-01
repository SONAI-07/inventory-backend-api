from __future__ import annotations

from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from uuid import UUID
from datetime import datetime
from decimal import Decimal

# --- REQUEST DTOs (Incoming Data) ---

class OrderItemCreate(BaseModel):
    product_id: UUID
    quantity: int = Field(..., gt=0, description="Quantity must be at least 1")

class OrderCreate(BaseModel):
    customer_id: UUID
    items: List[OrderItemCreate] = Field(..., min_length=1, description="Order must contain at least one item")


# --- RESPONSE DTOs (Outgoing Data) ---

class OrderItemResponse(BaseModel):
    id: UUID
    product_id: UUID
    quantity: int
    unit_price: Decimal

    model_config = ConfigDict(from_attributes=True)

class OrderResponse(BaseModel):
    id: UUID
    customer_id: UUID
    status: str
    total_amount: Decimal
    items: List[OrderItemResponse]
    created_at: datetime
    # Change 'datetime | None' to 'Optional[datetime]'
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)