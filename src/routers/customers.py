from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from uuid import UUID

from src.database.connection import get_db
from src.models.customer import Customer
from src.schemas.customer import CustomerCreate, CustomerResponse

router = APIRouter(
    prefix="/customers",
    tags=["Customers"]
)

@router.post("/", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
async def create_customer(customer_in: CustomerCreate, db: AsyncSession = Depends(get_db)):
    # Check for unique email
    query_email = select(Customer).where(Customer.email == customer_in.email)
    if (await db.execute(query_email)).scalars().first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered.")

    # Check for unique phone number
    query_phone = select(Customer).where(Customer.phone_number == customer_in.phone_number)
    if (await db.execute(query_phone)).scalars().first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Phone number already registered.")

    new_customer = Customer(**customer_in.model_dump())
    db.add(new_customer)
    await db.commit()
    await db.refresh(new_customer)

    return new_customer

@router.get("/", response_model=List[CustomerResponse])
async def get_all_customers(db: AsyncSession = Depends(get_db)):
    query = select(Customer)
    result = await db.execute(query)
    return result.scalars().all()

@router.get("/{id}", response_model=CustomerResponse)
async def get_customer_by_id(id: UUID, db: AsyncSession = Depends(get_db)):
    query = select(Customer).where(Customer.id == id)
    customer = (await db.execute(query)).scalars().first()

    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found.")
    return customer