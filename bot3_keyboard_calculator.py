from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from api_key import TELEGRAM_BOT_TOKEN

import logging

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot3_keyboard_calculator.log'
                    )

PROXY = {'proxy_url': 'socks5://t2.learn.python.ru:1080',
    'urllib3_proxy_kwargs': {'username': 'learn', 'password': 'python'}}


def greet_user(bot, update):
    text = 'Вызван /start'
    print(text)
    update.message.reply_text(text)


def keyboard_on(bot, update):
    chat_id = update.message.chat.id
    custom_keyboard = [['1', '2', '3', '+'],
                        ['4', '5', '6', '-'],
                        ['7', '8', '9', '*'],
                        ['.', '0', '=', ':']]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard)
    bot.send_message(chat_id=chat_id,
                    text='Введите выражение',
                    reply_markup=reply_markup)


def keyboard_off(bot, update):
    chat_id = update.message.chat.id
    reply_markup = ReplyKeyboardRemove()
    bot.send_message(chat_id=chat_id, text="Не прощаюсь", reply_markup=reply_markup)


def text_handler_for_calculator(bot, update, user_data):
    key = update.message.chat.id
    value = user_data.get(key, '') + update.message.text
    user_data[key] = value
    signs = '-+*:'
    if value.endswith('='):
        user_text = user_data[key]
        for elem in signs:
            if elem in user_text:
                sep_sign = elem

        try:
            one = float(user_text.split(sep_sign)[0])
            two = float(user_text.split(sep_sign)[1].split('=')[0])

        except ValueError:
            print('Неверный формат')
            update.message.reply_text('Неверный формат')
            return

        if sep_sign == '+':
            answer = one + two
        elif sep_sign == '-':
            answer = one - two
        elif sep_sign == ':':
            try:
                answer = one / two
            except ZeroDivisionError:
                print('Делить на 0 нельзя')
                update.message.reply_text('Делить на 0 нельзя')
                return
        elif sep_sign == '*':
            answer = one * two

        if answer % 1 == 0:
            answer = int(answer)

        print(answer)
        update.message.reply_text(answer)
        user_data.clear()


def main():
    mybot = Updater(TELEGRAM_BOT_TOKEN, request_kwargs=PROXY)


    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler('keyboard_on', keyboard_on))
    dp.add_handler(CommandHandler('keyboard_off', keyboard_off))
    dp.add_handler(MessageHandler(Filters.text, text_handler_for_calculator, pass_user_data=True))


    mybot.start_polling()
    mybot.idle()

main()
