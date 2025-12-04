import razorpay
import os
from fastapi import HTTPException

razorpay_client = razorpay.Client(
    api_key=os.environ.get("RAZORPAY_API_KEY"),
    api_secret=os.environ.get("RAZORPAY_SECRET"),
)


async def create_customer(data : dict) :
    try :
        print(os.environ.get("RAZORPAY_API_KEY"))
        customer = razorpay_client.customer.create(data)
        print(customer)
        return customer
    except Exception as e :
        raise HTTPException(status_code=500, detail=str(e))

async def get_customer(customer_id : str) :
    try :
        customer = razorpay_client.customer.fetch(customer_id)
        return customer
    except Exception as e :
        raise HTTPException(status_code=500, detail=str(e))

async def get_customers() :
    try :
        customers = razorpay_client.customer.all()
        print(customers)
        return customers
    except Exception as e :
        raise HTTPException(status_code=500, detail=str(e))
