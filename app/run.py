import os
import time
from dotenv import load_dotenv
from pyngrok import ngrok, conf
import uvicorn
from app.main import app
from app.routes.telegram.telegramRoutes import bot

load_dotenv()

ngrok_token = os.getenv("NGROK_TOKEN")

if __name__ == "__main__":
    print("BOT RUNNING")

     #Configuramos la region de ngrok
    conf.get_default().region = "sa" # South America
    #creamos las credenciales de ngrok
    ngrok.set_auth_token(ngrok_token)

    #Iniciamos el tunel de ngrok , para que el bot pueda recibir los nuevos mensajes con el puerto 8000 , mismo que usamos en FastAPI
    ngrok_tunnel = ngrok.connect(8000, bind_tls=True) # con bind indico que sea https encriptado
     #url del tunnel del https creado
    ngrok_url = ngrok_tunnel.public_url
    print(f"Ngrok Tunnel URL: {ngrok_url}")

    # Configurar webhook en Telegram
    bot.remove_webhook() #Para asegurarnos de que no haya un webhook previo
    time.sleep(1)
    bot.set_webhook(url=f"{ngrok_url}/api/telegram/webhook") # Establecer el webhook con la URL de ngrok

    # Levantar FastAPI con Uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)#Buscamos en main.py el app de FastAPI
