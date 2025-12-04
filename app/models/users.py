from app.core.database import Base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy import Uuid


class User(Base):
    __tablename__ = "users"

    id = Column(String, unique=True, index=True)
    email = Column(String, primary_key=True, index=True, nullable=False)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    mobile_number = Column(Integer, nullable=True)
    customer_id = Column(String, nullable=True)