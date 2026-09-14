from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine("sqlite:///./database.db", connect_args={"check_same_thread": False})

Base = declarative_base()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

""" 
autocommit=False: los cambios no se guardan automáticamente.
autoflush=False: SQLAlchemy no envía cambios automáticamente antes de cada consulta.
bind=engine: conecta la fábrica con SQLite. 
"""

def get_db():
    db = SessionLocal()
    try:
        yield db  # la función se pausa y "entrega" esa sesión (db) a quien la llamó. FastAPI la recibe y se la pasa al endpoint.
    finally:
        db.close()  # Una vez que el endpoint termina de ejecutarse, la función se reanuda y cierra la sesión (db).