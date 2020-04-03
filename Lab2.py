import requests
from bs4 import BeautifulSoup as bs4
import re
import time
import logging


logging.basicConfig(filename='Lab2.log', level=logging.INFO)


def update_page(timer):
    page = requests.get('https://lenta.ru/parts/news/')
    parser(page,
           timer)


news = []
url_first_part = 'https://lenta.ru'

search1 = r'[демо\w+\s]+[\пар\w+\s]+[\сша\s]'
search2 = r'[респ\w+\s]+[\пар\w+\s]+[\сша\s]'

visited = set()


def parser(page, timer):
    page_info = bs4(page.text, 'html.parser')
    page_info = page_info.select("h3 a")
    for i in page_info:
        if i.attrs['href'] in visited:
            continue
        else:
            visited.add(i.attrs['href'])
        if str(i.attrs['href']).__contains__("http"):
            url = i.attrs['href']
        else:
            url = '{}{}'.format(url_first_part, i.attrs["href"])
        new_page = requests.get(url)
        try:
            title = str(bs4(new_page.text, 'html.parser').select_one('h1')).replace('>','+').replace('<','+').split("+")[2]
        except IndexError:
            continue
        articles = bs4(new_page.text, 'html.parser').select('p')
        for article in articles:
            if not re.search('демократ\w', str(article)) or re.search("республикц\w", str(article)) or re.search('дем\w+ пар\w+ сша', str(article)) or re.search('рес\w+ пар\w+ сша', str(article)):
                logging.info("Title: {} \n Url: {} \n \n".format(title, url))
                break

    if timer - 300 >= 0:
        time.sleep(300)
        update_page(timer-300)


update_page(86400)
logging.info('Вот все найденные новости')