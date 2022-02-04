from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages

from .forms import LogInForm


def index(request):
    context = {"": ""}
    return render(request, "shop/index.html", context)


# Pgae with users 'login' form, and outhput messages.
def log_in(request):
    if request.method == "POST":
        form = LogInForm(request.POST)

        # Checking is form valid.
        if form.is_valid():
            form_data = form.cleaned_data
            user = authenticate(
                username=form_data["username"],
                password=form_data["password"]
            )
            if user:
                if user.is_active:
                    login(request, user)

                    popup_message = (
                        "Process done successfully, "
                        "you can check result on the admin side.")
                    messages.success(request, popup_message)
                    return redirect("../index.html")
                    # context = {"": ""}
                    # return render(request, "shop/index.html", context)
                    # return HttpResponse()
                else:
                    return HttpResponse("Your account is not active")

            elif not user:
                popup_message = ("Process LOOOOLL")
                messages.warning(request, popup_message)
                return redirect("../login")
            else:
                return HttpResponse("Invalid username or password.")

    else:
        form = LogInForm()
    context = {"form": form}
    return render(request, "shop/login.html", context)
