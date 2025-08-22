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

# Se abre otra terminal para ejecutar el bot de telegram

# Ejecutar el archivo donde esta el webhook para el bot y lo conecta con la API

python -m app.run


