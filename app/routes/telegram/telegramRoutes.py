from dotenv import load_dotenv
import os
from fastapi import APIRouter ,Request
import telebot
from pyngrok import ngrok, conf
import json
router= APIRouter(tags=["Telegram"])   

load_dotenv()

telegram_token = os.getenv("TELEGRAM_TOKEN")

bot=telebot.TeleBot(telegram_token)

# Endpoint para recibir actualizaciones desde Telegram
@router.post("/webhook")
async def webhook(request: Request):
    if request.headers.get("content-type") == "application/json":# Verificamos que lo que llega sea JSON
        data = await request.json() # Obtenemos el contenido del request
        update = telebot.types.Update.de_json(data)   # Lo convertimos en objeto Update
        bot.process_new_updates([update]) # Se lo pasamos al bot para que lo maneje
        return {"status": "ok"}
    return {"status": "unsupported content"}, 400


# Responde a los comandos /start y /help
@bot.message_handler(commands=['start','help'])
def send_welcome(message):
    bot.reply_to(message, "Como estas ,chaval?") #Reply_to envia un mensaje de respuesta al usuario que envio el comando


#Gestionar los mensajes de texto recibidos que no sean comandos
@bot.message_handler(content_types=['text'])#Osea actua con cualquier mensaje de texto
def bot_texto(message):
    # parse_mode=HTML sirve para aceptar etiquetas de formato HTML en el texto.
    bot.send_message(message.chat.id,message.text,parse_mode="HTML")#Reenvia el mismo mensaje que recibe , message.chat.id es el id del chat de telegram donde se envia el mensaje , y message.text es el texto del mensaje que se envia

