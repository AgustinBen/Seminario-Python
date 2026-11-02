from fastapi import FastAPI, HTTPException, status, Query
# from database import Base, engine, get_db
from database import db_session, Base, engine
from models import Product, Sale
from schemas import ProductCreate, ProductResponse

Base.metadata.create_all(bind=engine)
app = FastAPI()

@app.middleware("http")
def close_db_session(request, call_next):
    response = call_next(request)
    db_session.remove()
    return response

@app.get("/")
def root():
    return {'message': 'Hello'}

# Endpoints de Producto

@app.post("/products", status_code=status.HTTP_201_CREATED)
def post_product(product_data: ProductCreate):
    try:
        new_product = Product.query.filter_by(name=product_data.name).first()

        if new_product:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Product already exists")

        new_product = Product(name=product_data.name, price=product_data.price)

        db_session.add(new_product)
        db_session.commit()
        db_session.refresh(new_product)

        response = {"product" : new_product}
        return response
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occurred while trying to create product: {e}")


@app.get("/products", status_code=status.HTTP_200_OK)
def get_products():
    try:
        products = Product.query.all()
        response = {"products" : products}
        return response
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail= f"An error occurred while trying to get products: {e}")


@app.get("/products/{product_id}", status_code=status.HTTP_200_OK)
def get_product(product_id: int):
    try:
        product = Product.query.get(product_id)

        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

        response = {"product": product}
        return response
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occurred while trying to get product with id: {product_id}: {e}")


@app.put("/products/{product_id}", status_code=status.HTTP_200_OK)
def update_product(product_id: int, product_data: ProductCreate):
    try:
        product = Product.query.get(product_id)

        if not product:
            raise (HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"))

        existing_product = Product.query.filter(Product.name == product_data.name, Product.id != product_id).first()
        
        if existing_product:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Product already exists")

        product.name = product_data.name
        product.price = product_data.price

        db_session.add(product)
        db_session.commit()
        db_session.refresh(product)

        response = {"product" : product}
        return response
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occurred while trying to update product with id {product_id}: {e}")

@app.delete("/products/{product_id}", status_code=status.HTTP_200_OK)
def delete_product(product_id: int):
    try:
        product = Product.query.get(product_id)

        if not product:
            raise (HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"))

        # if product.cart_items:
        #     raise HTTPException(
        #         status_code=status.HTTP_409_CONFLICT,
        #         detail="Product cannot be deleted because it is registered in a cart"
        #     )

        db_session.delete(product)
        db_session.commit()

        return {"message": "Product deleted"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occurred while trying to delete product with id {product_id}: {e}")






# Endpoints de Venta
