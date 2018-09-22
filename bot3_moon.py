from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler
from api_key import TELEGRAM_BOT_TOKEN

import logging
import datetime as dt
import ephem
import re

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot3_moon.log'
                    )

PROXY = {'proxy_url': 'socks5://t1.learn.python.ru:1080',
    'urllib3_proxy_kwargs': {'username': 'learn', 'password': 'python'}}

def greet_user(bot, update):
    text = 'Вызван /start'
    print(text)
    update.message.reply_text(text)


def full_moon(bot, update):
    user_text = update.message.text
    try:
        date = re.search('(\\d{4}/\\d{2}/\\d{2})|(\\d{4}-\\d{2}-\\d{2})', user_text)[0]
    except TypeError:
        print('Неверная дата')
        update.message.reply_text('Неверная дата')
        return

    date_full_moon = ephem.next_full_moon(date)
    print('Ближайшее полнолуние наступит {}'.format(date_full_moon))
    update.message.reply_text('Ближайшее полнолуние наступит {}'.format(date_full_moon))


def main():
    mybot = Updater(TELEGRAM_BOT_TOKEN, request_kwargs=PROXY)


    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(MessageHandler(Filters.text, full_moon))


    mybot.start_polling()
    mybot.idle()

main()
