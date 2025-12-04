from fastapi import APIRouter, HTTPException, Depends
from app.services.customer import create_customer
from app.schemas.customer import CustomerCreate
from app.core.database import get_db
from sqlalchemy.orm import Session
from app.services.customer import get_customer, get_customers

router = APIRouter()

@router.post("/customer")
async def create_customer_route(customer: CustomerCreate):
    try:
        return await create_customer(customer.model_dump())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/customer/{customer_id}")
async def get_customer_route(customer_id: str, db: Session = Depends(get_db)):
    try:
        return await get_customer(customer_id, db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/customers")
async def get_customers_route():
    try:
        return await get_customers()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))