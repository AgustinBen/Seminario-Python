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



# class CartResponse(BaseModel):
#     id: int 
#     creation_date: date
#     status: str
#     # items: list[CartItemResponse]

#     class Config:
#         from_attributes = True

# class SaleCreate(BaseModel):
#     date: date
#     time: time
#     product_id: int
#     quantity: int


# class SaleResponse(BaseModel):
#     id: int
#     date: date
#     time: time
#     cart: CartResponse
#     total_price: float

#     class Config:
#         from_attributes = True

