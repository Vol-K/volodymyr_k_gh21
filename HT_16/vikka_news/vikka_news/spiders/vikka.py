"""
Переробити попереднє домашнє завдання: зберігати результати в базу, 
використовуючи pipelines.
"""


import scrapy
import datetime
from ..items import VikkaNewsItem


# Check date fromat from User
class CheckDate(object):
    """
    This class has one goal, check date gotten from User 
    for the correct date format or no.
    """

    @staticmethod
    def check_wrong_symbols(date):

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

    # Checking it is real date or this 'str' included mixed
    # permitted symbols only.
    def is_it_date(self, user_date):

        try:
            datetime.datetime.strptime(user_date, "%Y/%m/%d")
            check_result = True
        except ValueError:
            check_result = False

        return check_result


# Getting from User right date
class GetRightDate(object):
    """
    Getting from User right date (not to old and not from the future).
    """
    
    def is_right_date(sef, date_by_user):
        exit_date_check_cicle = False
        while not exit_date_check_cicle:

            check = CheckDate()
            if not check.check_wrong_symbols(date_by_user):
                print("...........................................................")
                print("You input date in wrong format, try as example (2013/12/31)")
                date_by_user = input("Please input date: ")
            elif not check.is_it_date(date_by_user):
                print("..............................................................")
                print("Sorry, you inputed not date, try again as example (2013/12/31)")
                date_by_user = input("Please input date: ")
            else:
                date_now = datetime.datetime.now()
                ransform_date_by_user = datetime.datetime.strptime(
                    date_by_user, "%Y/%m/%d")
                oldest_date_in_archive = datetime.datetime.strptime(
                    "2010/01/11", "%Y/%m/%d")

                if ransform_date_by_user > date_now:
                    print("..................................................")
                    print("###  Sorry, you input future date, try again.  ###")
                    date_by_user = input("Please input date: ")
                elif ransform_date_by_user < oldest_date_in_archive:
                    print(
                        "....................................................................")
                    print(
                        "Sorry, you input to old date, oldest date in archive is - 2010/01/11")
                    date_by_user = input("Please input date: ")
                else:
                    print("......................")
                    print("You input correct date")
                    exit_date_check_cicle = True

        return date_by_user


class VikkaSpider(scrapy.Spider):

    name = 'vikka2'
    allowed_domains = ['vikka.ua']

    # Introducing block for User
    print("...........................................................")
    print("Hello, You can get newsline by one days from Vikka website.")
    print("Please, use correct format of date, for example: 2013/12/31")
    date_by_user = input("Please input date: ")

    # Getting from User right date (not to old and not from the future)
    get_date = GetRightDate()
    date_by_user = get_date.is_right_date(date_by_user)

    # Link for our start parsing
    basic_url = "https://www.vikka.ua/"
    start_urls = [basic_url + date_by_user]

    # Support elements for printing end message
    link_counter = 0
    news_counter = 0

    # Method for parsing links to the news
    def parse(self, response):
        for element in response.css(".cat-post-info"):
            VikkaSpider.link_counter += 1
            news_link = element.css("h2.title-cat-post a::attr(href)").get()
            yield response.follow(news_link, callback=self.parse_news)

        # Checking of pagination
        pagination = response.css("div.nav-links")
        if pagination:
            next_page = pagination.css("a.next::attr(href)").get()
            yield response.follow(next_page, callback=self.parse)

    # Processing of news links from 'parse' method
    # Get info what we need (title, test, tags, link)
    def parse_news(self, response):
        VikkaSpider.news_counter += 1

        news_title = response.css("h1.post-title::text").get()

        news_body = []
        for elem in response.css("div.entry-content"):
            news_body = elem.css("div.entry-content p strong::text, \
                div.entry-content p::text, div.entry-content p em::text, \
                div.entry-content p em a::text, \
                div.entry-content p a::text").extract()
            news_body = list(map(str.strip, news_body))
        news_body = " ".join(news_body)
        news_body = news_body.replace(" .", ".")

        news_tags = response.css("a.post-tag::text").getall()
        # Modifying tags (added to him "#")
        tags_modifyed = []
        for item in news_tags:
            item = "#" + item
            tags_modifyed.append(item)
        news_tags = ", ".join(tags_modifyed).strip()

        news_url = response.url

        # Forming a dict with all scraped information about each news and
        # sent it to the 'pipeline' for writing into SQL databse.
        item = {"date": self.date_by_user, "title": news_title,
                "body": news_body, "tags": news_tags, "url": news_url}
        yield item

        # End message, that proccess finished
        if (VikkaSpider.link_counter != 0) and (VikkaSpider.news_counter != 0):
            if VikkaSpider.link_counter == VikkaSpider.news_counter:
                print("...................................................")
                print("...................................................")
                print("#####  Congratulation, process are finished.  #####")
                print("...................................................")
                print("...................................................")
