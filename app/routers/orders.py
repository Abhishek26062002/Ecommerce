from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.models.orders import Order
from app.models.orderitems import OrderItem
from app.models.product import Product
from app.schemas.orders import OrderCreateSchema
from app.services.payment_integration import create_payment_link
from fastapi.responses import RedirectResponse
import uuid
from sqlalchemy.future import select
router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/create-order")
async def create_order(payload: OrderCreateSchema, db: AsyncSession = Depends(get_db)):
    try:
        print("Creating order with payload:", payload)
        print(sum(item.unit_price for item in payload.items))
        order_id = f'order_{str(uuid.uuid4())}'
        new_order = Order(
            id=order_id,
            user_id=payload.user_id,
            total_amount=sum(item.unit_price for item in payload.items),
            status="pending"
        )
        db.add(new_order)
        await db.commit()
        await db.refresh(new_order)
        print("New order created with ID:", new_order.id)
        print("order items:", new_order)
        for item in payload.items:
            item_id = f'orderitem_{str(uuid.uuid4())}'
            order_item = OrderItem(
                id=item_id,
                order_id=new_order.id,
                product_id=item.product_id,
                machine_type=item.machine_type,
                quantity=1,
                price=item.unit_price
            )
            db.add(order_item)

        await db.commit()
        product_ids = [item.product_id for item in payload.items]
        amount = 0
        for product_id in product_ids:
            product_price = await db.execute(select(Product.discount_price).where(Product.id == product_id))
            product_price = product_price.fetchone()[0]
            amount += product_price
        payment_link = await create_payment_link(
            amount=new_order.total_amount,
            customer_details=payload.payment_link_request.customer_details.model_dump(),
            currency=payload.payment_link_request.currency
        )
        print("order_id:", type(new_order.id))
        new_order.payment_id = payment_link['payment_link_id']
        await db.commit()
        return {"order_id": new_order.id, "status": new_order.status, "payment_link": payment_link['redirect_url']}
    except Exception as e:
        print(f"Error creating order: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/get_orders/{user_id}")
async def get_orders(user_id: str, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(
            select(Order).where(Order.user_id == user_id, Order.status == "paid")
        )
        orders = result.scalars().all()
        order_items_result = await db.execute(
            select(OrderItem).where(OrderItem.order_id.in_([order.id for order in orders]))
        )
        order_items = order_items_result.scalars().all()
        orders_items_with_product_details = []
        detailed_items = []
        for order in orders:
            items = [item for item in order_items if item.order_id == order.id]
            
            for item in items:
                product_result = await db.execute(
                    select(Product).where(Product.id == item.product_id)
                )
                product = product_result.scalars().first()
                # detailed_items.append({
                #     "order_item": item,
                #     "product": product
                # })
                detailed_items.append({
                    "order_id": item.order_id,
                    "product_id": product.id,
                    "product_name": product.name,
                    "product_description": product.description,
                    "selected_type": item.machine_type,
                    "quantity": item.quantity,
                    "price": product.discount_price if product.discount_price else item.price,
                    "images": product.images_urls, 
                    "category": product.category,
                    "payment_id": order.payment_id
                })
            # orders_items_with_product_details.append({
            #     "order": order,
            #     "items": detailed_items
            # })

        return detailed_items
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/order_history/{user_id}")
async def order_history(user_id: str, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(
            select(Order).where(Order.user_id == user_id)
        )
        orders = result.scalars().all()
        return orders
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))