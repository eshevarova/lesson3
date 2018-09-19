from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from api_key import key

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


def cities_play(bot, update, user_data):
    key = update.message.chat.id
    key_last = key + 1
    with open('cities.txt', 'r', encoding='utf-8') as f:
        cities_list = f.readlines()
        cities_list = [elem.rstrip('\n') for elem in cities_list]

    user_city = update.message.text[8:]
    user_data[key] = cities_list
    random.shuffle(user_data[key])

    update.message.reply_text('Добро пожаловать в режим игры в города! Следующий город можете вводить без команды /goroda')
    
    try:
        user_data[key].remove(user_city)
    except ValueError:
        print('Я не знаю такой город, попробуйте еще раз')
        update.message.reply_text('Я не знаю такой город, попробуйте еще раз')
        return

    length = 0

    for elem in user_data[key]:
        length += 1
        if elem.startswith(user_city[-1].upper()):
            print(elem)
            update.message.reply_text('{}, ваш ход'.format(elem))
            user_data[key_last] = elem
            user_data[key].remove(elem)
            break
        elif length == len(user_data[key]):
            print('Я сдаюсь')
            update.message.reply_text('Я сдаюсь')
            user_data.clear()
            return
        

def cities_handler(bot, update, user_data):
    key = update.message.chat.id
    key_last = key + 1
    
    user_city = update.message.text
    if user_city == 'Я сдаюсь':
        print('До встречи!')
        update.message.reply_text('До встречи!')
        user_data.clear()
        return

    if user_city[0].lower() == user_data[key_last][-1]:

        try:
            user_data[key].remove(user_city)
        except ValueError:
            print('Я не знаю такой город или вы его уже называли, попробуйте еще раз')
            update.message.reply_text('Я не знаю такой город или вы его уже называли, попробуйте еще раз')
            return

        length = 0

        for elem in user_data[key]:
            length += 1
            if elem.startswith(user_city[-1].upper()):
                print(elem)
                update.message.reply_text('{}, ваш ход'.format(elem))
                user_data[key_last] = elem
                user_data[key].remove(elem)
                break
            elif length == len(user_data[key]):
                print('Я сдаюсь')
                update.message.reply_text('Я сдаюсь')
                user_data.clear()
                return

    else:
        print('Ты вводишь что-то не то')
        update.message.reply_text('Ты вводишь что-то не то')
        return


def main():
    mybot = Updater(key, request_kwargs=PROXY)


    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler('goroda', cities_play, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.text, cities_handler, pass_user_data=True))


    mybot.start_polling()
    mybot.idle()

main()
