"""
Напишіть скрейпер для сайту "vikka.ua", який буде приймати від
користувача дату, збирати і зберігати інформацію про новини за вказаний день.

Особливості реалізації:
-використовувати лише Scrapy, BeautifulSoup (опціонально), lxml (опціонально)
та вбудовані модулі Python;
-дані повинні зберігатися у csv файл з датою в якості назви у форматі 
"рік_місяць_число.csv" (напр. 2022_01_13.csv);
- дані, які потрібно зберігати (саме в такому порядку вони мають бути у файлі):
1.Заголовок новини;
2.Текст новини у форматі рядка без HTML тегів та у вигляді суцільного тексту
(Добре: "Hello world" Погано: "<p>Hello</p><p>world</p>");
3.Теги у форматі рядка, де всі теги записані з решіткою через кому 
(#назва_тегу, #назва_тегу, ...);
4. URL новини.
- збереження даних у файл може відбуватися за бажанням або в самому спайдері, 
або через Pipelines (буде плюсом в карму);
- код повинен бути написаний з дотриманням вимог PEP8 (іменування змінних, функцій,
класів, порядок імпортів, відступи, коментарі, документація і т.д.);
- клієнт не повинен здогадуватися, що у вас в голові - додайте якісь підказки там,
де це необхідно;
- клієнт може випадково ввести некорректні дані, пам'ятайте про це;
- якщо клієнту доведеться відправляти вам бота на доопрацювання багато разів, 
або не всі його вимоги будуть виконані - він знайде іншого виконавця, а з вами 
договір буде розірваний. У нього в команді немає тестувальників, тому перед 
відправкою завдання - впевніться, що все працює і відповідає ТЗ.
- не забудьте про requirements.txt;
- клієнт буде запускати бота через термінал командою "scrapy crawl назва_скрейпера".
"""


import re
import scrapy
from pathlib import Path
import datetime
import csv


# Check date fromat from User 
class CheckWrongSymbols(object):
    """
    This class has one goal, check date gotten from User 
    for the correct date format or no.
    """

    @staticmethod
    def check_symbols(date):
            
        false_counter = 0
        for elem in date:
            if not elem.isdigit():
                if elem != "/":
                    false_counter += 1

        if false_counter != 0:
            check = False
        else:
            check = True

        return check

# Getting from User right date
class GetRightDate(object):
    """
    Getting from User right date (not to old and not from the future).
    """
    def is_right_date(sef, date_by_user):
        exit_date_check_cicle = False
        while not exit_date_check_cicle:

            check = CheckWrongSymbols
            if not check.check_symbols(date_by_user):
                print("...........................................................")
                print("You input date in wrong format, try as example (2013/12/31)")
                date_by_user = input("Please input date: ")
            else:
                date_now = datetime.datetime.now()
                ransform_date_by_user = datetime.datetime.strptime(date_by_user, "%Y/%m/%d")
                oldest_date_in_archive = datetime.datetime.strptime("2010/01/11", "%Y/%m/%d")
        
                if ransform_date_by_user > date_now:
                    print(".......................................")
                    print("Sorry, you input future date, try again")
                    date_by_user = input("Please input date: ")
                elif ransform_date_by_user < oldest_date_in_archive:
                    print("....................................................................")
                    print("Sorry, you input to old date, oldest date in archive is - 2010/01/11")
                    date_by_user = input("Please input date: ")
                else:
                    print("......................")
                    print("You input correct date")
                    exit_date_check_cicle = True

        return exit_date_check_cicle

class VikkaSpider(scrapy.Spider):
    
    name = 'vikka'
    allowed_domains = ['vikka.ua']

    # Introducing block for User
    print("...........................................................")
    print("Hello, You can get newsline by one days from Vikka website.")
    print("Please, use correct format of date, for example: 2013/12/31")
    # date_by_user = input("Please input date: ")
    date_by_user = "2021/01/02"

    # Getting from User right date (not to old and not from the future)
    get_date = GetRightDate()
    get_date.is_right_date(date_by_user)

    # Link for our start parsing
    basic_url = "https://www.vikka.ua/"
    start_urls = [basic_url + date_by_user]

    # Support elements for printing end message
    link_counter = 0
    news_counter = 0

    # Name & path to th CSV file
    file_name = date_by_user.replace("/", "_") + ".csv"
    news_csv_file_path = Path(Path.cwd(), file_name)

    # Method for parsing links to the news
    def parse(self, response):
        for element in response.css(".cat-post-info"):
            VikkaSpider.link_counter += 1
            news_link = element.css("h2.title-cat-post a::attr(href)").get()
            yield response.follow(news_link, callback=self.parse_news)
            
    # Processing of news links from 'parse' method
    # Get info what we need (title, test, tags, link)
    def parse_news(self, response):
        VikkaSpider.news_counter += 1

        news_title = response.css("h1.post-title::text").get()

        news_body = response.css("div.entry-content p::text").getall()
        news_body = " ".join(news_body).strip()

        news_tags = response.css("a.post-tag::text").getall()
        # Modifying tags (added to him "#")
        tags_modifyed = []
        for item in news_tags:
            item = "#" + item
            tags_modifyed.append(item)
        news_tags = ", ".join(tags_modifyed).strip() 

        news_url = response.url

        # List with all scraped information
        news_details = [news_title, news_body, news_tags, news_url]

        # Append data to the 'CSV' file
        with open(self.news_csv_file_path, "a", encoding="utf-8", newline="") as news:
            writer = csv.writer(news)
            writer.writerows([news_details])

        # End message, that proccess finished
        if (VikkaSpider.link_counter != 0) and (VikkaSpider.news_counter != 0):
            if VikkaSpider.link_counter == VikkaSpider.news_counter:
                print("..............................................................")
                print("..............................................................")
                print("Proccess finished, you can find file with date on this adress:")
                print(self.news_csv_file_path)
                print("..............................................................")
                print("..............................................................")