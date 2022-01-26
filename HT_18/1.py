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
Перевірити свій код можна з допомогою ресурсу: http://pep8online.com/.

Для тих, кому хочеться зробити щось "додаткове" - можете зробити наступне: 
другим параметром cкрипт може приймати назву HTML тега і за допомогою регулярного 
виразу видаляти цей тег разом із усим його вмістом із значення атрибута "text"
(якщо він існує) отриманого запису.
"""

import sys
import json
import csv
from pathlib import Path

import requests


# Wright cleaned data to the 'CSV' file database.
class WrightData(object):
    """
    Class include one method, its writing data to the file
    using integrated 'CSV' module in python.
    """

    def wright_header(self, file_path, header):
        with open(file_path, "a", encoding="utf-8", newline="") as file:
            writer = csv.writer(file)
            writer.writerows([header])

    def wright_body(self, file_path, field_names, data):
        with open(file_path, "a", encoding="utf-8", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=field_names)
            writer.writerows([data])


# Checking inputed argument by user.
class UserInputArgumentCheck(object):

    arpoved_categories = ["askstories", "showstories",
                          "newstories", "jobstories"]

    # Check is input right argument
    # (compare with list of aproved arguments).
    def is_category_in_list(self, category):
        if category not in self.arpoved_categories:
            check_result = False
        else:
            check_result = True

        return check_result, category

    # Check is input one argument only.
    def is_valid_argument(self, argument):
        if len(argument) == 0:
            valid_result = 'default'
        elif len(argument) == 1:
            valid_result = True
        else:
            valid_result = False

        return valid_result


# Adding a new element to the header.
class HeaderModify(object):
    """
    Adding a new elements to the file header, because some elements
    inside one category has different headers (align to one etalon).
    """

    def add_new_header_element(self, header, argument):

        if argument == "jobstories":
            header.insert(3, "text")
        elif argument == "newstories":
            if "kids" not in header:
                header.insert(3, "kids")
            if "text" not in header:
                header.insert(4, "text")
        elif argument == "showstories":
            if "text" not in header:
                header.insert(3, "text")

        return header


# Keep in touch with user on element writing process.
class PrintCounterOfWrittenElement(object):

    def print_counter(self, counter):
        if counter == 1:
            print(f"Element #{counter} was write to the file.")
        elif (counter % 10) == 0:
            print(f"Element #{counter} was write to the file.")


# Create empty element to write.
class EmptyElement(object):

    def create_empty_element(self, category, id):
        if category == "newstories" or category == "showstories":
            element = {
                "by": "", "descendants": "", "id": id, "kids": "",
                "text": "", "score": "", "time": "", "title": "",
                "type": "", "url": ""}
        elif category == "askstories":
            element = {
                "by": "", "descendants": "", "id": id, "kids": "",
                "text": "", "score": "", "time": "", "title": "",
                "type": ""}
        elif category == "jobstories":
            element = {
                "by": "", "id": id, "text": "", "score": "", "time": "",
                "title": "", "type": "", "url": ""}

        return element


class GetElements(object):
    """
    Class initialize 'data_writer' & 'counter_printer' instanses, and also
    create variable: 'file_path', 'item_header', and 'counter'.
    Class method 'request_clean_elements' - getting list of all elements iside
    requster category, and cleaning and modifying header of each element.
    """

    data_writer = WrightData()
    counter_printer = PrintCounterOfWrittenElement()
    empty_element = EmptyElement()
    item_header = False
    file_path = None
    counter = 0

    # Getting list of elements, and modify them.
    def request_clean_elements(self, argument):
        self.file_path = Path(Path.cwd(), f"{argument}_db.csv")

        # Get list of elements inside inputed category.
        requests_all_elements = requests.get(
            "https://hacker-news.firebaseio.com"
            f"/v0/{argument}.json?print=pretty")
        requests_all_elements = json.loads(requests_all_elements.text)

        print("..........................................................")
        print(
            f"Congratulation, script found {len(requests_all_elements)} "
            "elements by yours request.")
        print("..........................................................")

        # Getting each element from the list, modifying and writing them
        # one by one.
        for item in requests_all_elements:
            item_request = requests.get(
                "https://hacker-news.firebaseio.com"
                f"/v0/item/{item}.json?print=pretty")
            item_request = json.loads(item_request.text)

            # Create empty 'item' is script find item without data.
            if not item_request:
                item_request = self.empty_element.create_empty_element(
                    argument, item)

            # Creating file header, and adding a new elements,
            # because some elements has different header (align to one etalon).
            if not self.item_header:
                self.item_header = list(item_request.keys())
                header_change = HeaderModify()
                self.item_header = header_change.add_new_header_element(
                    self.item_header, argument)
                self.data_writer.wright_header(self.file_path,
                                               self.item_header)

            self.data_writer.wright_body(self.file_path, self.item_header,
                                         item_request)

            # Printing to the console number of element (only dozens)
            # which was written (keeping in touch of user).
            self.counter += 1
            self.counter_printer.print_counter(self.counter)


# Script workflow.
if __name__ == '__main__':

    # Get all argumets by User from command line.
    comand_line_arguments = sys.argv

    # Checking and validation of got argument from user.
    check = UserInputArgumentCheck()
    argument_valid = check.is_valid_argument(comand_line_arguments[1:])
    if argument_valid is True:
        argument_check = check.is_category_in_list(comand_line_arguments[1])
    elif argument_valid == 'default':
        argument_check = [True, 'newstories']
        print("..........................................................")
        print("You didn't choose any categories.")
        print("Script will select the 'new stories' as a default category.")

    # Printing 'mistake' message, if argument wasn`t chaked.
    if not argument_valid:
        print("Sorry, you made mistake in arguments. Script will be stopped.")
    elif not argument_check[0]:
        print("Sorry, category doesn`t correct. Script will be stopped.")
    else:
        find_element = GetElements()
        find_element.request_clean_elements(argument_check[1])

        # Final message for user, with path to the DB file.
        print("..........................................................")
        print("You can find all saved elements in the 'CSV' database file.")
        print(find_element.file_path)
        print("..........................................................")
