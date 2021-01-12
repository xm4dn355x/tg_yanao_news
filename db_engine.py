# -*- coding: utf-8 -*-
########################################################################
#                                                                      #
# Методы работы с БД                                                   #
#                                                                      #
# MIT License                                                          #
# Copyright (c) 2021 Michael Nikitenko                                 #
#                                                                      #
########################################################################


import psycopg2
from psycopg2.extras import DictCursor

from bot_config import DB_NAME, DB_HOST, DB_USER, DB_PASS


# DB connection and cursor
conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
cursor = conn.cursor(cursor_factory=DictCursor)


def get_all_db_data() -> list:
    """Возвращает все строки из базы"""
    cursor.execute('''SELECT * FROM news''')
    res = cursor.fetchall()
    return res


def insert_data(title: str, url: str, source: str) -> None:
    """Получает заголовок ссылку и источник статьи и записывает их в БД"""
    cursor.execute(
        f'''INSERT INTO news (title, url, author, status) VALUES ('{title}', '{url}', '{source}', FALSE )'''
    )
    conn.commit()


def update_data(url: str) -> None:
    """Меняет статус опубликованности поста на True"""
    cursor.execute(f'''UPDATE news SET status=TRUE WHERE url='{url}';''')
    conn.commit()


def delete_data(url: str) -> None:
    """Получает url новости и удаляет её из базы"""
    cursor.execute(f'''DELETE FROM news WHERE url='{url}';''')
    conn.commit()


if __name__ == '__main__':
    print('db_engine')
    insert_data('title', 'url', 'source')
    rows = get_all_db_data()
    for row in rows:
        print(row)
    print("uhybjhbbkbj")
    update_data('url')
    rows = get_all_db_data()
    for row in rows:
        print(row)
    print("uhybjhbbkbj")
    delete_data('url')
    rows = get_all_db_data()
    for row in rows:
        print(row)
    print("uhybjhbbkbj")
