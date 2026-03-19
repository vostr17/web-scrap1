import sys
from sys import flags

import requests
import bs4
from pprint import pprint
import lxml
import re
import time


""" Ищет ключевые слова (список keywords) в тексте статьи по ссылке article_url"""
def is_keywords_in_article(key_words, article_url):
    article_text = ''
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 YaBrowser/25.12.0.0 Safari/537.36'}
    try:
        response = requests.get(article_url, headers=headers)
    except requests.RequestException as e:
        print(f'Ошибка при запросе: {e}')
        sys.exit(0)

    soup = bs4.BeautifulSoup(response.text, 'lxml')
    text = soup.find_all('p')

    for a in text:
        article_text += a.text.strip()

    for word in key_words:
        for word_i in re.findall(r'\b(\w+)', article_text):
                if word_i.lower() == word:
                    return True
    return False






""" Загрузка страницы со статьями """
url = 'https://habr.com/ru/articles/'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 YaBrowser/25.12.0.0 Safari/537.36'}
try:
    response = requests.get(url, headers=headers)
except requests.RequestException as e:
    print(f'Ошибка при запросе: {e}')
    sys.exit(0)


KEYWORDS = ['дизайн', 'фото', 'web', 'python']

article_title = ''
article_url = ''
article_time = ''
result_article = [] # Список с данными одной найденной статьи
result_articles = [] # Список со списками всех найденных статей

s1 = ''

soup = bs4.BeautifulSoup(response.text, 'lxml')


#Ищем в коде страницы блок статья (article)
articles = soup.find_all('article', attrs={'class': 'tm-articles-list__item'})
for article in articles:
    # Находим и присваиваем дату и время выхода статьи
    article_time = article.find('time')['title'].split(',')[0]
    result_article.append(article_time)

    # Находим и присваиваем название статьи (article_title)
    article_title = article.find('h2', attrs={'class': 'tm-title tm-title_h2'})
    result_article.append(article_title.text)

    # Находим и присваиваем адрес статьи (article_url)
    article_url = 'https://habr.com' + article_title.find('a')['href']
    result_article.append(article_url)

    result_articles.append(result_article)
    result_article = []


result3 = []
for article in result_articles:
    if is_keywords_in_article(KEYWORDS, article[2]):
        result3.append(article)
    else:
        print(f'Cтатья по ссылке {article[2]} не содержит ключевых слов')
    time.sleep(10)
print(*result3, sep='\n')






