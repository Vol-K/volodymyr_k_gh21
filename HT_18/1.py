""" Завдання_1

Використовуючи бібліотеку requests написати скрейпер для отримання статей / 
записів із АПІ.

Документація на АПІ: https://github.com/HackerNews/API

Скрипт повинен отримувати із командного рядка одну із наступних категорій:
askstories, showstories, newstories, jobstories.

Якщо жодної категорії не указано - використовувати newstories. Якщо категорія 
не входить в список - вивести попередження про це і завершити роботу.

Результати роботи зберегти в CSV файл. Зберігати всі доступні поля. 
Зверніть увагу - інстанси різних типів мають різний набір полів.

Код повинен притримуватися стандарту pep8.
Перевірити свій код можна з допомогою ресурсу http://pep8online.com/.

Для тих, кому хочеться зробити щось "додаткове" - можете зробити наступне: 
другим параметром cкрипт може приймати назву HTML тега і за допомогою регулярного 
виразу видаляти цей тег разом із усим його вмістом із значення атрибута "text"
(якщо він існує) отриманого запису.
"""


import json
import csv
from pathlib import Path

import requests


class UseInputCategoryCheck(object):

    arpoved_categories = ["askstories", "showstories",
                          "newstories", "jobstories"]

    def is_category_in_list(self, inp_category):

        if inp_category[0] not in self.arpoved_categories:
            check_result = False
        else:
            check_result = True

        return check_result, inp_category


class WelcomeMessage(object):

    def message(self, categories):
        print(".........................................................")
        print("###   Hello, available 4 categories for the script.   ###")

        for item in categories:
            print(F"Category name: '{item}'")
        user_input = input(
            "Please, select one categories (its name) from this list: ").split()
            
        return user_input


# Script workflow logic
if __name__ == '__main__':
    check = UseInputCategoryCheck()
    welcome = WelcomeMessage()
    ddd = welcome.message(check.arpoved_categories)

    xxx = check.is_category_in_list(ddd)

    if not xxx[0]:
        print("LOL")
    else:
        requests_t = requests.get(
            f"https://hacker-news.firebaseio.com/v0/{xxx[1][0]}.json?print=pretty")
        requests_t = json.loads(requests_t.text)

        for item in requests_t:
            item_request = requests.get(
                f"https://hacker-news.firebaseio.com/v0/item/{item}.json?print=pretty")
            item_request = json.loads(item_request.text)
            print(item_request)

    # print("HHHH")
