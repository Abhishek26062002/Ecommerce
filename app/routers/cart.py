from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.models.cart import Cart
from app.models.Cartitem import CartItem
from sqlalchemy.future import select
from app.models.users import User
from app.models.product import Product
from app.schemas.cart import AddItemsSchema
from typing import List

router = APIRouter(prefix="/cart", tags=["cart"])   



@router.get("/")
async def get_carts(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Cart))
    carts = result.scalars().all()
    return carts


@router.post("/create_cart", status_code=status.HTTP_201_CREATED)
async def create_cart(user_id: int, db: AsyncSession = Depends(get_db)):
    new_cart = Cart(user_id=user_id)
    user = await db.execute(select(User).where(User.id == user_id))
    user_instance = user.scalars().first()
    if not user_instance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user_instance.cart_id = new_cart.id
    db.add(new_cart)
    await db.commit()
    await db.refresh(new_cart)
    return new_cart


@router.delete("/delete_cart/{cart_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_cart(cart_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Cart).where(Cart.id == cart_id))
    cart = result.scalars().first()
    if not cart:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found")
    await db.delete(cart)
    await db.commit()


@router.get("/{cart_id}/items")
async def get_cart_items(cart_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(CartItem).where(CartItem.cart_id == cart_id))
    items = result.scalars().all()
    return items


@router.get("get_cart_by_user/{user_id}")
async def get_cart_by_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Cart).where(Cart.user_id == user_id))
    cart = result.scalars().first()
    if not cart:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found for the user")
    return cart


@router.post("/{user_id}/add_items", status_code=status.HTTP_201_CREATED)
async def add_items_to_cart(req : AddItemsSchema, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Cart).where(Cart.user_id == req.user_id))
    cart = result.scalars().first()
    
    if not cart:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found for the user")
    
    for item in req.items:
        product = await db.execute(select(Product).where(Product.id == item.product_id))
        product_instance = product.scalars().first()
        if not product_instance:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with ID {item.product_id} not found")
        unit_price = product_instance.price
        total_price = unit_price * 1
        cart_item = CartItem(
            cart_id=cart.user_id,
            product_id=item.product_id,
            machine_type=item.selected_format,
            quantity=1,
            unit_price=item.unit_price,
            total_price=total_price
        )
        
        db.add(cart_item)
    await db.commit()
    return {"message": "Items added to cart successfully"}


@router.delete("/remove_item/{item_id}")
async def remove_item_from_cart(item_id: str, db: AsyncSession = Depends(get_db)):
    print("Removing item with ID:", item_id)
    result = await db.execute(select(CartItem).where(CartItem.product_id == item_id))
    item = result.scalars().first()
    print(item)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart item not found")
    await db.delete(item)
    print(f"Item {item_id} deleted")
    await db.commit()



@router.get("/items/{user_id}")
async def get_all_products_from_cart(user_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(CartItem).where(CartItem.cart_id == user_id))
    items = result.scalars().all()
    data = []
    for item in items:
        product = await db.execute(select(Product).where(Product.id == item.product_id))
        product = product.scalars().first()
        data.append({
            "product_id": str(product.id),
            "item_id": item.id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "images_urls": product.images_urls,
            "selected_format": item.machine_type,
            "quantity": item.quantity,
            "unit_price": item.unit_price,
            "total_price": item.total_price,
            "machine_type": product.machine_type
        })
    print("data:", data)
    return data


@router.put("/update_item/{item_id}")
async def update_cart_item(item_id: str, quantity: int = None, machine_type : str = None, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(CartItem).where(CartItem.product_id == item_id))
    item = result.scalars().first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart item not found")
    if quantity is not None:
        item.quantity = quantity
    item.total_price = item.unit_price * item.quantity
    if machine_type is not None:
        item.machine_type = machine_type
    await db.commit()
    await db.refresh(item)
    return item

    