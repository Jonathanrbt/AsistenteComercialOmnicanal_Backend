import os
from typing import List, Dict, Optional
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, Filter

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
COLLECTION = os.getenv("QDRANT_COLLECTION", "kb_products")

class QdrantService:
    def __init__(self):
        self.client = QdrantClient(url=QDRANT_URL)
        self.collection = COLLECTION
    
    def search(self, query: str, limit: int = 5, filters: Optional[Dict] = None) -> List[Dict]:
        try:
            query_filter = self._build_filter(filters) if filters else None
            
            results = self.client.query(
                collection_name=self.collection,
                query_text=query,
                limit=limit,
                query_filter=query_filter,
                with_payload=True
            )
            
            context_items = []
            for result in results:
                context_items.append({
                    "score": result.score,
                    "content": result.payload
                })
            
            return context_items
            
        except Exception as e:
            print(f"Error en búsqueda: {e}")
            return []
    
    def _build_filter(self, filters: Dict) -> Filter:
        from qdrant_client.models import FieldCondition, MatchValue, Range
        
        conditions = []
        for key, value in filters.items():
            if isinstance(value, dict) and any(op in value for op in ["gte", "lte", "gt", "lt"]):
                conditions.append(FieldCondition(key=key, range=Range(**value)))
            else:
                conditions.append(FieldCondition(key=key, match=MatchValue(value=value)))
        
        return Filter(must=conditions)
    
    def ensure_collection(self):
        try:
            collections = [c.name for c in self.client.get_collections().collections]
            if self.collection not in collections:
                self.client.create_collection(
                    collection_name=self.collection,
                    vectors_config=VectorParams(size=384, distance=Distance.COSINE)
                )
        except Exception as e:
            print(f"Error creando colección: {e}")
    
    def add_documents(self, docs: List[str], metadata: List[Dict], ids: List[int]):
        try:
            self.ensure_collection()
            self.client.add(
                collection_name=self.collection,
                documents=docs,
                metadata=metadata,
                ids=ids
            )
            return True
        except Exception as e:
            print(f"Error añadiendo documentos: {e}")
            return False

_service = None
def get_qdrant() -> QdrantService:
    global _service
    if _service is None:
        _service = QdrantService()
    return _service