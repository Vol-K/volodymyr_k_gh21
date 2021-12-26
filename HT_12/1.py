"""" Завдання_1

http://quotes.toscrape.com/ - написати скрейпер для збору всієї 
    доступної інформації про записи:
        цитата, автор, інфа про автора... 
    Отриману інформацію зберегти в CSV файл та в базу. Результати зберегти в 
    репозиторії. Пагінацію по сторінкам робити динамічною (знаходите лінку 
    на наступну сторінку і берете з неї URL). 
    Хто захардкодить пагінацію зміною номеру сторінки в УРЛі - буде наказаний ;)
"""

from pathlib import Path
import requests
from bs4 import BeautifulSoup
import sqlite3
import csv


# Connect for database
database_file_path = Path(Path.cwd(), "quotes_database.db")
database = sqlite3.connect(database_file_path, check_same_thread=False)
db_cur = database.cursor()

# Path to th CSV file (other DB)
quotes_details_path = Path(Path.cwd(), "quotes_details.csv")

# Links for the website
link_backup = "http://quotes.toscrape.com/"
page_link = "http://quotes.toscrape.com/"

csv_counter = 0

print("## Start script ##")

end_flag = False
while not end_flag:

    got_page = requests.get(page_link)
    got_page_soup = BeautifulSoup(got_page.text, 'lxml')
    quotes = got_page_soup.select(".quote")

    # Get all info about each quote
    for element in quotes:

        # Author name block
        author_name = element.select_one(".author")
        author_name = author_name.get_text()

        # Get access to the detailed info about author
        author_half_link = element.find(href=True)
        author_half_link = author_half_link["href"]
        author_link = link_backup + author_half_link
        author_page = requests.get(author_link)
        author_page_soup = BeautifulSoup(author_page.text, 'lxml')
        
        # Author birth date block
        author_birth_date = author_page_soup.select_one(".author-born-date")
        author_birth_date = author_birth_date.get_text()

        # Author birth location block
        author_birth_location = author_page_soup.select_one(".author-born-location")
        author_birth_location = author_birth_location.get_text()
        birth_location = author_birth_location.split(", ")
        
        if len(birth_location) == 1:
            author_city = None
            author_country = birth_location[-1][3:]
        elif len(birth_location) == 2: 
            author_city = birth_location[0][3:]
            author_country = birth_location[-1]
        elif len(birth_location) > 2:
            author_country = birth_location[-1]
            birth_location.pop(-1)
            author_city = ', '.join(birth_location)
            author_city = author_city[3:]

        # Tags block
        tags_soup = element.select(".tag")
        tags_for_insert = ""

        for item in tags_soup:
            get_tag = item.get_text()
            if len(tags_for_insert) < 1:
                tags_for_insert += (get_tag)
            else:
                tags_for_insert += (", " + get_tag)

        # Quote-body block
        quote = element.select_one(".text")
        quote = quote.get_text()

        # Wrigth all info about quote to the DB (SQLite3 block)
        quote_info_list = [author_name, author_birth_date, author_city,
                           author_country, tags_for_insert, quote]
        db_cur.execute("INSERT INTO quote_info (author, birth_date, birth_city,\
                        birth_country, quote_tags, quote_body) \
                        VALUES (?, ?, ?, ?, ?, ?)", quote_info_list)
        database.commit()

        # CSV vlock
        csv_counter += 1
        quote_info_list.insert(0, str(csv_counter))
       
        if not author_city:
            quote_info_list[3] = ""
           
        new_row = []
        new_row.append(quote_info_list) 
        with open(quotes_details_path, "a", encoding="utf-8", newline="") as quotes_details:
            writer = csv.writer(quotes_details)
            if csv_counter == 1:
                writer.writerow(["id", "author", "birth_date", "birth_city",
                                    "birth_country", "quote_tags", "qoute_body"])
            writer.writerows(new_row)
        
    print(f"## Find & added element #{csv_counter} into DB ##")

    # Next page rule (is it valid)
    next_page = got_page_soup.select_one(".next a[href]")
    if not next_page:
        print("## END script ##")
        end_flag = True
    else:
        next_page_link = next_page["href"]
        page_link = link_backup + next_page_link