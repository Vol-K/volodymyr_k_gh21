from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Sum


from .forms import ProductForm, EditProductForm, AddToCartProductForm
from .models import TeleVision, Phones, PersonalComputers, ProduntsInCart
from .shop_support import (cart_get_info_for_context, choose_model,
                           init_model_to_update_product,
                           make_context_to_edit_product)


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

        current_user_id = request.user.id
        check_products_amount = ProduntsInCart.objects.all().filter(
            user_id=current_user_id).aggregate(Sum("amount"))

        context["amount"] = check_products_amount["amount__sum"]

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

        current_user_id = request.user.id
        check_products_amount = ProduntsInCart.objects.all().filter(
            user_id=current_user_id).aggregate(Sum("amount"))

        context["amount"] = check_products_amount["amount__sum"]

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

        current_user_id = request.user.id
        check_products_amount = ProduntsInCart.objects.all().filter(
            user_id=current_user_id).aggregate(Sum("amount"))

        context["amount"] = check_products_amount["amount__sum"]

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
def add_to_cart(request):
    if request.method == "POST":
        form = AddToCartProductForm(request.POST)
        if form.is_valid():
            form_brand = request.POST.get('brand')
            form_model = request.POST.get('model')
            form_category = request.POST.get('category')
            form_amount = request.POST.get('amount')

            if request.user.is_authenticated:
                username = request.user.username
                loged_user_id = request.user.id

                # Selecting right model for the correct access to the database.
                product_all_info = choose_model(
                    form_category, form_brand, form_model)

                # Update product information to the database.
                for product in product_all_info:
                    get_prod_id = product.id
                    get_price = product.price

                product_to_cart = ProduntsInCart(
                    prod_id=get_prod_id,
                    user_id=loged_user_id,
                    category=form_category,
                    amount=form_amount,
                    price_one_product=get_price,
                )
                product_to_cart.save()

                # Getting all nedded info to the 'context'
                # for rendering 'cart' webpage.
                context_info = cart_get_info_for_context(loged_user_id)
                context = {
                    "username": username,
                    "amount": context_info[0],
                    "total_sum": context_info[1],
                    "all_products": context_info[2],
                }

                # Message to 'user', that product was added to his 'cart'.
                popup_message = (
                    "You are added product to the cart.")
                messages.success(request, popup_message)

                return render(request, "shop/cart.html", context)

    # Show all products inside 'user' cart.
    elif request.method == "GET":
        if request.user.is_authenticated:
            username = request.user.username
            current_user_id = request.user.id

            # Getting all nedded info to the 'context'
            # for rendering 'cart' webpage.
            context_info = cart_get_info_for_context(current_user_id)
            context = {
                "username": username,
                "amount": context_info[0],
                "total_sum": context_info[1],
                "all_products": context_info[2],
            }

            return render(request, "shop/cart.html", context)

        # Block access to this page for the unauthorised user.
        elif not request.user.is_authenticated:
            popup_message = ("Sorry, this page unavailable for you.")
            messages.warning(request, popup_message)
            return redirect("../index.html")
