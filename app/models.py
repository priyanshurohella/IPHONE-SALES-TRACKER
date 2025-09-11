from sqlalchemy import Column, Integer, String, DECIMAL, Date, TIMESTAMP, func
from .database import Base

class IPhoneSale(Base):
    __tablename__ = "iphone_sales"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String(100), nullable=False)
    phone_model = Column(String(50), nullable=False)
    color = Column(String(30), nullable=False)
    storage_gb = Column(Integer, nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    sale_date = Column(Date, nullable=False)
    store_location = Column(String(100), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
