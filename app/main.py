import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.utils.dbConn import create_db_and_tables
from dotenv import load_dotenv

load_dotenv()

project_name = os.getenv("PROJECT_NAME", "Asistente Comercial Omnicanal")
version = os.getenv("VERSION", "1.0.0")
frontend_origin = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")

app = FastAPI(
    title=project_name,
    version=version,
    description="Backend para el asistente comercial omnicanal.",
)

# 🔧 CONFIGURACIÓN CORS - ACTUALIZADA
origins = [
    "http://localhost:5173",  # Vue.js/React dev server
    "http://localhost:3000",  # React dev server alternativo
    "http://127.0.0.1:5173",  # Vue.js/React con IP
    "http://127.0.0.1:3000",  # React con IP
    "https://localhost:5173",  # HTTPS local
    "https://127.0.0.1:5173",  # HTTPS con IP
    # Agrega aquí tu dominio de producción cuando lo tengas
    # "https://tudominio.com",
    # "https://www.tudominio.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Lista de orígenes permitidos
    allow_credentials=True,  # Permitir cookies y auth headers
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos los headers
    expose_headers=["*"],  # Exponer todos los headers al frontend
    max_age=600,  # Cachear preflight requests por 10 minutos
)

# Importar routers después de definir la app para evitar problemas de importación circular
from app.routes.auth import auth_router
app.include_router(auth_router, prefix="/api", tags=["Authentication"])

@app.on_event("startup")
def on_startup():
    print("Iniciando aplicación...")
    create_db_and_tables()
    print("Aplicación iniciada correctamente")

@app.get("/")
def health_check():
    return {
        "status": "ok", 
        "message": "Asistente Comercial Omnicanal API",
        "version": version,
        "cors_enabled": True,
        "allowed_origins": origins
    }

@app.get("/api/health")
def api_health_check():
    return {
        "status": "healthy", 
        "service": "backend",
        "database": "connected",
        "cors": "enabled"
    }

# 🔧 Endpoint para verificar configuración CORS
@app.options("/{path:path}")
async def options_handler():
    return {"message": "CORS preflight handled"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)