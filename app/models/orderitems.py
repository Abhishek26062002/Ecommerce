from app.core.database import Base
from sqlalchemy import Column, String, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship



class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(String, primary_key=True)
    
    order_id = Column(String, nullable=False)  # No FK
    product_id = Column(String, nullable=False)  # No FK
    machine_type = Column(String, nullable=True)
    quantity = Column(Integer, default=1, nullable=False)
    price = Column(Float, nullable=False)






