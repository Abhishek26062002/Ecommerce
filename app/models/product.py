from app.core.database import Base
from sqlalchemy import Column, String, Float, Text, Boolean, Integer, ARRAY
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.sql.sqltypes import DateTime
from datetime import datetime




class Product(Base):
    __tablename__ = "products"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    discount_price = Column(Float, nullable=True)
    in_stock = Column(Boolean, default=True)
    sub_category = Column(String(100), nullable=True)
    images_urls = Column(ARRAY(String), nullable=True)
    category = Column(String(100), nullable=True)
    brand = Column(String(100), nullable=True)
    machine_type = Column(String(100), nullable=True)
    color = Column(String(50), nullable=True)
    size = Column(String(50), nullable=True)
    # dst = Column(String(100), nullable=True)
    # jef = Column(String(100), nullable=True)
    stock_count = Column(Integer, nullable=True)
    date_created = Column(DateTime, default=datetime.now(), nullable=False)
    downloadable_files = Column(String, nullable=True)  
    