from app.core.database import Base
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Float
from datetime import datetime
from sqlalchemy.orm import relationship


 
class Order(Base):
    __tablename__ = "orders"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, nullable=False)

    total_amount = Column(Float, nullable=False)
    status = Column(
        String,
        default="PENDING"   # PENDING, PAID, FAILED, SHIPPED, COMPLETED, CANCELLED
    )

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.now(),
        onupdate=datetime.now()
    )
    payment_id = Column(String, nullable=True)

    # user = relationship("User", back_populates="orders")
    # items = relationship("OrderItem", back_populates="order", cascade="all, delete")
    
