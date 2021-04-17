
from subprocess import Popen
from subprocess import PIPE

import echo.scan as model


from telegram import Bot
from telegram import Update
from telegram  import File
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters
from telegram.ext import CallbackQueryHandler
#from echo.config import TG_TOKEN
TG_TOKEN = "1183753875:AAGfNLR-E5SRp1_xD24pJgAdVuOezMfvWx8"

def do_start(bot: Bot, update: Update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text = "Привет! Я бот, который умеет делать 3d модель по картинке. Отправь фото прямо сюда!"
    )

def do_help(bot: Bot, update: Update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text = "Это учебный бот, помогающий решать ряды\n\n"
               "Список доступных материалов\n"
               "Признаки :\n"
               "Коши\nДаламбер\nГорячев\nРаабе"
    )
def do_time(bot: Bot, update: Update):
    process = Popen(["date"], stdout=PIPE)
    text, error = process.communicate()
    if error:
        text = "Произошла ошибка, ряд не найден"
    else:
        text = text.decode("utf-8")
    bot.send_message(
        chat_id=update.message.chat_id,
        text=text
    )


#@bot.message_handler(content_types=['document'])

def handle_docs_photo(bot: Bot, update: Update):
    try:

        chat_id = update.message.chat.id

        file_info = bot.get_file(update.message.photo[-1].file_id)

        downloaded_file = file_info.download('C:/Users/User/'+"test.jpg")
        bot.send_message(chat_id= chat_id, text = "Создаю модель...")

        model.start('C:/Users/User/'+"test.jpg")
        bot.send_message(chat_id=chat_id, text="Модель готова! Через некоторое время отправлю сюда.")
        bot.send_document(chat_id=chat_id, document=open('test_3d.stl', 'rb'))

    except Exception as e:
        bot.send_message(chat_id= chat_id, text = e)

def do_echo(bot: Bot, update: Update):
    chat_id = update.message.chat_id
    text = "Ваш ID = {}\n\n{}".format(chat_id,update.message.text)

    bot.send_message(
        chat_id=chat_id,
        text=text
    )

def main():
    bot = Bot(
        token = TG_TOKEN
    )
    updater = Updater (
         bot = bot,
    )
    start_handler = CommandHandler("start", do_start)
    #message_handler = MessageHandler(Filters.text, do_echo)
    #help_handler = CommandHandler("help", do_help)
    #time_handler = CommandHandler("time", do_time)
    image_handler = MessageHandler(Filters.photo, handle_docs_photo)

    updater.dispatcher.add_handler(start_handler)
    #updater.dispatcher.add_handler(help_handler)
    #updater.dispatcher.add_handler(time_handler)
    updater.dispatcher.add_handler(image_handler)

    #updater.dispatcher.add_handler(message_handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
