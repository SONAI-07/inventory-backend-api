from sqlalchemy import Column, String, Integer, Numeric, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from src.database.connection import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # @ManyToOne equivalent: Linking Order to Customer
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=False, index=True)

    # Order metadata
    status = Column(String, default="PENDING", nullable=False) # e.g., PENDING, COMPLETED, CANCELLED
    total_amount = Column(Numeric(10, 2), nullable=False, default=0.00)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # ORM Relationship (@OneToMany equivalent).
    # cascade="all, delete-orphan" acts like cascade = CascadeType.ALL
    customer = relationship("Customer", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Foreign Keys linking to the Order and the Product
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id"), nullable=False, index=True)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), nullable=False, index=True)

    quantity = Column(Integer, nullable=False)

    # We store unit_price here to lock in the price at the time of purchase.
    # If the product price changes tomorrow, historical orders shouldn't be affected.
    unit_price = Column(Numeric(10, 2), nullable=False)

    # ORM Relationships (@ManyToOne equivalents)
    order = relationship("Order", back_populates="items")
    product = relationship("Product") # Unidirectional relationship is fine here