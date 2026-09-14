from sqlalchemy import Column, Integer, String, Float
from database import Base

""" 
Los productos deberán contar con los siguientes datos: 
● id (int pk autoincrement not null) 
● nombre (str not null) 
● precio (float not null)  
"""

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)

    # sales = relationship("Sales", back_populates="product")






