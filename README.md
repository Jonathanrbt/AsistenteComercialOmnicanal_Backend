# Crear entorno virtual
python -m venv venv --> crear entorno virtual

## En Linux/macOS:

source venv/bin/activate

## En Windows:

venv\Scripts\activate

# Instalar dependencias

pip install -r requirements.txt

# En caso de instalar nuevas dependencias
pip freeze > requirements.txt --> generar el reqs.txt de nuevo (en caso de instalar nuevas dependencias)

# Ejecutar el servidor de desarrollo

uvicorn app.main:app --reload

 CC-02/KB_recuperacion
## KB y recuperación (opcional pero ya funcional)

### 1. Levantar Qdrant (solo la primera vez)

docker run -d --name qdrant -p 6333:6333 qdrant/qdrant

## cargar la KB

python app/scripts/ingest.py

## si se quiere probar la recuperacion

python -c "from app.services.search import retrieve_products; print(retrieve_products('playstation', threshold=0.0))"

## ruta para ver los productos 

http://localhost:6333/dashboard

# Se abre otra terminal para ejecutar el bot de telegram

# Ejecutar el archivo donde esta el webhook para el bot y lo conecta con la API

python -m app.run


