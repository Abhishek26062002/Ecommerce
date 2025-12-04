from pydantic import BaseModel
from typing import List
from app.schemas.cartitem import CartItemSchema


class AddItemsSchema(BaseModel):
    user_id: str
    items: List[CartItemSchema]