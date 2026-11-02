from fastapi import FastAPI, HTTPException, status, Query
from database import db_session, Base, engine
from datetime import date
from models import Product, Sale, Cart, CartProduct
from schemas import (
    ProductCreate, 
    ProductResponse,
    CartCreate,
    CartProductCreate,
    CartResponse,
    SaleCreate,
    SaleUpdate,
    SaleCartAssign,
    SaleResponse,
)

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

@app.post("/products", status_code=status.HTTP_201_CREATED, response_model=ProductResponse)
def create_product(product_data: ProductCreate):
    try:
        new_product = Product.query.filter_by(name=product_data.name).first()

        if new_product:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Product already exists")

        new_product = Product(name=product_data.name, price=product_data.price)

        db_session.add(new_product)
        db_session.commit()
        db_session.refresh(new_product)

        response = new_product
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


@app.get("/products/{product_id}", status_code=status.HTTP_200_OK, response_model=ProductResponse)
def get_product(product_id: int):
    try:
        product = Product.query.get(product_id)

        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

        response = product
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

#POST
@app.post("/sales", status_code=status.HTTP_201_CREATED, response_model=SaleResponse)
def create_sale(sale_data: SaleCreate):
    try:
        cart = Cart.query.get(sale_data.cart_id)

        if not cart:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart does not exist")

        if cart.status != "close":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only carts with status 'close' can be assigned to a sale"
            )

        if Sale.query.filter_by(cart_id=cart.id).first():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Cart is already assigned to another sale"
            )

        total_price = sum(item.quantity * item.product.price for item in cart.items)

        sale = Sale(
        date=sale_data.date,
        time=sale_data.time,
        cart_id=cart.id,
        total_price=total_price
        )

        db_session.add(sale)
        db_session.commit()
        db_session.refresh(sale)
        return sale
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occurred while trying to create sale: {e}")

#GET
@app.get("/sales", status_code=status.HTTP_200_OK, response_model=list[SaleResponse])
def get_sales(
    date_from: date | None = Query(None, alias="date-from"),
    date_to: date | None = Query(None, alias="date-to")
):
    try:
        if date_from and date_to and date_from > date_to:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="date-from must be before or equal to date-to")

        query = Sale.query

        if date_from:
            query = query.filter(Sale.date >= date_from)

        if date_to:
            query = query.filter(Sale.date <= date_to)

        sales = query.all()
        return sales
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occurred while trying to get sales: {e}")

#GET ID
@app.get("/sales/{sale_id}", status_code=status.HTTP_200_OK, response_model=SaleResponse)
def get_sale(sale_id: int):
    try:
        sale = Sale.query.get(sale_id)

        if not sale:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sale not found")
        
        return sale
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occurred while trying to get sale with id {sale_id}: {e}")

#PUT
@app.put("/sales/{sale_id}", status_code=status.HTTP_200_OK, response_model=SaleResponse)
def update_sale(sale_id: int, sale_data: SaleUpdate):
    try:
        sale = Sale.query.get(sale_id)

        if not sale:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sale not found")

        sale.date = sale_data.date
        sale.time = sale_data.time

        db_session.add(sale)
        db_session.commit()
        db_session.refresh(sale)

        return sale
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occurred while trying to update sale with id {sale_id}: {e}")

#DELETE
@app.delete("/sales/{sale_id}", status_code=status.HTTP_200_OK)
def delete_sale(sale_id: int):
    try:
        sale = Sale.query.get(sale_id)

        if not sale:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sale not found")

        db_session.delete(sale)
        db_session.commit()

        return {"message": "Sale deleted"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occurred while trying to delete sale with id {sale_id}: {e}")


#Endpoints de Carrito













    








