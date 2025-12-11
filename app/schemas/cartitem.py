from pydantic import BaseModel
from typing import List



class CartItemSchema(BaseModel):
    product_id: str
    machine_type: List[str]
    quantity: int
    unit_price: float