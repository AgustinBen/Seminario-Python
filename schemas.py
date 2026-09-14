from pydantic import BaseModel

class ProductCreate(BaseModel):
    name: str
    price: float


class ProductResponse(BaseModel):
    id: int
    name: str
    price: float

    class Config:
        from_attributes = True   # Es un permiso para que Pydantic pueda leer el objeto (en versiones viejas de Pydantic se llama orm_mode = True)


