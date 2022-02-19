import requests
import json

from app.celery import celery_app
from scraping.my_helper import CheckModelCategoryAndValue, AddAndWright


# Main logic of processing data ('category' from user).
@celery_app.task
def processing_logic(selected_category):

    requests_all_elements = requests.get(
        "https://hacker-news.firebaseio.com"
        f"/v0/{selected_category}.json?print=pretty")
    requests_all_elements = json.loads(requests_all_elements.text)

    # Getting all 'id' of elements from database
    access_database = CheckModelCategoryAndValue()
    rows_in_databse = (
        list(access_database.all_model_values(
            selected_category).values('id_item')))

    all_id_from_database = ([element["id_item"]
                             for element in rows_in_databse
                             if "id_item" in element])

    # Modifying list of elements to the wrighting into databse
    # (lits of new elements 'minus' all old elements from DB).
    requests_all_elements = (
        set(requests_all_elements+all_id_from_database) -
        set(all_id_from_database))

    # Initialize database wrighter
    wright = AddAndWright()

    # Getting each element from the list, modifying and writing them
    # one by one.
    for item in requests_all_elements:
        item_request = requests.get(
            "https://hacker-news.firebaseio.com"
            f"/v0/item/{item}.json?print=pretty")
        item_request = json.loads(item_request.text)

        # Add item elements to the database
        add_to_db = wright.wright_element(selected_category, item_request)
