from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Sum

from .forms import LogInForm
from shop.models import TeleVision, Phones, PersonalComputers, ProduntsInCart


# Getting all products by all categories from DB and rendering page.
def index(request):

    all_phones = list(Phones.objects.all())
    all_tv = list(TeleVision.objects.all())
    all_computers = list(PersonalComputers.objects.all())

    # Packaging all variables inside 'context' of the webpage.
    context = {"phone": all_phones,
               "television": all_tv,
               "computers": all_computers}

    # Check type of authenticated user and his name.
    if request.user.is_authenticated:
        if request.user.is_superuser:
            context["username"] = request.user.username
            context["user_tupe"] = "admin"
        else:
            context["username"] = request.user.username
        current_user_id = request.user.id

        check_products_amount = ProduntsInCart.objects.all().filter(
            user_id=current_user_id).aggregate(Sum("amount"))

        context["amount"] = check_products_amount["amount__sum"]

    return render(request, "shop/index.html", context)


# Page with users 'login' form, and outhput messages for
# success/failure login results.
def log_in(request):
    if request.method == "POST":
        form = LogInForm(request.POST)

        # Checking is form valid.
        if form.is_valid():
            form_data = form.cleaned_data
            user = authenticate(
                username=form_data["username"],
                password=form_data["password"],
            )

            if user:
                if user.is_active:
                    login(request, user)

                    # Output message.
                    popup_message = (
                        f"Congratulation user: '{form_data['username']}', "
                        "you are login to our webshop."
                    )
                    messages.success(request, popup_message)

                    return redirect("../index.html")

                else:
                    return HttpResponse(
                        "Your account is not active, contact with "
                        "website admin."
                    )

            # Output message if inputed invalid values.
            elif not user:
                popup_message = ("Invalid username or password, try again.")
                messages.error(request, popup_message)

                return redirect("../login")

            # Message for case if something went wrong.
            else:
                return HttpResponse(
                    "Server can't process your request, happened something "
                    "wrong. Please try again after a few seconds."
                )

    # Redirectuser to the 'Login' page, to try again.
    else:
        form = LogInForm()

    context = {"form": form}

    return render(request, "shop/login.html", context)


# Exit user from the website.
def log_out(request):
    logout(request)
    return redirect("../index.html")
