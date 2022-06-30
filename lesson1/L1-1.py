# Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя,
# сохранить JSON-вывод в файле *.json.

import requests

# name = input('Введите имя пользователя: ')
name = 'laixintao'
url = 'https://api.github.com/users/' + name + '/repos'
header = {'User-Agent':
              'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 '
              'Safari/537.36 OPR/86.0.4363.59 (Edition Yx 05)'}

request = requests.get(url, headers=header)

if request.ok:
    with open("response.json", "w", encoding="utf-8") as f:
        f.write(request.text)

    a = [f"{i.get('name')}{' (' + i.get('description') + ')' if i.get('description') else ''}"for i in request.json()]
    print(*a, sep='\n')
    