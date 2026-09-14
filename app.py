from fastapi import FastAPI, HTTPException, status, Depends
from database import Base, engine, get_db
from sqlalchemy.orm import Session
import models
from models import Product
import schemas 
from schemas import ProductCreate, ProductResponse

Base.metadata.create_all(bind=engine)
app = FastAPI()

""" ● POST /productos  
● GET /productos  
● GET /productos/{id} 
● PUT /productos/{id} 
● DELETE /productos/{id}  """

@app.get("/", tags=["Home"])
def hello_world():
    return {"message": "¡Hola, mundo!"}

@app.post("/products", status_code=status.HTTP_201_CREATED, response_model=ProductResponse)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    try:
        new_product = Product(name=product.name, price=product.price)
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        return new_product
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en POST /products: {e}")


@app.get("/products", status_code=status.HTTP_200_OK)
def get_products(db: Session = Depends(get_db)):
    try:
        products = db.query(Product).all()
        response = {"products" : products}
        return response
    
    except Exception as e:
        raise HTTPException(status_code=500, detail= f"Error en GET /products: {e}")
        

@app.get("/products/{id}", status_code=status.HTTP_200_OK)
def get_product(id: int, db: Session = Depends(get_db)):
    
    try:
        product = db.query(Product).filter(Product.id == id).first()
    
    except Exception as e:
        raise HTTPException(status_code=500, detail= f"Error en GET /products/{id}: {e}")

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    response = {"product" : product}
    return response

@app.put("/products/{id}", status_code=status.HTTP_200_OK, response_model=ProductResponse)
def update_product(id: int, product: ProductCreate, db: Session = Depends(get_db)):

    try:
        current_product = db.query(Product).filter(Product.id == id).first() # Buscamos el producto por id en la base
         
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en PUT /products/{id}: {e}")

    if not current_product:
        raise HTTPException(status_code=404, detail="Product not found") # Si no existe devolvemos 404

    current_product.name = product.name
    current_product.price = product.price
    db.commit()                     # Guardar los cambios
    db.refresh(current_product)     # Refrescamos
    return current_product          # devolvemos el producto actualizado

@app.delete("/products/{id}", status_code=status.HTTP_200_OK)
def delete_product(id: int, db: Session = Depends(get_db)):
    try:
        product = db.query(Product).filter(Product.id == id).first()

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en DELETE /products/{id}: {e}")

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db.delete(product)
    db.commit()
    return "Product successfully removed"
