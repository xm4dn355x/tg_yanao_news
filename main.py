# -*- coding: utf-8 -*-
########################################################################
#                                                                      #
# Парсер новостей, публикующий свежие новости в телеграм-канал         #
#                                                                      #
# BSD 3-Clause License                                                 #
# Copyright (c) 2021 Michael Nikitenko                                 #
#                                                                      #
########################################################################


from datetime import datetime
from random import randint
from time import sleep

from telegram import Bot
from telegram.utils.request import Request

from bot_config import API_TOKEN, ADMIN_ID, CHANNEL_ID
from db_engine import update_data, insert_data
from news_parser import get_current_news


request = Request(connect_timeout=3)
bot = Bot(request=request, token=API_TOKEN)


def log_error(f):
    """Отлавливание ошибок телоеграм-бота"""
    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            error = f'ERROR {e} in '
            print(error)
            update = args[0]
            if update and hasattr(update, 'message'):
                bot.send_message(chat_id=ADMIN_ID, text=error)
            raise e
    return inner


@log_error
def post_new(post: dict):
    """Принимает тело поста и постит его в телеграм канал"""
    insert_data(post['title'], post['url'], post['author'])
    bot.send_message(chat_id=CHANNEL_ID, text=generate_message_text(post), parse_mode='html')
    update_data(post['url'])


def generate_message_text(post: dict) -> str:
    """Принимает тело поста и генерирует на его основе текст поста"""
    return f'<a href="{post["url"]}">{post["title"]}</a>\n\n#{post["author"]}'


def update_channel_loop():
    """Бесконечный цикл публикующий новости в телеграм канале"""
    while True:
        try:
            current_news = get_current_news()
            for post in current_news:
                print(f'{datetime.now()} {post}')
                post_new(post)
                sleep(5)
            sleep(randint(800, 1000))
        except AttributeError:
            print(f'{datetime.now()} Каптча ебаная')
            sleep(randint(800, 1000))


if __name__ == '__main__':
    print('Телеграм бот: Парсер Яндекс новостей')
    update_channel_loop()
