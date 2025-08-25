import os
import requests
from typing import Protocol

class LLMProvider(Protocol):
    def generate(self, prompt: str, context: str) -> str:
        ...

class OllamaAdapter:
    def __init__(self, model: str = "llama3.2"):
        self.base_url = os.getenv("OLLAMA_URL", "http://localhost:11434")
        self.model = model
    
    def generate(self, prompt: str, context: str) -> str:
        try:
            response = requests.post(f"{self.base_url}/api/generate", json={
                "model": self.model,
                "prompt": prompt,
                "stream": False
            })
            if response.status_code == 200:
                return response.json().get("response", "Error generando respuesta")
            return f"Error Ollama: {response.status_code}"
        except Exception as e:
            return f"Error conectando Ollama: {e}"

# class OpenAIAdapter:
#     def __init__(self, model: str = "gpt-4o-mini"):
#         self.api_key = os.getenv("OPENAI_API_KEY")
#         self.model = model
    
#     def generate(self, prompt: str, context: str) -> str:
#         if not self.api_key:
#             return "OpenAI API key no configurado"
        
#         try:
#             import openai
#             client = openai.OpenAI(api_key=self.api_key)
            
#             response = client.chat.completions.create(
#                 model=self.model,
#                 messages=[
#                     {"role": "system", "content": "Responde basándote en el contexto proporcionado."},
#                     {"role": "user", "content": prompt}
#                 ],
#                 max_tokens=500,
#                 temperature=0.1
#             )
#             return response.choices[0].message.content
#         except Exception as e:
#             return f"Error OpenAI: {e}"

# def get_llm_adapter(provider: str, **kwargs) -> LLMProvider:
#     if provider == "ollama":
#         return OllamaAdapter(**kwargs)
#     elif provider == "openai":
#         return OpenAIAdapter(**kwargs)
#     else:
#         raise ValueError(f"Provider {provider} no soportado")