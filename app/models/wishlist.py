from sqlalchemy import Column, Integer, ForeignKey, DateTime, func, String
from sqlalchemy.orm import relationship
from app.core.database import Base
from sqlalchemy import Uuid


class Wishlist(Base):
    __tablename__ = "wishlists"

    
    user_id = Column(String, primary_key=True)
    

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    items = relationship(
        "WishlistItem",
        back_populates="wishlist",
        cascade="all, delete-orphan"
    )
