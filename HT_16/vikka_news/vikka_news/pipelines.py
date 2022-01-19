# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3


# Savind got data (from 'vikka' spider) to the SQL DB
class VikkaNewsPipeline:

    # Initialise DB methods
    def __init__(self):
        self.create_conn()
        self.create_table()

    # Create connect to DB and cursor
    def create_conn(self):
        self.database = sqlite3.connect("vikka_news.db")
        self.db_cur = self.database.cursor()
   
    # Create table
    def create_table(self):
        self.db_cur.execute("DROP TABLE IF EXISTS news")
        self.db_cur.execute("CREATE TABLE news (date TEXT, title TEXT, \
                             body TEXT, tags TEXT, url TEXT)") 

    def process_item(self, item, spider):
        self.write_news(item)
        return item

    # Write data to the table into SQL DB
    def write_news(self, item):
        items = tuple(item.values())
        self.db_cur.execute("INSERT INTO news VALUES (?, ?, ?, ?, ?)", items)
        self.database.commit()