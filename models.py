from sqlalchemy import Column, Integer, String, Float, Date, Time, ForeignKey, UniqueConstraint
from database import Base
from sqlalchemy.orm import relationship

class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)

    cart_product = relationship("CartProduct", back_populates="product")

class Cart(Base):
    __tablename__ = "cart"

    id = Column(Integer, primary_key=True, autoincrement=True)
    creation_dale = Column(Date, nullable=False)
    status = Column(String(20), nullable=False)

    items = relationship("CartProduct", back_populates="cart", cascade="all, delete-orphan")
    sales = relationship("Sale", back_populates="cart")

class CartProduct(Base):
    __tablename__ = "cart_product"
    __table_args__ = (UniqueConstraint("cart_id", "product_id", name="uq_cart_product"),)

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    cart_id = Column(Integer, ForeignKey("cart.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)
    quantity = Column(Integer, nullable=False)

    cart = relationship("Cart", back_populates="items")
    product = relationship("Product", back_populates="cart_product")

class Sale(Base):
    __tablename__ = "sale"

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)
    cart_id = Column(Integer, ForeignKey("cart.id"), unique=True, nullable=False)
    total_price = Column(Float, nullable=False)

    cart = relationship("Cart", back_populates="sales")

    

