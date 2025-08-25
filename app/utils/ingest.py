#!/usr/bin/env python3
import json
import sys
from pathlib import Path
from datetime import datetime
from utils.qdrantClient import get_qdrant

def load_kb_data(file_path: str = "data/productsKB.json"):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, list) else [data]
    except Exception as e:
        print(f"Error cargando {file_path}: {e}")
        return []

def transform_products(products):
    docs, metadata, ids = [], [], []
    
    for product in products:
        if not product.get("product_id"):
            continue
            
        text_content = f"""
{product.get('title', '')}
{product.get('description', '')}
Categoría: {product.get('category', '')}
Precio: ${product.get('price', 0):,.0f}
{'Disponible' if product.get('stock', 0) > 0 else 'Agotado'}
        """.strip()
        meta = {
            "text": text_content,
            "source": "products",
            "title": product.get("title"),
            "lang": "es", 
            "tags": [product.get("category", "general")],
            "created_at": datetime.utcnow().isoformat(),
            # Campos específicos para filtros
            "product_id": product["product_id"],
            "description": product.get("description", ""),
            "price": float(product.get("price", 0)),
            "category": product.get("category", "general"),
            "stock": int(product.get("stock", 0))
        }
        
        docs.append(text_content)
        metadata.append(meta)
        ids.append(product["product_id"])
    
    return docs, metadata, ids

def main():
    print("🔄 Ingesta KB en Qdrant...")
    
    products = load_kb_data()
    if not products:
        print("❌ No hay productos para ingestar")
        return False
    
    docs, metadata, ids = transform_products(products)
    print(f"📊 Procesados: {len(docs)} productos")
    
    qdrant = get_qdrant()
    success = qdrant.add_documents(docs, metadata, ids)
    
    if success:
        print(f"✅ Ingesta completada: {len(docs)} documentos")
    else:
        print("❌ Error en ingesta")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)