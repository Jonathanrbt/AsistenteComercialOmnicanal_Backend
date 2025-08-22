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

app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
        "version": version
    }

@app.get("/api/health")
def api_health_check():
    return {
        "status": "healthy", 
        "service": "backend",
        "database": "connected"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)