from fastapi import FastAPI, status

app = FastAPI()

@app.get("/")
def hello_world():
    return {"message": "¡Hola, mundo!"}


@app.get("/products", status_code=status.HTTP_200_OK)
def get_products():
    return {"message" : "Lista de Productos"}

@app.get("/products/{id}", status_code=status.HTTP_200_OK)
def get_product(id: int):
    return {"message" : f"Producto con id {id}"}





""" ● POST /productos  
● GET /productos  
● GET /productos/{id} 
● PUT /productos/{id} 
● DELETE /productos/{id}  """