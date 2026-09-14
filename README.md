# Seminario de Python - Agustín Bengolea

### *Funcionalidades:*

- ABM completo de productos.
- ABM completo de ventas.
- Cálculo automático del total de cada venta.


## Instalación

- Open Powershell/Bash/Terminal and navigate to project folder.
- Run `python -m venv .venv` for creating venv.
- Run `.venv/Scripts/activate` for activating venv.
- Run `pip install -r requirements.txt` for installing libraries from requirements file.
- Run `fastapi run` or `uvicorn app:app --reload` for running app at localhost and default port (8000).
- Open browser and go to localhost:8000/docs for swagger documentation.

## Endpoints principales

| Recurso | Operaciones |
| --- | --- |
| `/products` | `GET`, `POST` |
| `/products/{product_id}` | `GET`, `PUT`, `DELETE` |
| `/sales` | `GET`, `POST` |
| `/sales/{sale_id}` | `GET`, `PUT`, `DELETE` |
