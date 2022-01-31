from .models import Askstories, Showstories, Newstories, Jobstories

import requests
import json


# Working with models.
class CheckModelCategoryAndValue(object):

    # Checking data by user, and init right model.
    def initialize_right_category(self, inp_category):
        if inp_category == "askstories":
            initialuzed_model = Askstories()
        elif inp_category == "showstories":
            initialuzed_model = Showstories()
        elif inp_category == "newstories":
            initialuzed_model = Newstories()
        elif inp_category == "jobstories":
            initialuzed_model = Jobstories()

        return initialuzed_model

    # Get all ites from selected model.
    def all_model_values(self, inp_category):
        if inp_category == "askstories":
            all_rows = Askstories.objects.all()
        elif inp_category == "showstories":
            all_rows = Showstories.objects.all()
        elif inp_category == "newstories":
            all_rows = Newstories.objects.all()
        elif inp_category == "jobstories":
            all_rows = Jobstories.objects.all()

        return all_rows


# Writhing elements to the 'SQlite' database.
class AddAndWright(object):

    # Selecting correct model for writing data.
    def wright_element(self, user_category, element):

        if user_category == "askstories":
            model = CheckModelCategoryAndValue()
            categoy_item = model.initialize_right_category(user_category)
            categoy_item.by = element["by"]
            categoy_item.descendants = element["descendants"]
            categoy_item.id_item = element["id"]
            try:
                categoy_item.kids = element["kids"]
            except KeyError:
                categoy_item.kids = ""
            try:
                categoy_item.text = element["text"]
            except KeyError:
                categoy_item.text = ""
            categoy_item.score = element["score"]
            categoy_item.time = element["time"]
            categoy_item.title = element["title"]
            categoy_item.type = element["type"]
            categoy_item.save()

        elif user_category == "showstories":
            model = CheckModelCategoryAndValue()
            categoy_item = model.initialize_right_category(user_category)
            categoy_item.by = element["by"]
            categoy_item.descendants = element["descendants"]
            categoy_item.id_item = element["id"]
            try:
                categoy_item.kids = element["kids"]
            except KeyError:
                categoy_item.kids = ""
            try:
                categoy_item.text = element["text"]
            except KeyError:
                categoy_item.text = ""
            categoy_item.score = element["score"]
            categoy_item.time = element["time"]
            categoy_item.title = element["title"]
            categoy_item.type = element["type"]
            try:
                categoy_item.url = element["url"]
            except KeyError:
                categoy_item.url = ""
            categoy_item.save()

        elif user_category == "newstories":
            model = CheckModelCategoryAndValue()
            categoy_item = model.initialize_right_category(user_category)
            categoy_item.by = element["by"]
            categoy_item.descendants = element["descendants"]
            categoy_item.id_item = element["id"]
            try:
                categoy_item.kids = element["kids"]
            except KeyError:
                categoy_item.kids = ""
            try:
                categoy_item.text = element["text"]
            except KeyError:
                categoy_item.text = ""
            categoy_item.score = element["score"]
            categoy_item.time = element["time"]
            categoy_item.title = element["title"]
            categoy_item.type = element["type"]
            try:
                categoy_item.url = element["url"]
            except KeyError:
                categoy_item.url = ""
            categoy_item.save()

        elif user_category == "jobstories":
            model = CheckModelCategoryAndValue()
            categoy_item = model.initialize_right_category(user_category)
            categoy_item.by = element["by"]
            categoy_item.id_item = element["id"]
            try:
                categoy_item.text = element["text"]
            except KeyError:
                categoy_item.text = ""
            categoy_item.score = element["score"]
            categoy_item.time = element["time"]
            categoy_item.title = element["title"]
            categoy_item.type = element["type"]
            try:
                categoy_item.url = element["url"]
            except KeyError:
                categoy_item.url = ""
            categoy_item.save()


# Logic of main workflow for: get, check, and writhe data.
# Get list of elements inside inputed category.
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
