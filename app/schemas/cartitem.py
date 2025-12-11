from pydantic import BaseModel
from typing import List



class CartItemSchema(BaseModel):
    product_id: str
    selected_format: str
    quantity: int
    unit_price: float