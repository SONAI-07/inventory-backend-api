from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List
from uuid import UUID
from decimal import Decimal

from src.database.connection import get_db
from src.models.order import Order, OrderItem
from src.models.product import Product
from src.models.customer import Customer
from src.schemas.order import OrderCreate, OrderResponse

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)

@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(order_in: OrderCreate, db: AsyncSession = Depends(get_db)):
    # 1. Validate Customer Exists
    customer = await db.scalar(select(Customer).where(Customer.id == order_in.customer_id))
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found.")

    total_amount = Decimal("0.00")
    order_items_to_create = []

    # 2. Process each item in the order
    for item in order_in.items:
        # PESSIMISTIC LOCKING: Lock the product row so no other transaction can modify it
        query = select(Product).where(Product.id == item.product_id).with_for_update()
        product = (await db.execute(query)).scalars().first()

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with ID {item.product_id} not found."
            )

        # 3. Enforce Business Rule: Check Inventory
        if product.stock < item.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Insufficient stock for product '{product.name}'. Requested: {item.quantity}, Available: {product.stock}"
            )

        # 4. Enforce Business Rule: Reduce Stock
        product.stock -= item.quantity

        # 5. Enforce Business Rule: Calculate Total Amount backend-side
        unit_price = product.price
        total_amount += (unit_price * item.quantity)

        # Build the OrderItem entity
        order_items_to_create.append(
            OrderItem(
                product_id=product.id,
                quantity=item.quantity,
                unit_price=unit_price
            )
        )

    # 6. Create the Order entity
    new_order = Order(
        customer_id=order_in.customer_id,
        total_amount=total_amount,
        status="COMPLETED",
        items=order_items_to_create # SQLAlchemy automatically links the relationship
    )

    db.add(new_order)

    # 7. Commit the transaction. If anything above failed, FastAPI/SQLAlchemy rolls this back automatically.
    await db.commit()

    # Eagerly load the items to return in the response (Prevents LazyInitializationException equivalent)
    query_result = select(Order).options(selectinload(Order.items)).where(Order.id == new_order.id)
    final_order = (await db.execute(query_result)).scalars().first()

    return final_order


@router.get("/", response_model=List[OrderResponse])
async def get_all_orders(db: AsyncSession = Depends(get_db)):
    # selectinload fetches the @OneToMany relationships in a single optimized query
    query = select(Order).options(selectinload(Order.items))
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{id}", response_model=OrderResponse)
async def get_order_by_id(id: UUID, db: AsyncSession = Depends(get_db)):
    query = select(Order).options(selectinload(Order.items)).where(Order.id == id)
    order = (await db.execute(query)).scalars().first()

    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found.")
    return order


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(id: UUID, db: AsyncSession = Depends(get_db)):
    # Fetch the order and its items
    query = select(Order).options(selectinload(Order.items)).where(Order.id == id)
    order = (await db.execute(query)).scalars().first()

    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found.")

    # Business Rule: When an order is cancelled/deleted, we MUST restore the inventory stock.
    for item in order.items:
        product_query = select(Product).where(Product.id == item.product_id).with_for_update()
        product = (await db.execute(product_query)).scalars().first()
        if product:
            product.stock += item.quantity # Restore the stock

    # Delete the order (SQLAlchemy cascade delete will automatically remove the OrderItems)
    await db.delete(order)
    await db.commit()
    return None