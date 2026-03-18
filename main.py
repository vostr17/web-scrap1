from sys import flags

import requests
import bs4
from pprint import pprint
import lxml
import re

""" Проверяет список (raw_list) на наличие ключевых слов 
(список key_words) и возвращает список с результатом проверки (result_list)"""
def search_keywords(key_words, raw_list):
    result_list = []
    for word in key_words:
        for result in raw_list:
            for title in re.findall(r'\b(\w+)', result[0]):
                if title.lower() == word:
                    if result not in result_list:
                        result_list.append(result)
            for tags in result[3]:
                # Разбиваем список тэгов на строки
                for tag in re.findall(r'\b(\w+)', tags):
                    if tag.lower() == word:
                        if result not in result_list:
                            result_list.append(result)
            for abstracts in result[4]:
                # Разбиваем список абстракта на строки
                for abstract in re.findall(r'\b(\w+)', abstracts):
                    # Разбиваем строки на слова
                    if abstract.lower() == word:
                        if result not in result_list:
                            result_list.append(result)
    return result_list


url = 'https://habr.com/ru/articles/'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 YaBrowser/25.12.0.0 Safari/537.36'}
response = requests.get(url, headers=headers)


KEYWORDS = ['дизайн', 'фото', 'web', 'python']

article_title = ''
article_url = ''
article_time = ''
article_tags = []
article_abstract = []
result1 = []
result2 = []

s1 = ''

soup = bs4.BeautifulSoup(response.text, 'lxml')


#Ищем в коде страницы блок статья (article)
articles = soup.find_all('article', attrs={'class': 'tm-articles-list__item'})
for article in articles:
    # Находим и присваиваем название статьи (article_title)
    title = article.find('h2', attrs={'class': 'tm-title tm-title_h2'})
    article_title = title.text
    result1.append(article_title)

    # Находим и присваиваем адрес статьи (article_url)
    article_url = 'https://habr.com' + title.find('a')['href']
    result1.append(article_url)

    # Находим и присваиваем дату и время выхода статьи
    article_time = article.find('time')['title'].split(',')[0]
    result1.append(article_time)

    #Находим и присваиваем теги статьи (article_tags)
    tags = article.find('div', attrs={'class': 'tm-publication-hubs'})
    t1 = tags.find_all('a')
    if t1:
        for t in t1:
            t2 = t.find_all('span')
            tag = t2[0].text
            article_tags.append(tag)
        result1.append(article_tags)

    #Находим и присваиваем абстракт статьи (article_abstract)
    abstract = article.find('div', attrs={'class': 'article-formatted-body article-formatted-body article-formatted-body_version-2'})
    a_abstract = abstract.find_all('p')
    for a in a_abstract:
        s1 += a.text.strip()
    article_abstract.append(s1)
    s1 = ''
    result1.append(article_abstract)

    result2.append(result1)
    article_title = ''
    article_url = ''
    article_tags = []
    article_abstract = []
    result1 = []


result1 = []
result3 = []

result1 = search_keywords(KEYWORDS, result2)

# Вывод результата в формате <дата> - <название статьи> - <ссылка>
for article in result1:
    result3 = [f'{article[2]} - {''.join(article[0])} - {article[1]}'
            for article in result1]
print(*result3, sep='\n')








