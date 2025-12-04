from app.core.database import get_db
from app.models.cart import Cart
from app.models.Cartitem import CartItem
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.users import User
from app.models.wishlist import Wishlist




async def create_cart_for_user(user_id: int, db: AsyncSession):
    new_cart = Cart(user_id=user_id)
    db.add(new_cart)
    await db.commit()
    await db.refresh(new_cart)
    return new_cart

async def create_wishlist_for_user(user_id: int, db: AsyncSession):
    new_wishlist = Wishlist(user_id=user_id)
    db.add(new_wishlist)
    await db.commit()
    await db.refresh(new_wishlist)
    return new_wishlist