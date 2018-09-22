from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from api_key import TELEGRAM_BOT_TOKEN

import logging
import random

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot3_cities.log'
                    )

PROXY = {'proxy_url': 'socks5://t2.learn.python.ru:1080',
    'urllib3_proxy_kwargs': {'username': 'learn', 'password': 'python'}}

def greet_user(bot, update):
    text = 'Вызван /start'
    print(text)
    update.message.reply_text(text)

def print_city(city_dict, user_city, key, key_last):
    try:
        city_dict[key].remove(user_city)
    except ValueError:
        print('Я не знаю такой город или его уже называли, попробуйте еще раз')
        return 'Я не знаю такой город или его уже называли, попробуйте еще раз'


    for elem in city_dict[key]:
        if elem.startswith(user_city[-1].upper()):
            print(elem)
            city_dict[key_last] = elem
            city_dict[key].remove(elem)
            return '{}, ваш ход'.format(elem)

    city_dict.clear()
    print('Я сдаюсь')
    return 'Я сдаюсь'
    
def cities_play(bot, update, user_data):

    key = 'cities'
    key_last = 'last_city'
    with open('cities.txt', 'r', encoding='utf-8') as f:
        cities_list = f.readlines()
        cities_list = [elem.rstrip('\n') for elem in cities_list]

    user_city = update.message.text[8:]
    user_data[key] = cities_list
    random.shuffle(user_data[key])

    update.message.reply_text('Добро пожаловать в режим игры в города! Следующий город можете вводить без команды /goroda')
    
    bot_answer = print_city(user_data, user_city, key, key_last)
    update.message.reply_text(bot_answer)
        

def cities_handler(bot, update, user_data):
    key = 'cities'
    key_last = 'last_city'
    
    user_city = update.message.text
    if user_city == 'Я сдаюсь':
        print('До встречи!')
        update.message.reply_text('До встречи!')
        user_data.clear()
        return

    if user_city[0].lower() == user_data[key_last][-1]:

        bot_answer = print_city(user_data, user_city, key, key_last)
        update.message.reply_text(bot_answer)

    else:
        print('Ты вводишь что-то не то')
        update.message.reply_text('Ты вводишь что-то не то')
        return


def main():
    mybot = Updater(TELEGRAM_BOT_TOKEN, request_kwargs=PROXY)


    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler('goroda', cities_play, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.text, cities_handler, pass_user_data=True))


    mybot.start_polling()
    mybot.idle()

main()
