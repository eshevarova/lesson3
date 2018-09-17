from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler
from api_key import key
from telegram import ReplyKeyboardMarkup

import logging
import re

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot3_word_calc.log'
                    )

PROXY = {'proxy_url': 'socks5://t1.learn.python.ru:1080',
    'urllib3_proxy_kwargs': {'username': 'learn', 'password': 'python'}}

def greet_user(bot, update):
    text = 'Вызван /start'
    print(text)
    update.message.reply_text(text)


def word_calculation(bot, update):
    numbers_dict = {'ноль': 0, 'один': 1, 'два': 2, 'три': 3, 'четыре': 4, 'пять': 5, 'шесть': 6,
     'семь': 7, 'восемь': 8, 'девять': 9, 'десять': 10, 'одиннадцать': 11, 'двенадцать': 12,
      'тринадцать': 13, 'четырнадцать': 14, 'пятнадцать': 15, 'шестнадцать': 16, 'семнадцать': 17,
       'восемнадцать': 18, 'девятнадцать': 19, 'двадцать': 20, 'тридцать': 30, 'сорок': 40, 'пятьдесят': 50,
        'шестьдесят': 60, 'семьдесят': 70, 'восемьдесят': 80, 'девяносто': 90, 'сто': 100, 'двести': 200,
         'триста': 300, 'четыреста': 400, 'пятьсот': 500, 'шестьсот': 600, 'семьсот': 700, 'восемьсот': 800,
          'девятьсот': 900, 'тысяча': 1000}

    signs = [' минус ', ' плюс ', ' умножить на ', ' разделить на ']


    def word_to_number_int(string):
        result = 0
        for elem in string.split(' '):
            result += numbers_dict[elem]
        return result


    def word_to_number_float(string):
        result = 0
        main_part_str = re.split(' и ', string)[0]
        decimal_part_str = re.split(' и ', string)[1]

        main_part = word_to_number_int(main_part_str)
        decimal_part = word_to_number_int(decimal_part_str)

        result = float('{}.{}'.format(str(main_part), str(decimal_part)))
        return result

    # сообщение пользователя начинается с фразы "Сколько будет ", 
    # поэтому игнорируем первые 14 символов
    user_text = update.message.text[14:]

    for elem in signs:
        if elem in user_text:
            sep_sign = elem

    one_str = re.split(sep_sign, user_text)[0]
    two_str = re.split(sep_sign, user_text)[1]

    if ' и ' in one_str:
        one = word_to_number_float(one_str)
    else:
        one = word_to_number_int(one_str)

    if ' и ' in two_str:
        two = word_to_number_float(two_str)
    else:
        two = word_to_number_int(two_str)


    if sep_sign == ' минус ':
        answer = one - two
    elif sep_sign == ' плюс ':
        answer = one + two
    elif sep_sign == ' умножить на ':
        answer = one * two
    elif sep_sign == ' разделить на ':
        answer = one / two

    print(answer)
    update.message.reply_text(answer)


def main():
    mybot = Updater(key, request_kwargs=PROXY)


    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(MessageHandler(Filters.text, word_calculation))


    mybot.start_polling()
    mybot.idle()

main()
