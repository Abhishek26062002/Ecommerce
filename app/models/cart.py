from sqlalchemy import Column, Integer, ForeignKey, DateTime, func, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import text
from app.core.database import Base 
from sqlalchemy import Uuid# your SQLAlchemy Base


class Cart(Base):
    __tablename__ = "carts"

    user_id = Column(String, primary_key=True, unique=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    cart_items = relationship("CartItem", back_populates="cart")

