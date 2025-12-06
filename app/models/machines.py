from app.core.database import Base
from sqlalchemy import Column, String, Text, Boolean, Integer
from sqlalchemy.sql.sqltypes import DateTime
from datetime import datetime


class Machine(Base):
    __tablename__ = "machines"

    machine_id = Column(String, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    brand = Column(String(100), nullable=True)
    machine_type = Column(String(100), nullable=True)
    price = Column(float, nullable=False)
    discount_price = Column(float, nullable=True)
    color = Column(String(50), nullable=True)
    size = Column(String(50), nullable=True)
    stock_count = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False)
    