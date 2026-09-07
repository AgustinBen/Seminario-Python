from fastapi import FastAPI, HTTPException, status, Depends
from database import Base, engine, get_db
from sqlalchemy.orm import Session
import models
from models import Product

Base.metadata.create_all(bind=engine)
app = FastAPI()

@app.get("/", tags=["Home"])
def hello_world():
    return {"message": "¡Hola, mundo!"}


@app.get("/products", status_code=status.HTTP_200_OK)
def get_products(db: Session = Depends(get_db)):
    try:
        products = db.query(Product).all()
        response = {"products" : products}
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail= f"Error en /products: {e}")
        


@app.get("/products/{id}", status_code=status.HTTP_200_OK)
def get_product(id: int, db: Session = Depends(get_db)):

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    try:
        product = db.query(Product).filter(Product.id == id).first()

        response = {"product" : product}
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail= f"Error en /products/{id}: {e}")




""" ● POST /productos  
● GET /productos  
● GET /productos/{id} 
● PUT /productos/{id} 
● DELETE /productos/{id}  """