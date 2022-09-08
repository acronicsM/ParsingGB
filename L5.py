from builtins import input

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

import time
import re
from pymongo import MongoClient
from pprint import pprint

reg_str = re.compile(r'0:\d+')
dbName, Coll = 'mails', 'mails_col'
Ip, Port = 'localhost', 27017


class MongoMy:
    def __init__(self):
        self._client = MongoClient(Ip, Port)
        self._db = self._client[dbName]
        self._coll = self._db[Coll]

    def update_one(self, document):
        self._coll.update_one({'_id': document.get('_id')}, {'$set': document}, upsert=True)

    def show_coll(self):
        pprint(list(self._coll.find({})))


def logging(_driver, _login, _pswd):
    _driver.get('https://account.mail.ru/')

    by_login = (By.NAME, 'username')
    by_pswd = (By.XPATH, "//input[contains(@name,'password')]")

    login = WebDriverWait(_driver, timeout=10).until(EC.presence_of_element_located(by_login))
    login.send_keys(_login)

    login.send_keys(Keys.ENTER)

    pswd = WebDriverWait(driver, timeout=3).until(EC.presence_of_element_located(by_pswd))
    while not pswd.is_displayed():
        pass
    pswd.send_keys(_pswd)

    pswd.send_keys(Keys.ENTER)


def getListMails(_driver):
    by_mails = (By.CLASS_NAME, 'contract-trigger')
    by_items = (By.TAG_NAME, 'a')
    # by_items = (By.CLASS_NAME, class_mail)
    box = '/inbox/0'

    WebDriverWait(_driver, timeout=10).until(EC.presence_of_element_located(by_mails))

    emails_list = []
    item = None
    last = -1

    while last is not None:
        for i in _driver.find_elements(*by_items):
            try:
                if box in str(i.get_attribute('href')):
                    emails_list.append(i.get_attribute('href'))
                    item = i
            except:
                pass

        last = None if last == item else item

        if last is not None:
            last.send_keys(Keys.PAGE_DOWN)
            time.sleep(3)

    return set(emails_list)


def getEmail(_driver, url):
    by_subject = (By.CLASS_NAME, 'thread-subject')
    by_contact = (By.CLASS_NAME, 'letter-contact')
    by_date = (By.CLASS_NAME, 'letter__date')
    by_body = (By.CLASS_NAME, 'letter-body')

    id = reg_str.findall(url)[0][2:]

    _driver.get(url)

    subject = WebDriverWait(_driver, timeout=10).until(EC.presence_of_element_located(by_subject)).text
    contact = WebDriverWait(_driver, timeout=10).until(EC.presence_of_element_located(by_contact)).text
    date = WebDriverWait(_driver, timeout=10).until(EC.presence_of_element_located(by_date)).text
    body = WebDriverWait(_driver, timeout=10).until(EC.presence_of_element_located(by_body)).get_attribute('innerHTML')

    MongoMy().update_one({'_id': id, 'link': url, 'subject': subject, 'contact': contact, 'date': date, 'body': body})


if __name__ == '__main__':

    _login = input('Введите логин: ')
    _pswd = input('Введите пароль: ')

    s = Service('./msedgedriver.exe')

    driver = webdriver.Edge(service=s)
    driver.maximize_window()

    logging(driver, _login, _pswd)
    emails = getListMails(driver)

    for u in emails:
        getEmail(driver, u)

    driver.close()

    MongoMy().show_coll()
