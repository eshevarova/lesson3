from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler
from api_key import key
from telegram import ReplyKeyboardMarkup

import logging
import random

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot3_cities.log'
                    )

PROXY = {'proxy_url': 'socks5://t1.learn.python.ru:1080',
    'urllib3_proxy_kwargs': {'username': 'learn', 'password': 'python'}}

def greet_user(bot, update):
    text = 'Вызван /start'
    print(text)
    update.message.reply_text(text)


def cities_play(bot, update):
    with open('cities.txt', 'r', encoding='utf-8') as f:
        cities_list = f.readlines()
        cities_list = [elem.rstrip('\n') for elem in cities_list]

    user_city = update.message.text[8:]

    while True:
        if user_city == 'Надоело':
            print('Ну пока')
            update.message.reply_text('Ну пока')
            break
        else:
            try:
                cities_list.remove(user_city)
            except ValueError:
                pass

            for el in cities_list:
                if el.startswith(user_city[-1].upper()):
                    bot_city = el

            #print(bot_city)
            #update.message.reply_text(bot_city)
            cities_list.remove(bot_city)
        
            user_city = update.message.text
            print(user_city)



  

     


def main():
    mybot = Updater(key, request_kwargs=PROXY)


    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler('goroda', cities_play))


    mybot.start_polling()
    mybot.idle()

main()
