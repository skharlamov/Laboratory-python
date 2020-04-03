import re
import requests
from bs4 import BeautifulSoup as bs

file = open('access.log', 'r')
types = {'GET': list(), "HEAD": list(), "POST": list(), 'OPTIONS': list(), 'PROPFIND': list(), 'CONNECT':list()}
ips = {}
check_this = set()
types_list = ['GET', 'POST', 'HEAD', 'OPTIONS', 'PROPFIND', 'CONNECT']
tops = {'5': list(), '4': list(), '3': list(), '2': list(), '1': list(), '0':list()}
requ = list()


# сортировка запросов по ip и типу запроса
def sort_request(request):
    mark_type = False
    for typ in types_list:
        if len(re.findall(typ, request)) > 0:
            types[typ].append(request)
            mark_type = True
            break
    if not mark_type:
        check_this.add(request)
    if re.findall('\d+.\d+.\d+.\d+',i)[0] not in ips.keys():
        ips[re.findall('\d+.\d+.\d+.\d+', i)[0]] = list()
    ips[re.findall('\d+.\d+.\d+.\d+', i)[0]].append(i)


# проверка на схожеть тела запроса с другими запросами от других ip
def fifth_check(request):
    request_body = request.split(']')[1]
    request_ip = re.findall('\d+.\d+.\d+.\d+', request)[0]
    number = 0
    for key in ips.keys():
        for req in ips[key]:
            if request_body in req and not request_ip in req:
                number = 1
                return number

    return number


# проверка на наличие ссылки, откуда совершен был переход
def fourth_check(request):
    if re.search('http+', request):
        number = 0
    else:
        number = 1
    number += fifth_check(request)
    return number


# имеется ли у тела тип запроса
def third_check(request):
    if request in check_this:
        number = 1
    else:
        number = 0
    number += fourth_check(request)
    return number


# Проверка на наличие протока http
def second_check(request):
    if re.search('/HTTP/\d.\d', request):
        number = 1
    else:
        number = 0
    number += third_check(request)
    return number


# Проверка на наличие данных о браузере
def first_check(request):
    if not re.search('Mozilla/5.0', request):
        number = 1
    else:
        number = 0
    number += second_check(request)
    tops[str(number)].append(request)


for i in file.readlines():
    if not '195.101.2.195'.__contains__(i):
        sort_request(i)
        requ.append(i)


for i in requ:
    first_check(i)
for i in range(4):
    number = 0
    for g in tops[str(5-i)]:
        if number == 50:
            break
        print('Степень подозрительности {} из 5'.format(5-i))
        print('{} \n \n'.format(g))
        number += 1