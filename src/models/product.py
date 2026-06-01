from sqlalchemy import Column, String, Integer, Numeric, DateTime, func, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
import uuid
from src.database.connection import Base

class Product(Base):
    __tablename__ = "products"

    # Equivalent to @Id and @GeneratedValue(strategy = GenerationType.UUID)
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Equivalent to @Column(nullable = false)
    name = Column(String, nullable=False, index=True)

    # Equivalent to @Column(unique = true, nullable = false)
    sku = Column(String, unique=True, nullable=False, index=True)

    # We use Numeric (Decimal) for prices to avoid floating-point arithmetic errors
    price = Column(Numeric(10, 2), nullable=False)

    # Stock quantity
    stock = Column(Integer, nullable=False, default=0)

    # Auditing fields (Equivalent to @CreatedDate / @LastModifiedDate)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Database-level validation: Ensure stock never goes negative
    __table_args__ = (
        CheckConstraint('stock >= 0', name='check_stock_non_negative'),
    )