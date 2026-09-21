from pydantic import BaseModel
from datetime import date, time

class ProductCreate(BaseModel):
    name: str
    price: float


class ProductResponse(BaseModel):
    id: int
    name: str
    price: float

    class Config:
        from_attributes = True   # Es un permiso para que Pydantic pueda leer el objeto (en versiones viejas de Pydantic se llama orm_mode = True)


class SaleCreate(BaseModel):
    date: date
    time: time
    product_id: int
    quantity: int


class SaleResponse(BaseModel):
    id: int
    date: date
    time: time
    quantity: int
    product: ProductResponse
    total_price: float

    class Config:
        from_attributes = True


