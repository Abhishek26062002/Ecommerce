from pydantic import BaseModel

class customerDetails(BaseModel):
    name: str
    email: str
    phone: str

class PaymentLinkRequest(BaseModel):
    customer_details: customerDetails
    currency: str = "INR"