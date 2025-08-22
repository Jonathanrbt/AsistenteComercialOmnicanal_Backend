"""
Carga productos desde products.json a Qdrant.
Ejecutar: python app/scripts/ingest.py
"""
import sys, json, hashlib
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from fastembed import TextEmbedding
import os

client = QdrantClient(os.getenv("QDRANT_URL", "http://localhost:6333"))
model = TextEmbedding("sentence-transformers/all-MiniLM-L6-v2")
COLLECTION = "company_kb"
VECTOR_SIZE = 384

# Crear colección si no existe
try:
    client.get_collection(COLLECTION)
except:
    client.create_collection(
        collection_name=COLLECTION,
        vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE)
    )

# Cargar productos
kb_path = Path(__file__).resolve().parent.parent / "kb"
with open(kb_path / "products.json", encoding="utf-8") as f:
    products = json.load(f)

points = []
for p in products:
    text = f"{p['title']}. {p['description']} Precio: {p['price']} COP. Categoría: {p['category']}. Stock: {p['stock']}."
    vector = next(model.embed([text]))
    points.append(
        PointStruct(
            id=p["product_id"],
            vector=vector.tolist(),
            payload=p  # Guardamos el JSON completo
        )
    )

client.upsert(COLLECTION, points)
print(f"{len(points)} producto(s) cargado(s) en Qdrant.")