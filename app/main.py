from fastapi import FastAPI
from sqlmodel import SQLModel
from app.utils.dbConn import engine
from app.models import userModel, chatModel, messageModel
from app.services.search import retrieve_products
from app.routes.telegram.telegramRoutes import router as telegramRouter
from routes.ragRoutes import router as rag_router

app = FastAPI()
appII= FastAPI(title="RAG Search API", version="1.0.0")

app.include_router(telegramRouter, prefix="/api/telegram")

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/search")
def search(query: str):
    return retrieve_products(query)

appII.include_router(rag_router, prefix="/api", tags=["rag"])

@appII.get("/")
async def root():
    return {
        "message": "RAG Search API",
        "endpoints": {
            "search": "POST /api/search - Búsqueda semántica",
            "products": "GET /api/search/products - Buscar productos",
            "rag": "POST /api/rag - RAG completo (necesita LLM)",
            "docs": "GET /docs - Documentación"
        }
    }