from pydantic import BaseModel  
from typing import List
from app.schemas.payment_integration import PaymentLinkRequest


class OrderItemSchema(BaseModel):
    product_id: str
    machine_type: str
    unit_price: float

class OrderCreateSchema(BaseModel):
    user_id: str
    payment_link_request: PaymentLinkRequest
    items: list[OrderItemSchema]