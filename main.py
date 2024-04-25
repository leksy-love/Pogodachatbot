import requests
from telegram.ext import Application, MessageHandler, filters,  CommandHandler, ConversationHandler
import logging
from telegram import ReplyKeyboardMarkup
from math import *
pric = ''
a = ''
gorod = ''

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
    global pric, a
    """Отправляет сообщение когда получена команда /start"""
    user = update.effective_user
    print(user)
    pric = str(user)
    pric = pric.split(',')
    pric = pric[-1]
    pric = pric[11:]
    pric = pric[:-2]
    a = pric
    #print(pric)
    if pric == 'Hgwkx':
        await update.message.reply_html(
            rf"Привет {user.mention_html()}! Я погода-бот. Как мне тебя называть, о великий автор бота?",
        )
    else:
        await update.message.reply_html(
            rf"Привет {user.mention_html()}! Я погода-бот. Как мне тебя называть?",
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
    return gorod

reply_keyboard = [['/pogoda', '/data'],
                  ['/help', '/picture']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

async def data(update, context):
    await update.message.reply_text(
        f"Ты смотришь погоду в городе {gorod}"
    )
    return 1


async def pogoda(update, context):
    global gorod, pric
    info = requests.get(
        "https://api.openweathermap.org/data/2.5/weather?q=" + gorod + "&appid=c062ce8252920e6e0f7e79b988cb9146&units=metric")
    ds = info.content.decode('UTF-8')
    ds = ds.split('\"')
    f = {}
    with open("Names.txt", "a") as file:
        file.write('\nГород ')
        file.write(str(gorod))
        file.write(', Имя ')
        file.write(str(pric))
        file.close()
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

    await update.message.reply_text(
        f"Погода в городе {gorod}:\n"
        f"Температура равна {f['Темп']}\n"
        f"Ощущается как {f['Темпчув']}\n"
        f"Погода - {f['Погода']}\n"
        f"Влажность {f['Влажность']}\n"
        f"Скорость ветра равна {f['Скоростьветра']}"
    )

    return f

async def send_picture(update, context):
    await context.bot.send_photo(update.message.chat.id, photo='https://disk.yandex.ru/i/wZMQoKZyVEiB3g')


def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("pogoda", pogoda))
    application.add_handler(CommandHandler("data", data))
    application.add_handler(CommandHandler("picture", send_picture))
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




