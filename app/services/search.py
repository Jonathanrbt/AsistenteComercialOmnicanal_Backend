"""
Servicio para recuperar los productos desde el Qdrant
"""
import os
from qdrant_client import QdrantClient
from fastembed import TextEmbedding


QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333") 
TOP_K = int(os.getenv("TOP_K", 3)) 
SCORE_THRESHOLD = float(os.getenv("SCORE_THRESHOLD", 0.75))

client = QdrantClient(QDRANT_URL)
model = TextEmbedding("sentence-transformers/all-MiniLM-L6-v2")
COLLECTION = "company_kb"

def retrieve_products(question: str, top_k: int = TOP_K, threshold: float = SCORE_THRESHOLD):
    vector = next(model.embed([question]))
    hits = client.search(
        collection_name=COLLECTION,
        query_vector=vector.tolist(),
        limit=top_k,
        score_threshold=threshold
    )
    return [hit.payload for hit in hits]  # devuelve los JSON completos