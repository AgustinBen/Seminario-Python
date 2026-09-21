from fastapi import FastAPI, HTTPException, status, Depends
from database import Base, engine, get_db
from sqlalchemy.orm import Session
import models
from models import Product, Sale
import schemas 
from schemas import ProductCreate, ProductResponse, SaleResponse, SaleCreate

Base.metadata.create_all(bind=engine)
app = FastAPI()

# Endpoints de Producto

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
        

@app.get("/products/{id}", status_code=status.HTTP_200_OK, response_model=ProductResponse)
def get_product(id: int, db: Session = Depends(get_db)):
    
    try:
        product = db.query(Product).filter(Product.id == id).first()

    except Exception as e:
        raise HTTPException(status_code=500, detail= f"Error en GET /products/{id}: {e}")

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    return product


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

# Endpoints de Venta

@app.post("/sales", status_code=status.HTTP_201_CREATED, response_model=SaleResponse)
def post_sale(sale: SaleCreate, db: Session = Depends(get_db)):
    try:
        product = db.query(Product).filter(Product.id == sale.product_id).first()

    except Exception as e:
        raise HTTPException(status_code=500, detail= f"Error en producto id:{sale.product_id}: {e}")

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    total_price = product.price * sale.quantity
    new_sale = Sale(date=sale.date, time=sale.time, quantity=sale.quantity, product_id=sale.product_id, total_price=total_price)
    db.add(new_sale)
    db.commit()
    db.refresh(new_sale)
    return new_sale


@app.get("/sales", status_code=status.HTTP_200_OK)
def get_sales(db: Session = Depends(get_db)):
    try:
        sales = db.query(Sale).all()
        response = {"sales" : sales}
        return response
    
    except Exception as e:
            raise HTTPException(status_code=500, detail= f"Error en GET /products: {e}")


@app.get("/sales/{id}", status_code=status.HTTP_200_OK, response_model=SaleResponse)
def get_sale(id: int, db: Session = Depends(get_db)):
    try:
        sale = db.query(Sale).filter(Sale.id == id).first()

    except Exception as e:
        raise HTTPException(status_code=500, detail= f"Error en GET /sales/{id}: {e}")

    if not sale:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sale not found")

    return sale


@app.put("/sales/{id}", status_code=status.HTTP_200_OK, response_model=SaleResponse)
def update_sale(id: int, sale: SaleCreate, db: Session = Depends(get_db)):
    try:
        current_sale = db.query(Sale).filter(Sale.id == id).first()

    except Exception as e:
        raise HTTPException(status_code=500, detail= f"Error en GET /sales/{id}: {e}")

    if not current_sale:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sale not found")

    try:
        current_product = db.query(Product).filter(Product.id == sale.product_id).first()

    except Exception as e:
        raise HTTPException(status_code=500, detail= f"Error en GET /sales/{id}: {e}")

    if not current_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    current_sale.date = sale.date
    current_sale.time = sale.time
    current_sale.product_id = sale.product_id
    current_sale.quantity = sale.quantity
    current_sale.total_price = current_product.price * sale.quantity

    db.commit()
    db.refresh(current_sale)
    return current_sale


@app.delete("/sales/{id}", status_code=status.HTTP_200_OK)
def delete_sale(id: int, db: Session = Depends(get_db)):
    try:
        sale = db.query(Sale).filter(Sale.id == id).first()

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en DELETE /sales/{id}: {e}")

    if not sale:
        raise HTTPException(status_code=404, detail="Sale not found")
    
    db.delete(sale)
    db.commit()
    return "Sale successfully removed"
