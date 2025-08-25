FROM python:3.11-slim

# Directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements primero (para cache de Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código de la aplicación
COPY . .

# Crear directorio de datos si no existe
RUN mkdir -p data

# Exponer puerto
EXPOSE 8000

# Variables de entorno por defecto
ENV QDRANT_URL=http://qdrant:6333
ENV QDRANT_COLLECTION=kb_products
ENV PYTHONPATH=/app

# Comando por defecto
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]