import geocoder
from bs4 import BeautifulSoup
import requests
import lxml
import pandas as pd
import logging
from telegram.ext import Application, MessageHandler, filters,  CommandHandler, ConversationHandler
import logging
import telebot
from telegram import ReplyKeyboardMarkup
import config
import aiohttp
info = requests.get("https://api.openweathermap.org/data/2.5/weather?q=Новосибирск&appid=c062ce8252920e6e0f7e79b988cb9146&units=metric")

print(info.content)

pric = ''
a = []



BOT_TOKEN = '7062541187:AAH4DuPesp2OSwIIIW3-iSZ7qYY-rrPp-Gk'
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

async def stop(update, context):
    await update.message.reply_text("Всего доброго!")
    return ConversationHandler.END

async def help_command(update, context):
    """Отправляет сообщение когда получена команда /help"""
    await update.message.reply_text("Я расскажу тебе все о погоде сейчас. Просто введи свое имя и город")



async def start(update, context):
    global pric
    """Отправляет сообщение когда получена команда /start"""
    user = update.effective_user
    pric = str(user)
    pric = pric.split(' ')[5]
    pric = pric[10:]
    pric = pric[:-2]
    a.append(pric)
    print(pric)
    if pric == 'Hgwkx':
        await update.message.reply_html(
            rf"Привет {user.mention_html()}! Я погода-бот. Как мне тебя называть, о великий автор бота?",
        )
    elif pric == '':
        await update.message.reply_html(
            rf"Привет {user.mention_html()}!",
        )

    else:
        await update.message.reply_html(
            rf"Привет {user.mention_html()}! Я погода бот. Как мне тебя называть?",
        )
    return 1


async def first_response(update, context):
    context.user_data['locality'] = update.message.text
    name = update.message.text
    print(a)

    await update.message.reply_text(
        f"В каком городе ты живешь, {name}?")
    return 2

async def second_response(update, context):
    city = update.message.text
    logger.info(city)
    # Используем user_data в ответе.
    await update.message.reply_text(
        f"Прекрасно! сейчас посмотрим погоду в городе {city}!")
    context.user_data.clear()
    return ConversationHandler.END # Константа, означающая конец диалога.
# Все обработчики из states и fallbacks становятся неактивными.


def polpogody(info_content):


async def pogoda(update, context):
    await update.message.reply_text(
        "Привет, пришли данные o погоде в твоем городе!")
    return 1


def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("help", help_command))
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, first_response)],
            2: [MessageHandler(filters.TEXT & ~filters.COMMAND, second_response)]
        },

        fallbacks=[CommandHandler('stop', stop)]
    )

    application.add_handler(conv_handler)

    #application.add_handler(geo_dialog_handler())
    application.run_polling()

if __name__ == '__main__':
    main()
