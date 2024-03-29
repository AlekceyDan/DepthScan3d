
from subprocess import Popen
from subprocess import PIPE
import cv2
import scan as make3d

import DenseDepth.test as net
import video

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
TG_TOKEN = "your_token"

def do_start(bot: Bot, update: Update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text = "Привет! Я бот, который способен сделать 3d модель по картинке. Отправь пожайлуста фото прямо сюда!"
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

        downloaded_file = file_info.download("test.png")


        im = cv2.imread("test.png")
        height, width, channels = im.shape

        im = cv2.resize(im, (640, 480))

        cv2.imwrite("test.png",im)







        bot.send_message(chat_id= chat_id, text = "Создаю карту глубин...")
        net.depth_net()

        im = cv2.imread("depth.png")
        im = cv2.resize(im, (width,height))


        im = im-im.min()
        im = im/im.max()*255
        cv2.imwrite("depth.png",im)


        if height>width:
            im = cv2.imread("depth.png")
            im = cv2.resize(im, (240, 320))
            cv2.imwrite("depth.png",im)





        bot.send_message(chat_id= chat_id, text = "Карта глубин готова.")




        bot.send_photo(chat_id= chat_id, photo = open('depth.png', 'rb'))
        bot.send_message(chat_id= chat_id, text = "Создаю 3d модель")
        make3d.start("depth.png")
        bot.send_document(chat_id=chat_id, document=open('test_3d.stl', 'rb'))

    except Exception as e:
        bot.send_message(chat_id= chat_id, text = e)



def handle_docs_video(bot: Bot, update: Update):
    try:

        chat_id = update.message.chat.id

        file_info = bot.get_file(update.message.video.file_id)

        downloaded_file = file_info.download("in.mp4")


        #im = cv2.imread("")
        #height, width, channels = im.shape

        #im = cv2.resize(im, (640, 480))

        #cv2.imwrite("test.png",im)




        bot.send_message(chat_id= chat_id, text = "Создаю карту глубин...")
        video.video("in.mp4")
        video.save()

        #im = cv2.imread("depth.png")
        #im = cv2.resize(im, (width,height))
        #cv2.imwrite("depth.png",im)

        '''
        if height>width:
            im = cv2.imread("depth.png")
            im = cv2.resize(im, (240, 320))
            cv2.imwrite("depth.png",im)
        '''

        bot.send_message(chat_id= chat_id, text = "Карта глубин готова.")




        bot.send_video(chat_id= chat_id, video = open('movie.mp4', 'rb'))
        #bot.send_message(chat_id= chat_id, text = "Создаю 3d модель")
        #make3d.start("depth.png")
        #bot.send_document(chat_id=chat_id, document=open('test_3d.stl', 'rb'))

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
    video_handler = MessageHandler(Filters.video, handle_docs_video)

    updater.dispatcher.add_handler(start_handler)
    #updater.dispatcher.add_handler(help_handler)
    #updater.dispatcher.add_handler(time_handler)
    updater.dispatcher.add_handler(image_handler)
    updater.dispatcher.add_handler(video_handler)

    #updater.dispatcher.add_handler(message_handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
