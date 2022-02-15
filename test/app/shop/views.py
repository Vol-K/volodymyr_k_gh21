from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import ProductForm, EditProductForm, AddToCartProductForm
from .models import TeleVision, Phones, PersonalComputers
from .shop_support import (
    choose_model, details_prod_info,
    init_model_to_update_product,
    make_context_to_edit_product,
    added_processing, check_items_in_cart
)


# Getting all products by 'Phone' category from DB and rendering page.
def phone(request):
    products = list(Phones.objects.all())
    context = {
        "products": products,
        "category": "mobile"
    }

    # Checking is this user are logged what viewing this page.
    # And include his name to showing on the webpage.
    if request.user.is_authenticated:
        context["username"] = request.user.username
        if request.user.is_superuser:
            context["user_tupe"] = "admin"

        items_in_cart = check_items_in_cart(request)
        context["amount"] = items_in_cart

    return render(request, "shop/phone.html", context)


# Getting all products by 'Computers' category from DB and rendering page.
def computers(request):
    products = list(PersonalComputers.objects.all())
    context = {
        "products": products,
        "category": "pc"
    }

    # Checking is this user are logged what viewing this page.
    # And include his name to showing on the webpage.
    if request.user.is_authenticated:
        context["username"] = request.user.username
        if request.user.is_superuser:
            context["user_tupe"] = "admin"

        items_in_cart = check_items_in_cart(request)
        context["amount"] = items_in_cart

    return render(request, "shop/computers.html", context)


# Getting all products by 'TV' category from DB and rendering page.
def television(request):
    products = list(TeleVision.objects.all())
    context = {
        "products": products,
        "category": "tv"
    }

    # Checking is this user are logged what viewing this page.
    # And include his name to showing on the webpage.
    if request.user.is_authenticated:
        context["username"] = request.user.username
        if request.user.is_superuser:
            context["user_tupe"] = "admin"

        items_in_cart = check_items_in_cart(request)
        context["amount"] = items_in_cart

    return render(request, "shop/television.html", context)


# Showing info of edited product.
def edit_product(request):
    if request.method == "POST":

        form = ProductForm(request.POST)

        if form.is_valid():
            form_brand = request.POST.get('brand')
            form_model = request.POST.get('model')
            category = request.POST.get('category')

            if request.user.is_authenticated:
                if request.user.is_superuser:
                    username = request.user.username

                    # Selecting right model for the correct access to the database.
                    product_info = choose_model(
                        category, form_brand, form_model)

                    context = make_context_to_edit_product(
                        product_info, category, username)

                    return render(request, "shop/editproduct.html", context)

    # Block access to this page for the unauthorised user.
    else:
        popup_message = ("Sorry, this page unavailable for you now.")
        messages.warning(request, popup_message)

        return redirect("../index.html")


# Getting new parameters for the product and wright it's to the database.
def edited(request):

    if request.method == "POST":

        form = EditProductForm(request.POST)
        if form.is_valid():
            form_brand = request.POST.get('brand')
            form_model = request.POST.get('model')
            form_category = request.POST.get('category')
            form_description = request.POST.get('description')
            form_price = request.POST.get('price')
            form_available = request.POST.get('available')
            old_brand = request.POST.get('old_brand')
            old_model = request.POST.get('old_model')

            # Selecting right model for the correct access to the database.
            product_info = choose_model(
                form_category, old_brand, old_model)

            # Getting product 'id' from database.
            for product in product_info:
                get_id = product.id

            # Update product parameters into database.
            product_to_update = init_model_to_update_product(
                form_category, get_id, form_brand, form_model,
                form_description, form_price, form_available
            )
            product_to_update.save()

        # Message on case on inputed invalid values.
        else:
            popup_message = ("Sorry, invalid values into form, try again.")
            messages.warning(request, popup_message)

            return redirect("../index.html")

    # Message - product was updated.
    popup_message = ("UPDATED")
    messages.warning(request, popup_message)

    return redirect("../index.html")


# Adding product to the cart.
def new_add_to_cart(request):

    prod_id = request.POST.get("id")
    prod_category = request.POST.get("category")

    # Added one more product to the cart (all logic).
    if prod_id:
        added = added_processing(request, prod_id, prod_category)

    # return redirect("phone.html")
    check_items_in_cart = request.session.get("user_cart")
    products_quantity = check_items_in_cart.get("item_quantity")
    # return JsonResponse({"quantity": added, "amount": products_quantity})
    print(prod_id)
    return JsonResponse({"quantity": added})


def user_cart(request):
    if request.user.is_authenticated:
        username = request.user.username
        # current_user_id = request.user.id
        check_user_cart = request.session.get("user_cart")
        if not check_user_cart:
            context = {"all_products": None}
        else:
            products_in_cart = check_user_cart.get("products")
            detailed_prod_info = details_prod_info(products_in_cart)
            context = {
                "username": username,
                "amount": check_user_cart.get("item_quantity"),
                "all_products": detailed_prod_info,
                "total_sum": check_user_cart.get("total"),
            }

        return render(request, "shop/cart.html", context)

    elif not request.user.is_authenticated:
        popup_message = ("Sorry, this page unavailable for you.")
        messages.warning(request, popup_message)
        return redirect("../index.html")
