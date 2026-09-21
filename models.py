from sqlalchemy import Column, Integer, String, Float, Date, Time, ForeignKey
from database import Base
from sqlalchemy.orm import relationship

""" 
Los productos deberán contar con los siguientes datos: 
● id (int pk autoincrement not null) 
● nombre (str not null) 
● precio (float not null) """

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)

    sales = relationship("Sale", back_populates="product")

"""
Las ventas deberán contar con los siguientes datos:
● id (int pk autoincrement not null)
● fecha (date not null)
● hora (time not null)
● id_producto (fk int not null)
● cantidad (int not null)
● precio_total (float not null) """

class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    total_price = Column(Float, nullable=False)

    product = relationship("Product", back_populates="sales")

    

