from fastapi import APIRouter, Query, HTTPException
from typing import Optional, Dict, Any
from pydantic import BaseModel
from services.ragService import get_rag

router = APIRouter()

class SearchRequest(BaseModel):
    query: str
    limit: int = 5
    filters: Optional[Dict[str, Any]] = None

@router.post("/search")
async def semantic_search(request: SearchRequest):
    try:
        rag = get_rag()
        result = rag.search_context(
            query=request.query,
            limit=request.limit, 
            filters=request.filters
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/search/products")
async def search_products(
    q: str = Query(..., description="Búsqueda"),
    limit: int = Query(5, ge=1, le=20),
    category: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    in_stock: Optional[bool] = None
):
    filters = {}
    if category:
        filters["category"] = category
    if min_price or max_price:
        price_filter = {}
        if min_price: price_filter["gte"] = min_price
        if max_price: price_filter["lte"] = max_price  
        filters["price"] = price_filter
    if in_stock:
        filters["stock"] = {"gt": 0}
    
    try:
        rag = get_rag()
        result = rag.search_context(q, limit, filters if filters else None)
        
        products = []
        for item in result["sources"]:
            payload = item["content"]
            if "product_id" in payload:
                products.append({
                    "product_id": payload["product_id"],
                    "title": payload.get("title"),
                    "price": payload.get("price"),
                    "category": payload.get("category"),
                    "stock": payload.get("stock", 0),
                    "relevance": round(item["score"], 3)
                })
        
        return {"products": products, "total": len(products)}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/rag")
async def rag_with_llm(request: SearchRequest):
    try:
        rag = get_rag()
        result = rag.rag_complete(
            query=request.query,
            limit=request.limit,
            filters=request.filters  
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))