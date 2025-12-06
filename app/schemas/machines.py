from pydantic import BaseModel
from typing import Optional


class MachineSchema(BaseModel):
    machine_id: str
    name: str
    description: Optional[str] = None
    brand: Optional[str] = None
    machine_type: Optional[str] = None
    price: float
    discount_price: Optional[float] = None
    color: Optional[str] = None
    size: Optional[str] = None
    stock_count: Optional[int] = None

    class Config:
        orm_mode = True