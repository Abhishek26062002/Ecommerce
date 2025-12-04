from sqlalchemy import Column, String
from app.core.database import Base




class Admin(Base) :
    __tablename__ = "admin_details"
    first_name = Column(String,nullable = False) 
    last_name = Column(String,nullable = False) 
    phone_number = Column(String,nullable = False) 
    email = Column(String,primary_key = True,unique=True,index = True) 
