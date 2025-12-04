from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.models.wishlist import Wishlist
from app.models.wishlistItem import WishlistItem
from sqlalchemy.future import select
from typing import List
from app.models.users import User

router = APIRouter(prefix="/wishlist", tags=["wishlist"])



@router.get("/")
async def get_wishlists(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Wishlist))
    wishlists = result.scalars().all()
    return wishlists



@router.post("/create_wishlist", status_code=status.HTTP_201_CREATED)
async def create_wishlist(user_id: str, db: AsyncSession = Depends(get_db)):
    new_wishlist = Wishlist(user_id=user_id)
    user = await db.execute(select(User).where(User.id == user_id))
    user_instance = user.scalars().first()
    if not user_instance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user_instance.wishlist_id = new_wishlist.id
    db.add(new_wishlist)
    await db.commit()
    await db.refresh(new_wishlist)
    return new_wishlist


@router.delete("/delete_wishlist/{wishlist_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_wishlist(wishlist_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Wishlist).where(Wishlist.id == wishlist_id))
    wishlist = result.scalars().first()
    if not wishlist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Wishlist not found")
    await db.delete(wishlist)
    await db.commit()          
    
    
    
@router.get("/{wishlist_id}/items")
async def get_wishlist_items(wishlist_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(WishlistItem).where(WishlistItem.wishlist_id == wishlist_id))
    items = result.scalars().all()
    return items   

@router.post("/{wishlist_id}/add_item", status_code=status.HTTP_201_CREATED)
async def add_item_to_wishlist(wishlist_id: int, product_id: int, note: str = None, db: AsyncSession = Depends(get_db)):
    new_item = WishlistItem(wishlist_id=wishlist_id, product_id=product_id, note=note)
    db.add(new_item)
    await db.commit()
    await db.refresh(new_item)
    return new_item



@router.delete("/{wishlist_id}/remove_item/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_item_from_wishlist(wishlist_id: int, item_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(WishlistItem).where(WishlistItem.id == item_id, WishlistItem.wishlist_id == wishlist_id))
    item = result.scalars().first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found in the wishlist")
    await db.delete(item)
    await db.commit()