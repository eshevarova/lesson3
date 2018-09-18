from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from api_key import key

import ephem
import logging
import datetime as dt

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot3_wordcount.log'
                    )

PROXY = {'proxy_url': 'socks5://t1.learn.python.ru:1080',
    'urllib3_proxy_kwargs': {'username': 'learn', 'password': 'python'}}

def greet_user(bot, update):
    text = 'Вызван /start'
    print(text)
    update.message.reply_text(text)


def count_word(bot, update):
    user_phrase = update.message.text[11:]
    length = 0
    if user_phrase[0] == '"' and user_phrase[-1] == '"' and len(user_phrase) == 2:
        print(length)
        update.message.reply_text(length)
    elif user_phrase[0] == '"' and user_phrase[-1] == '"' and len(user_phrase) > 2:
        user_phrase = user_phrase[1:-1]
        if (' ') in user_phrase:
            user_phrase = user_phrase.split(' ')
            length = len(user_phrase)
        elif (',') in user_phrase:
            user_phrase = user_phrase.split(',')
            length = len(user_phrase)
        elif ('"') in user_phrase:
            user_phrase = user_phrase.split('"')
            length = len(user_phrase)
        else:
            length = 1
        print(user_phrase, length)
        update.message.reply_text(length)
    else:
        print('Расставьте кавычки правильно')
        update.message.reply_text('Расставьте кавычки правильно')


def main():
    mybot = Updater(key, request_kwargs=PROXY)


    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler('wordcount', count_word))


    mybot.start_polling()
    mybot.idle()

main()
