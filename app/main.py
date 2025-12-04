from fastapi import FastAPI, Depends, HTTPException, status
from app.core.database import init_models

from app.routers import google_login, admin, product, cart, wishlist, payment_integration, customer, admin_login, orders

from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="E-Commerce Application")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    
    await init_models()

app.include_router(google_login.router)
app.include_router(admin.router)
app.include_router(product.router)
app.include_router(cart.router)
app.include_router(wishlist.router)
app.include_router(payment_integration.router)
app.include_router(customer.router)
app.include_router(admin_login.router)
app.include_router(orders.router)