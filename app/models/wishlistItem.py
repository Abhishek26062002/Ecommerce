from sqlalchemy import Column, Integer, ForeignKey, Float, String
from sqlalchemy.orm import relationship
from app.core.database import Base
from sqlalchemy.dialects.postgresql import UUID


class WishlistItem(Base):
    __tablename__ = "wishlist_items"

    id = Column(Integer, primary_key=True, index=True)
    wishlist_id = Column(String, ForeignKey("wishlists.user_id", ondelete="CASCADE"))
    product_id = Column(UUID, ForeignKey("products.id", ondelete="SET NULL"))

    note = Column(String, nullable=True)  # Optional note from user  

    wishlist = relationship("Wishlist", back_populates="items")
    product = relationship("Product")
