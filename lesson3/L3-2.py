# Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой больше введённой суммы
# (необходимо анализировать оба поля зарплаты).
# То есть цифра вводится одна, а запрос проверяет оба поля

from pprint import pprint
from pymongo import MongoClient


def fid_vacancys(vacancys, payment: int):

    param12 = {'$or': [
        {'min_zp': {'$gt': payment}},
        {'max_zp': {'$gt': payment}}
    ]
    }

    return list(vacancys.find(param12))


if __name__ == '__main__':
    client = MongoClient('localhost', 27017)
    db = client['vacancys']
    vacancys = db.vacancys

    pprint(fid_vacancys(vacancys, 100_000))
