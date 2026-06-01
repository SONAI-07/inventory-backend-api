from __future__ import annotations

from pydantic import BaseModel, Field, EmailStr, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional

# Base Schema (Equivalent to an abstract DTO class)
class CustomerBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=150, example="John Doe")

    # EmailStr automatically validates the string format (e.g., missing '@' or domain)
    email: EmailStr = Field(..., example="john.doe@example.com")

    phone_number: str = Field(
        ...,
        pattern=r'^\+?[1-9]\d{6,14}$',
        example="+919876543210",
        description="Must be a valid phone number, optionally starting with +"
    )

# Request DTO (For POST /customers)
class CustomerCreate(CustomerBase):
    pass

# Response DTO (For returning data to the React frontend)
class CustomerResponse(CustomerBase):
    id: UUID
    created_at: datetime
    # Change 'datetime | None' to 'Optional[datetime]'
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)