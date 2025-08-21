from dotenv import load_dotenv
import os
from fastapi import APIRouter
import telebot
from pyngrok import ngrok, conf

router= APIRouter(tags=["Telegram"])   

load_dotenv()

telegram_token = os.getenv("TELEGRAM_TOKEN")
ngrok_token = os.getenv("NGROK_TOKEN")

bot=telebot.TeleBot(telegram_token)

@router.post("/set_webhook")
def webhook():
    if request.headers.get*("content-type") == "application/json":
        update = telebot.types.Update.de_json(request.stream.read().decode("utf-8")) # Como esta en formato bites, lo decodificamos a utf-8 (JSON)
        bot.process_new_updates([update])
        return "ok" , 200
    
# Responde a los comandos /start y /help
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Como estas ,chaval?")


#Gestionar los mensajes de texto recibidos
@bot.message_handler(content_types=['text'])#Osea actua con cualquier mensaje de texto
def bot_texto(message):
    bot.send_message(message.chat.id,message.text,parse_mode="HTML")#Reenvia el mismo mensaje que recibe)

