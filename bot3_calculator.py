from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler
from api_key import TELEGRAM_BOT_TOKEN

import logging
import datetime as dt

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot3_calculator.log'
                    )

PROXY = {'proxy_url': 'socks5://t1.learn.python.ru:1080',
    'urllib3_proxy_kwargs': {'username': 'learn', 'password': 'python'}}

def greet_user(bot, update):
    text = 'Вызван /start'
    print(text)
    update.message.reply_text(text)


def calculation(bot, update):
    user_text = update.message.text
    signs = '-+*/'
    if user_text.endswith('='):
        user_text = user_text[:-1]
        if user_text == '':
            print('Неверный формат')
            update.message.reply_text('Неверный формат')
            return
        else:
            for char in user_text:
                if not char.isdigit():
                    if not char in signs:
                        print('Неверный формат')
                        update.message.reply_text('Неверный формат')
                        return
                    
        for elem in signs:
            if elem in user_text:
                sep_sign = elem
                print(sep_sign)
        try:
            one = float(user_text.split(sep_sign)[0])
            two = float(user_text.split(sep_sign)[1])
        except ValueError:
            print('Неверный формат')
            update.message.reply_text('Неверный формат')

        if sep_sign == '+':
            answer = one + two
        elif sep_sign == '-':
            answer = one - two
        elif sep_sign == '*':
            answer = one * two
        elif sep_sign == '/':

            try:
                answer = one / two
            except ZeroDivisionError:
                print('Делить на 0 нельзя')
                update.message.reply_text('Делить на 0 нельзя')
                return

        if answer % 1 == 0:
            answer = int(answer)

        print(answer)
        update.message.reply_text(answer)
    else:
        print('Вы забыли знак равенства')
        update.message.reply_text('Вы забыли знак равенства')


def main():
    mybot = Updater(TELEGRAM_BOT_TOKEN, request_kwargs=PROXY)


    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(MessageHandler(Filters.text, calculation))


    mybot.start_polling()
    mybot.idle()

main()
