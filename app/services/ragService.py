from typing import List, Dict, Optional, Protocol
from utils.qdrantClient import get_qdrant

# from adapters.llm_adapters import get_llm_adapter

# rag = RAGService(get_llm_adapter("ollama"))  # u "openai"
# result = rag.rag_complete("¿qué consolas tienes?")

class LLMProvider(Protocol):
    def generate(self, prompt: str, context: str) -> str:
        ...

class RAGService:
    def __init__(self, llm_provider: Optional[LLMProvider] = None):
        self.qdrant = get_qdrant()
        self.llm = llm_provider
    
    def search_context(self, query: str, limit: int = 5, filters: Optional[Dict] = None) -> Dict:
        results = self.qdrant.search(query, limit, filters)
        context_text = self._build_context(results)
        
        return {
            "query": query,
            "context": context_text,
            "sources": results,
            "ready_for_llm": True
        }
    
    def rag_complete(self, query: str, limit: int = 5, filters: Optional[Dict] = None) -> Dict:
        search_result = self.search_context(query, limit, filters)
        
        if not self.llm:
            return {
                **search_result,
                "answer": "No LLM configured - use search_context() for retrieval only"
            }
        prompt = self._build_prompt(query, search_result["context"])
        answer = self.llm.generate(prompt, search_result["context"])
        
        return {
            **search_result,
            "answer": answer
        }
    
    def _build_context(self, results: List[Dict]) -> str:
        if not results:
            return "No se encontraron productos relevantes."
        
        context_parts = []
        for i, item in enumerate(results, 1):
            payload = item["content"]
            score = item["score"]
            product_text = f"[Producto {i}] {payload.get('title', 'Sin título')}"
            if payload.get('description'):
                product_text += f" - {payload['description']}"
            if payload.get('price'):
                product_text += f" - Precio: ${payload['price']:,.0f}"
            if payload.get('stock', 0) > 0:
                product_text += f" - Disponible ({payload['stock']} unidades)"
            else:
                product_text += " - Agotado"
            
            context_parts.append(product_text)
        
        return "\n\n".join(context_parts)
    
    def _build_prompt(self, question: str, context: str) -> str:
        return f"""Responde basándote SOLO en la siguiente información de productos:

{context}

Pregunta: {question}

Respuesta:"""

def create_rag_service(llm_type: str = None) -> RAGService:
    pass
    #if llm_type == "openai":
        #from adapters.openai_adapter import OpenAIAdapter
        #return RAGService(OpenAIAdapter())
    #elif llm_type == "ollama":
        #from adapters.ollama_adapter import OllamaAdapter  
        #return RAGService(OllamaAdapter())
    #else:
        # Solo búsqueda, sin LLM
        #return RAGService()

# Instancia por defecto (solo búsqueda)
_rag_service = RAGService()

def get_rag() -> RAGService:
    return _rag_service