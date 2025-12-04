
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from app.services.payment_integration import create_payment_link
from app.schemas.payment_integration import PaymentLinkRequest
import json
from app.core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.orders import Order 
from sqlalchemy.future import select
from app.models.Cartitem import CartItem
from app.models.product import Product

router = APIRouter(prefix="/payment", tags=["payment"])


@router.post("/get_payment_link")
async def get_payment_link(req : PaymentLinkRequest, db: AsyncSession = Depends(get_db)):
    try:
        print("details",req)
        print(type(req.customer_details.model_dump_json()))
        print(req.customer_details.model_dump_json())
        products_ids = req.products
        
        amount = 0
        for product_id in products_ids:
            product_price = await db.execute(select(Product.discount_price).where(Product.id == product_id))
            product_price = product_price.fetchone()[0]
            amount += product_price
        print("Amount:", amount)
    
        payment_link = await create_payment_link(amount, json.loads(req.customer_details.model_dump_json()), req.currency)
        print(payment_link)
        return RedirectResponse(url=payment_link["redirect_url"], status_code=status.HTTP_302_FOUND)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))



@router.post('/razorpay-webhook')
async def razorpay_webhook(request: Request, db: AsyncSession = Depends(get_db)):
    event = await request.json()
    event_type = event.get("event")
    print("Razorpay Webhook Event Received:", event)
    if event_type == "payment_link.paid" or event_type == "payment.captured"   or event_type == "order.paid":
        payment_id = event["payload"]["payment"]["entity"]["notes"]["payment_link_id"]
        print("Payment ID:", payment_id)
        if payment_id:
            print("Fetching order for payment ID:", payment_id)
            order = await db.execute(select(Order).where(Order.payment_id == payment_id))
            order = order.scalars().first()
            print("Order fetched:", order)  
            print("Updating order status to 'paid' for order:", order.payment_id if order else "No order found")
            if order:
                order.status = "paid"
                cart_items_result = await db.execute(select(CartItem).where(CartItem.cart_id == order.user_id))
                cart_items = cart_items_result.scalars().all()
                for item in cart_items:
                    await db.delete(item)
                await db.commit()
                print(f"Order {payment_id} marked as paid.")
        print("✅ Payment success:", event["payload"]["payment"]["entity"]["id"])
    elif event_type == "payment.failed":
        payment_id = event["payload"]["payment"]['entity']["notes"]["payment_link_id"]
        if payment_id:
            order = await db.execute(select(Order).where(Order.payment_id == payment_id))
            order = order.scalars().first()
            if order:
                order.status = "failed"
                await db.commit()
                print(f"Order {payment_id} marked as failed.")
        print("❌ Payment failed:", event["payload"]["payment"]['entity']["notes"]["payment_link_id"])
    else:
        print("ℹ️ Other event (ignored):", event_type)
 
    return {"status": "ok"}