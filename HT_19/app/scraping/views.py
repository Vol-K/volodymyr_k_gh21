from django.shortcuts import render
from django.contrib import messages

import requests
import json

from .forms import CategoryForm
from .support_class import CheckModelCategoryAndValue, AddAndWright


# Logic for sending and processing form with data by user.
def index(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)

        if form.is_valid():
            selected_category = request.POST.get('field')

            # Get list of elements inside inputed category.
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
                add_to_db = wright.wright_element(
                    selected_category, item_request)

            # After success proccess show popup and link to the 'Admin side' 
            # of website for checking what were scraped.
            mesega = (
                "Process done successfully, "
                "you can check result on the admin side.")
            messages.success(request, mesega)

    # Generate page for the first view.
    context = {
        "form": CategoryForm()
    }
    return render(request, 'scraping/index.html', context)
