from sqlmodel import SQLModel, create_engine, Session
from typing import Annotated
from fastapi import Depends

sqlite_file_name = "assist.db"
DATABASE_URL = "sqlite:///./assist.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    print("Creando tablas de la base de datos...")
    SQLModel.metadata.create_all(engine)
    print("Tablas creadas exitosamente.")

def get_session():
    with Session(engine) as session:
        yield session

session_dep = Annotated[Session, Depends(get_session)]