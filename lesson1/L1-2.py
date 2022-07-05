# Изучить список открытых API (https://www.programmableweb.com/category/all/apis).
# Найти среди них любое, требующее авторизацию (любого типа).
# Выполнить запросы к нему, пройдя авторизацию.
# Ответ сервера записать в файл.

import requests

key = input('Введите ключ: ')
url = 'https://suppliers-api.wildberries.ru/public/api/v1/info'
agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 ' \
        'Safari/537.36 OPR/86.0.4363.59 (Edition Yx 05) '

header = {'User-Agent': agent,
          'Authorization': key,
          'Content-Type': "application/json"}

request = requests.get(url, headers=header)

if request.ok:
    with open("response_wb.json", "w", encoding="utf-8") as f:
        f.write(request.text)
