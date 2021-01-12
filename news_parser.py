# -*- coding: utf-8 -*-
########################################################################
#                                                                      #
# Сам парсер Яндекс-новостей                                           #
#                                                                      #
# MIT License                                                          #
# Copyright (c) 2021 Michael Nikitenko                                 #
#                                                                      #
########################################################################


from bs4 import BeautifulSoup
import requests

from db_engine import get_all_db_data


URL = 'https://newssearch.yandex.ru/yandsearch?text=%D1%8F%D0%BC%D0%B1%D1%83%D1%80%D0%B3+%7C+%D1%85%D0%B0%D1%80%D1%8E' \
      '%D1%87%D0%B8+%7C+%D0%BE%D0%B1%D1%81%D0%BA+%7C+%D0%B0%D0%BA%D1%81%D0%B0%D1%80%D0%BA%D0%B0+%7C+%D1%85%D0%B0%D1%8' \
      '0%D0%BF+%7C+%D0%B3%D1%83%D0%B1%D0%BA%D0%B8%D0%BD%D1%81%D0%BA+%7C+%D0%B1%D0%BE%D0%B2%D0%B0%D0%BD%D0%B5%D0%BD%D0' \
      '%BA%D0%BE%D0%B2+%7C+%D0%BD%D0%B0%D0%B4%D1%8B%D0%BC+%7C+%D0%BF%D1%80%D0%B8%D1%83%D1%80%D0%B0%D0%BB%D1%8C%D1%81%' \
      'D0%BA+%7C+%D0%BF%D1%83%D1%80%D0%BE%D0%B2%D1%81%D0%BA+%7C+%D1%88%D1%83%D1%80%D1%8B%D1%88%D0%BA%D0%B0%D1%80+%7C+' \
      '%D0%BA%D1%80%D0%B0%D1%81%D0%BD%D0%BE%D1%81%D0%B5%D0%BB%D1%8C%D0%BA%D1%83%D0%BF+%7C+%D1%8F%D0%BC%D0%B0%D0%BB%D1' \
      '%8C%D1%81%D0%BA%D0%B8%D0%B9+%7C+%D1%81%D0%B0%D0%BB%D0%B5%D1%85%D0%B0%D1%80%D0%B4+%7C+%D1%83%D1%80%D0%B5%D0%BD%' \
      'D0%B3%D0%BE%D0%B9+%7C+%D0%BD%D0%BE%D1%8F%D0%B1%D1%80%D1%8C%D1%81%D0%BA+%7C+%D1%82%D0%B0%D0%B7%D0%BE%D0%B2%D1%8' \
      '1%D0%BA+%7C+%D1%8F%D0%BC%D0%B0%D0%BB+%7C+%D0%B7%D0%BB%D0%B5%D0%BD%D0%BA%D0%BE+%7C+%D0%BD%D0%B5%D0%B5%D0%BB%D0%' \
      'BE%D0%B2+%7C+%D0%BB%D0%B0%D0%B1%D1%8B%D1%82%D0%BD%D0%B0%D0%BD%D0%B3%D0%B8+%7C+%D0%BC%D1%83%D1%80%D0%B0%D0%B2%D' \
      '0%BB%D0%B5%D0%BD%D0%BA%D0%BE+%7C+%D0%BA%D1%83%D0%BF%D1%80%D0%B0%D0%B2%D0%B0+%7C+%D1%81%D0%B0%D0%B1%D0%B5%D1%82' \
      '%D1%82+%7C+%D0%BD%D0%B0%D0%B4%D1%8B%D0%BC%D1%81%D0%BA%D0%B8%D0%B9+%7C+%D0%BF%D1%80%D0%B8%D1%83%D1%80%D0%B0%D0%' \
      'BB%D1%8C%D1%81%D0%BA%D0%B8%D0%B9+%7C+%D0%BF%D1%83%D1%80%D0%BE%D0%B2%D1%81%D0%BA%D0%B8%D0%B9+%7C+%D1%88%D1%83%D' \
      '1%80%D1%8B%D1%88%D0%BA%D0%B0%D1%80%D1%81%D0%BA%D0%B8%D0%B9+%7C+%D0%BA%D1%80%D0%B0%D1%81%D0%BD%D0%BE%D1%81%D0%B' \
      '5%D0%BB%D1%8C%D0%BA%D1%83%D0%BF%D1%81%D0%BA%D0%B8%D0%B9+%7C+%D1%8F%D0%BC%D0%B0%D0%BB%D1%8C%D1%81%D0%BA%D0%B8%D' \
      '0%B9+%7C+%D1%82%D0%B0%D0%B7%D0%BE%D0%B2%D1%81%D0%B8%D0%B9+%7C+%D0%B0%D1%80%D1%82%D1%8E%D1%85%D0%BE%D0%B2+%7C+%' \
      'D1%8F%D0%BD%D0%B0%D0%BE+%7C+%D1%8F%D0%BC%D0%B0%D0%BB%D0%BE&rpt=nnews2&rel=tm'


def get_html(url: str) -> str:
    """Получает URL и возвращает тело HTML-документа"""
    return requests.get(url=url, headers={'User-Agent': 'Custom'}).text


def get_mock_html(filename: str) -> str:
    """Мок-метод, который возвращает тело HTML документа из заранее сохранённого"""
    with open(filename, mode='r', encoding='utf-8') as file:
        res = file.read()
    return res


def get_posts(html: str) -> list:
    """Достаёт новостные посты"""
    soup = BeautifulSoup(html, 'lxml')
    posts_container = soup.find('div', class_='page-content__left')
    posts = posts_container.findAll('li', class_='search-item')
    res = []
    for post in posts:
        header = post.find('div', class_='document__title')
        title = header.text.replace('\t', '').replace('\n', '').replace('     ', '').strip()
        url = header.find('a', class_='link').get('href')
        author = post.find('div', class_='document__provider-name').text
        res.append({
            'url': url,
            'title': title,
            'author': author,
        })
    return res


def get_current_news() -> list:
    """Сверяет спарсенные новости с новостями в БД и возвращает только свежие новости"""
    db_data = get_all_db_data()
    parsed_news = get_posts(get_mock_html(url=URL))
    # parsed_news = get_posts(get_mock_html('test.html'))
    res = []
    for parsed in parsed_news:
        is_not_in_db = True
        for db in db_data:
            if db['title'] == parsed['title']:
                is_not_in_db = False
        if is_not_in_db:
            res.append(parsed)
    return res


if __name__ == '__main__':
    print('news parser')
    # html = get_mock_html('test.html')
    # html = get_html(url=URL)
    # posts = get_posts(html)
    # for post in posts:
    #     print(post)
    news = get_current_news()
    for post in news:
        print(post)
