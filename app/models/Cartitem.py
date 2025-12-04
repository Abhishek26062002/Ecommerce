from sqlalchemy import Column, Integer, ForeignKey, Float, String
from sqlalchemy.orm import relationship
from app.core.database import Base
from sqlalchemy.dialects.postgresql import UUID

class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True, index=True)
    cart_id = Column(String, ForeignKey("carts.user_id", ondelete="CASCADE"))
    product_id = Column(UUID, ForeignKey("products.id", ondelete="SET NULL"))
    machine_type = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    unit_price = Column(Float, nullable=False)   # Price at the time added to cart
    total_price = Column(Float, nullable=False)  # unit_price * quantity


    cart = relationship("Cart", back_populates="cart_items")