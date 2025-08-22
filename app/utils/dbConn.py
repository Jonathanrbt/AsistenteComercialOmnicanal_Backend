from sqlmodel import SQLModel, create_engine, Session
from typing import Annotated
from fastapi import Depends
import os

# Configuración de SQLite
sqlite_file_name = "assist.db"
DATABASE_URL = f"sqlite:///./{sqlite_file_name}"

# Configurar echo=True solo en desarrollo
echo = os.getenv("ENVIRONMENT", "development") == "development"
engine = create_engine(DATABASE_URL, echo=echo, connect_args={"check_same_thread": False})

def create_db_and_tables():
    print("Creando tablas de la base de datos...")
    
    try:
        # Importar todos los modelos aquí para que SQLModel los reconozca
        # SIN relaciones primero para evitar problemas
        from app.models.userModel import User
        from app.models.chatModel import Chat
        from app.models.messageModel import Message
        
        # Crear tablas
        SQLModel.metadata.create_all(engine)
        print("✅ Tablas creadas exitosamente.")
        
    except Exception as e:
        print(f"❌ Error creando tablas: {e}")
        # Si hay error, intentar crear solo la tabla de usuarios
        try:
            from app.models.userModel import User
            User.metadata.create_all(engine)
            print("✅ Tabla de usuarios creada como fallback")
        except Exception as inner_error:
            print(f"❌ Error crítico: {inner_error}")
            raise

def get_session():
    with Session(engine) as session:
        yield session

# Dependencia para inyección de sesiones
session_dep = Annotated[Session, Depends(get_session)]