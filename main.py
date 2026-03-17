import requests
import bs4
from pprint import pprint
import lxml


url = 'https://habr.com/ru/articles/page3/'

response = requests.get(url)


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
    article_time = article.find('time')['title']
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

for word in KEYWORDS:
    for result in result2:
        for title in result[0]:
            if word in title.lower():
                if result not in result1:
                    result1.append(result)
        for tag in result[3]:
            if word in tag.lower():
                if result not in result1:
                    result1.append(result)
        for abstract in result[4]:
            if word in abstract.lower():
                if result not in result1:
                    result1.append(result)


print(len(result1))
pprint(result1)






