import re
import requests
from bs4 import BeautifulSoup as bs
import time
import logging


logging.basicConfig(filename='Lab.log', level=logging.INFO)

page = requests.get('https://en.wikipedia.org/wiki/Special:Random')
page2 = requests.get('https://en.wikipedia.org/wiki/Special:Random')

link_part = 'https://en.wikipedia.org'
visited = set()
mark = False
path = {}
print(page.url)
print(page2.url)


def parser(link, search, level):
    global mark
    level += 1
    print(level)
    link2 = bs(link.text, 'html.parser').select('p a')
    if len(re.findall('/' + '/'.join(str(search.url).split('/')[3:]), link.text)):
        mark = True
        print('Путь найден')
    for lin in link2:
        if mark:
            path[str(level)] = link.url
            break
        try:
            a = lin.attrs['title']
            a = lin.attrs['href']
            if '.png'.__contains__(str(lin).lower()) or '.jpeg'.__contains__(str(lin).lower()):
                raise KeyError
        except KeyError:
            link2.remove(lin)
            continue
        if '{}{}'.format(level, lin.attrs['href']) in visited:
            continue
        else:
            visited.add('{}{}'.format(level, lin.attrs['href']))

        if level == 10:
            if mark is False:
                break
        else:

            if 'http'.__contains__(str(lin.attrs['href'])):
                try:
                    parser(requests.get(lin.attrs['href']), search, level)
                except requests.exceptions.ConnectionError:
                    time.sleep(0.05)
                    try:
                        parser(requests.get(lin.attrs['href']), search, level)
                    except requests.exceptions.ConnectionError:
                        continue

            else:
                try:
                    parser(requests.get('{}{}'.format(link_part,lin.attrs['href'])),search, level)
                except requests.exceptions.ConnectionError:
                    time.sleep(0.05)
                    try:
                        parser(requests.get('{}{}'.format(link_part, lin.attrs['href'])), search, level)
                    except requests.exceptions.ConnectionError:
                        continue
    link.close()


parser(page, page2, 0)
logging.info('Первый путь:')
for i in range(10):
    if path.get(str(i)):
        logging.info(path.get(str(i)))
logging.info(page2.url)
logging.info("\n \n \n")
mark = False
visited.clear()
path.clear()
parser(page2, page, 0)
logging.info("Второй путь:")
for i in range(10):
    if path.get(str(i)):
        logging.info(path.get(str(i)))

logging.info(page.url)
logging.info("\n \n \n")