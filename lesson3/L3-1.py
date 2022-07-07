# Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию,
# которая будет добавлять только новые вакансии/продукты в вашу базу.
from builtins import print
from datetime import date
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

Header = {'User-Agent':
          'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 '
          'Safari/537.36 OPR/86.0.4363.59 (Edition Yx 05)'}


def page_parsing_hh(url_hh, host, param, vacancys):

    def parsing_payment_hh(payment: str, sep='\u202f'):
        p_text = payment
        min_pay, max_pay, *cur_pay = p_text.replace(sep, '').replace('–', '').split()

        min_pay = int(min_pay) if min_pay.isdigit() else None
        max_pay = int(max_pay) if max_pay.isdigit() else None
        cur_pay = ''.join(cur_pay) if isinstance(cur_pay, list) else cur_pay

        return min_pay, max_pay, cur_pay

    class_vacancy = 'vacancy-serp-item__layout'
    class_payment = 'vacancy-serp__vacancy-compensation'
    class_employer = 'vacancy-serp__vacancy-employer'
    class_location = 'vacancy-serp__vacancy-address'
    class_next = 'pager-next'

    session = requests.Session()
    response = session.get(url_hh, params=param, headers=Header)

    if not response.ok:
        return False

    dom = BeautifulSoup(response.text, 'html.parser')

    for i in dom.find_all('div', {'class': class_vacancy}):

        name_link = i.find('a')
        zp = i.find('span', {'data-qa': class_payment})
        emplr = i.find('a', {'data-qa': class_employer})

        name = name_link.text
        link = name_link.get('href')
        employer = emplr.text if emplr is not None else ''
        location = i.find('div', {'data-qa': class_location}).text

        if zp is not None:
            min_zp, max_zp, currency = parsing_payment_hh(zp.text)
        else:
            min_zp, max_zp, currency = None, None, ''

        v = {'_id': hash(link),
             'name': name,
             'min_zp': min_zp,
             'max_zp': max_zp,
             'currency': currency,
             'link': link,
             'host': host,
             'employer': employer,
             'location': location,
             'update': str(date.today())}

        if vacancys.find_one({'_id': v.get('_id')}) is None:
            vacancys.insert_one(v)
        else:
            vacancys.replace_one({'_id': v.get('_id')}, v)

    return dom.find('a', {'data-qa': class_next}) is not None


def page_parsing_sj(url_hh, host, param, vacancys):

    def parsing_payment_sj(payment: str, min_pay=None, max_pay=None, cur_pay='', sep='\xa0'):
        p_text = payment.strip()
        if p_text[0:2] in 'от':
            s = p_text[2:].rpartition(sep)
            min_pay, cur_pay = int(s[0].replace(sep, '')), s[2]
        elif p_text[0:2] in 'до':
            s = p_text[2:].rpartition(sep)
            max_pay, cur_pay = int(s[0].replace(sep, '')), s[2]
        elif '—' in p_text:
            s = p_text.split('—')
            min_pay, max_pay = int(s[0].replace(sep, '')), int(s[1].rpartition(sep)[0].replace(sep, ''))
            cur_pay = s[1].rpartition(sep)[2]
        elif p_text[0].isdigit():
            s = p_text.rpartition(sep)
            min_pay, cur_pay = int(s[0].replace(sep, '')), s[2]
            max_pay = min_pay

        return min_pay, max_pay, cur_pay

    class_vacancy = '_2J3hU ZsUty GSXRd MgbFi'
    class_payment = '_1Fg5m _3ndp2 _1_dH8 _1oy1C _2eYAG _10_Fa _21QHd _36Ys4 _9Is4f'
    class_employer = '_3nMqD f-test-text-vacancy-item-company-name MjtUU _21QHd _36Ys4 _9Is4f _39z8N'
    class_location = 'f-test-text-company-item-location CJVN9 _21QHd _3lGwd _9Is4f'
    class_next = '_1IHWd _6Nb0L _37aW8 _3187U f-test-button-dalshe f-test-link-Dalshe'

    session = requests.Session()
    response = session.get(url_hh, params=param, headers=Header)

    if not response.ok:
        return False

    dom = BeautifulSoup(response.text, 'html.parser')

    for i in dom.find_all('div', {'class': class_vacancy}):
        name_link = i.find('a')
        zp = i.find('span', {'class': class_payment})
        emplr = i.find('span', {'class': class_employer})

        name, link = name_link.text, name_link.get('href')
        employer = emplr.find_next('a').text if emplr is not None else ''
        location = i.find('span', {'class': class_location}).text

        if zp is not None:
            min_zp, max_zp, currency = parsing_payment_sj(zp.text)
        else:
            min_zp, max_zp, currency = None, None, ''

        v = {'_id': hash(link),
             'name': name,
             'min_zp': min_zp,
             'max_zp': max_zp,
             'currency': currency,
             'link': link,
             'host': host,
             'employer': employer,
             'location': location,
             'update': str(date.today())}

        if vacancys.find_one({'_id': v.get('_id')}) is None:
            vacancys.insert_one(v)
        else:
            vacancys.replace_one({'_id': v.get('_id')}, v)

    return dom.find('a', {'class': class_next}) is not None


def parsing_hh(vac_name, max_page, vacancys):
    doit, start, host = True, 0, 'hh.ru'

    url_hh = f'https://{host}/search/vacancy'
    param = {'search_field': ['name', 'company_name'],
             'text': vac_name,
             'from': 'suggest_post',
             'items_on_page': 20,
             'page': start}

    while doit:
        if __name__ == '__main__':
            print(f'{host} page#{start}')

        doit = page_parsing_hh(url_hh, host, param, vacancys) and max_page > start+1
        start += 1


def parsing_sj(vac_name, max_page, vacancys):
    doit = True
    start = 1
    host = 'russia.superjob.ru'
    url_hh = f'https://{host}/vacancy/search/'

    while doit:
        if __name__ == '__main__':
            print(f'{host} page#{start}')

        param = {'keywords': vac_name, 'page': start}
        doit = page_parsing_sj(url_hh, host, param, vacancys) and max_page > start - 1
        start += 1


if __name__ == '__main__':
    client = MongoClient('localhost', 27017)
    db = client['vacancys']
    vacancys = db.vacancys

    vac_name = 'python'
    max_page = 3

    # max_page = int(input('Введите число страниц: '))
    # vacancy = input('Введите должность: ')

    parsing_hh(vac_name, max_page, vacancys)
    parsing_sj(vac_name, max_page, vacancys)
