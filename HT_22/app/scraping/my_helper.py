from .models import Askstories, Showstories, Newstories, Jobstories


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
            try:
                categoy_item.descendants = element["descendants"]
            except KeyError:
                categoy_item.descendants = ""
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
