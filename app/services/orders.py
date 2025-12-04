from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.orders import Order
from app.models.orderitems import OrderItem
from app.schemas.orders import OrderCreateSchema


async def create_order(payload: OrderCreateSchema, db: AsyncSession):
    try:
        new_order = Order(
            id=payload.order_id,
            user_id=payload.user_id,
            total_amount=sum(item.unit_price * item.qty for item in payload.items),
            status="pending"
        )
        db.add(new_order)
        await db.commit()
        await db.refresh(new_order)

        for item in payload.items:
            order_item = OrderItem(
                order_id=new_order.id,
                product_id=item.product_id,
                machine_type=item.machine_type,
                quantity=item.qty,
                price=item.unit_price
            )
            db.add(order_item)

        await db.commit()
        return {"order_id": new_order.id, "status": new_order.status}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))