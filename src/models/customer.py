from pickle import LONG4

from sqlalchemy import Column, String, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
import uuid
from src.database.connection import Base
from sqlalchemy.orm import relationship

class Customer(Base):
    __tablename__ = "customers"

    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Customer Details
    name = Column(String, nullable=False, index=True)

    email = Column(String, unique=True, nullable=False, index=True)

    phone_number = Column(String(20), unique=True, nullable=False, index=True)

    # Auditing fields
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    orders = relationship("Order", back_populates="customer", cascade="all, delete-orphan")