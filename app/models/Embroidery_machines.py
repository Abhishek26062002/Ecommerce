from app.core.database import Base
from sqlalchemy import Column, String, Text, Boolean, Integer, Float, ARRAY
from sqlalchemy.sql.sqltypes import DateTime
from datetime import datetime


class EmbroideryMachine(Base):
    __tablename__ = "embroidery_machines"

    machine_id = Column(String, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    brand = Column(String(100), nullable=True)
    model = Column(String(100), nullable=True)
    machine_type = Column(String(100), nullable=True)
    images_urls = Column(ARRAY(String), nullable=True)
    needle_count = Column(Integer, nullable=True)
    head_count = Column(Integer, nullable=True)
    max_embroidery_area = Column(String(50), nullable=True)
    max_spm = Column(Integer, nullable=True)
    file_formats = Column(ARRAY(String), nullable=True)
    auto_thread_trimmer = Column(Boolean, default=False, nullable=False)
    auto_color_change = Column(Boolean, default=False, nullable=False)
    thread_break_detection = Column(Boolean, default=False, nullable=False)
    usb = Column(Boolean, default=False, nullable=False)
    wifi = Column(Boolean, default=False, nullable=False)
    price = Column(Float, nullable=False)
    discount_price = Column(Float, nullable=True)
    stock_count = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False)