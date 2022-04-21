import time 
import json
from email import header
from msilib.schema import File
from unittest import result
from webbrowser import get
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

result_list = []


def parse_site(rubric, url_req):
    print("-------------------------------------------")

    request = requests.get(url_req, headers={'User-Agent': UserAgent().chrome}) 
    data = json.loads(request.text)
    iteration = 1
   
    if rubric == "Спорт":   
        for item in data['items']:
            article = item['html']
            soup = BeautifulSoup(article,"lxml")
            title = soup.find(class_="item__link").text.strip()
            url_site = soup.find(class_="item__link").get("href")
            result_list.append(title)
            result_list.append(url_site)
            print("(+) ARTICLE CARD №",iteration, "IS READY")
            iteration+=1
    else:
        article = data['html']
        soup = BeautifulSoup(article,"lxml")
        site = soup.find_all(class_="item__link")
        for data in site:
            result_list.append(data.text.strip())
            result_list.append(data.get("href"))
            print("(+) ARTICLE CARD №", iteration, "IS READY")
            iteration+=1

    print("-------------------------------------------")

    
def choice_rubric(rubric, varios_get_news):
    current_data = int(time.time())
    if varios_get_news == "Текущие новости":
        limit = 5
    else:
        limit = 1

    if rubric == "Политика":
        url_req = f"https://www.rbc.ru/v10/ajax/get-news-by-filters/?category=politics&offset=0&limit={limit}"
    elif rubric == "Экономика":
        url_req = f"https://www.rbc.ru/v10/ajax/get-news-by-filters/?category=economics&offset=0&limit={limit}"
    elif rubric == "Спорт":
        url_req = f"https://sportrbc.ru/ajax/get-news-feed-short/project/sport/lastDate/{current_data}/limit/{limit}"
    parse_site(rubric, url_req)
    
if __name__ == '__main__':
   choice_rubric("Политика","Текущие новости")
    
