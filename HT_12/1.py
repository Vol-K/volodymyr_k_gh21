"""" Завдання_1

http://quotes.toscrape.com/ - написати скрейпер для збору всієї 
    доступної інформації про записи:
        цитата, автор, інфа про автора... 
    Отриману інформацію зберегти в CSV файл та в базу. Результати зберегти в 
    репозиторії. Пагінацію по сторінкам робити динамічною (знаходите лінку 
    на наступну сторінку і берете з неї URL). 
    Хто захардкодить пагінацію зміною номеру сторінки в УРЛі - буде наказаний ;)
"""

#! перевірить імпорт
import pathlib
from pathlib import Path
import requests
from bs4 import BeautifulSoup
import sqlite3
import json
import time

####
# - id запису 
# - автор запису
# - дата народження автора
# - місто народження автора
# - країна народження автора
# - ....
# - теги запису (можливо)
# - тіло цитати

# Connect for database
database_file_path = Path(pathlib.Path.cwd(), "quotes_database.db")
database = sqlite3.connect(database_file_path, check_same_thread=False)
db_cur = database.cursor()


link = "http://quotes.toscrape.com/"
last = "https://quotes.toscrape.com/page/10/"

next_page = "empty"
x = requests.get(link)
x_soup = BeautifulSoup(x.text, 'lxml')
x_next = x_soup.select_one(".next a")

y = requests.get(last)
y_soup = BeautifulSoup(y.text, 'lxml')
y_next = y_soup.select_one(".next")
if not y_next:
    
    print("llllloooolll")
print(x_next)
print(y_next)