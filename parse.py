from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError 
from bs4 import BeautifulSoup
import csv
import re

articlesList = [['Автор','Имя статьи','Тема','Аннотация','Ссылка на статью','Содержимое']]

url = "https://habr.com/ru/search/page"
urlParamsStr="q=blockchain&target_type=posts&order=relevance"
pagesCount = 3
def parseArticle(article):
    list = []
    list.append(article.find(class_='tm-user-info__username').get_text().strip())
    list.append(article.find(class_='tm-article-snippet__title').get_text().strip())
    list.append(article.find(class_='tm-article-snippet__hubs').get_text().strip())
    list.append(article.find(class_='article-formatted-body').get_text().strip())
    list.append(article.find('a',class_='tm-article-snippet__title-link')['href'])
    return list

for pageNumber in range(pagesCount):
    try:
        html = urlopen(url+str(pageNumber+1)+'/?'+urlParamsStr)
    except HTTPError as e:
        print("The server returned an HTTP error")
    except URLError as e:
        print("The server could not be found!")
    else:
        bs = BeautifulSoup(html, 'html.parser')
        articles = bs.find_all(class_='tm-articles-list__item')
        for article in articles:
            data = parseArticle(article)
            try:
                 page = urlopen('https://habr.com'+data[4])
            except HTTPError as e:
                print("The server returned an HTTP error")
            except URLError as e:
                print("The server could not be found!")
            else:
                page_bs = BeautifulSoup(page, 'html.parser')
                article_content = page_bs.find(class_='article-formatted-body').get_text().strip()
                article_content = re.sub(r'\<[^>]*\>', '', article_content)
                data.append(re.sub("^\s+|\n|\r|\s+$", '', article_content))
                articlesList.append(data)

            
with open('parsed.csv', mode="w",  errors='replace') as File:  
    file_writer = csv.writer(File, delimiter = ";", lineterminator="\n")
    file_writer.writerows(articlesList)
        