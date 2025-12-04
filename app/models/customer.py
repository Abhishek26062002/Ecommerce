from app.core.database import Base
from sqlalchemy import Column, Integer, String

class Customer(Base):
    __tablename__ = "customers"
    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
