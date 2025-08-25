import os
from fastapi import APIRouter, HTTPException
from app.utils.qdrantClient import get_qdrant_client, query_text

router = APIRouter()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# if OPENAI_API_KEY:
#     import openai
#     openai.api_key = OPENAI_API_KEY

@router.post("/api/rag")
async def rag_query(payload: dict):
    question = payload.get("question")
    if not question:
        raise HTTPException(status_code=400, detail="question required")
    top_k = int(payload.get("top_k", 3))
    filters = payload.get("filters")

    client = get_qdrant_client()
    results = query_text(client, question, top_k=top_k, q_filter=filters)

    contexts = [r["document"] for r in results if r.get("document")]
    evidence_text = "\n\n---\n\n".join(contexts)

    # if OPENAI_API_KEY:
    #     prompt = (
    #         "Usa SOLO la siguiente información para responder. Si la información no es suficiente, responde 'No lo sé'.\n\n"
    #         f"Contexto:\n{evidence_text}\n\nPregunta: {question}\n\nRespuesta:"
    #     )
    #     resp = openai.ChatCompletion.create(
    #         model="gpt-4o-mini",
    #         messages=[
    #             {"role": "system", "content": "Eres un asistente que responde con evidencia."},
    #             {"role": "user", "content": prompt}
    #         ],
    #         max_tokens=512,
    #         temperature=0.0
    #     )
    #     answer = resp["choices"][0]["message"]["content"]
    #     return {"answer": answer, "evidence": results}
    # else:
    #     return {"answer": None, "evidence": results}
