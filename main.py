import requests
from telegram.ext import Application, MessageHandler, filters,  CommandHandler, ConversationHandler
import logging
from telegram import ReplyKeyboardMarkup
from math import *
pric = ''
a = []
gorod = ''
reply_keyboard = [['/pogoda', '/data'],
                  ['/help']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

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
    global gorod
    city = update.message.text
    gorod = city
    logger.info(city)
    # Используем user_data в ответе.
    print(city)
    await update.message.reply_text(
        f"Прекрасно! сейчас посмотрим погоду в городе {city}!",
    reply_markup=markup
    )
    context.user_data.clear()
    return ConversationHandler.END, city



async def data(update, context):
    await update.message.reply_text(
        f"Ты смотришь погоду в городе {gorod}"
    )
    return 1


async def pogoda(update, context):
    global gorod
    info = requests.get(
        "https://api.openweathermap.org/data/2.5/weather?q=" + gorod + "&appid=c062ce8252920e6e0f7e79b988cb9146&units=metric")
    ds = info.content.decode('UTF-8')
    ds = ds.split('\"')
    f = {}
    for i in range(len(ds)):
        if ds[i] == 'temp':
            asd = ds[i + 1]
            asd = asd[1:]
            asd = asd[:-1]
            f['Темп'] = floor(float(asd))
        elif ds[i] == 'feels_like':
            asd = ds[i + 1]
            asd = asd[1:]
            asd = asd[:-1]
            f['Темпчув'] = floor(float(asd))
        elif ds[i] == 'weather':
            asd = ds[i + 6]
            f['Погода'] = asd
        elif ds[i] == 'humidity':
            asd = ds[i + 1]
            asd = asd[1:]
            asd = asd[:-2]
            f['Влажность'] = asd + '%'
        elif ds[i] == 'speed':
            asd = ds[i + 1]
            asd = asd[1:]
            asd = asd[:-1]
            f['Скоростьветра'] = str(asd) + 'м/с'
        else:
            print("Что то пошло не так")

    await update.message.reply_text(
        f"Погода в городе {gorod}:\n"
        f"Температура равна {f['Темп']}\n"
        f"Ощущается как {f['Темпчув']}\n"
        f"Погода - {f['Погода']}\n"
        f"Влажность {f['Влажность']}\n"
        f"Скорость ветра равна {f['Скоростьветра']}"
    )

    return f

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("pogoda", pogoda))
    application.add_handler(CommandHandler("data", data))
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, first_response)],
            2: [MessageHandler(filters.TEXT & ~filters.COMMAND, second_response)]
        },

        fallbacks=[CommandHandler('stop', stop)]
    )

    application.add_handler(conv_handler)

    application.run_polling()



if __name__ == '__main__':
    main()
