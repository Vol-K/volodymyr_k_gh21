from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages

from .forms import LogInForm
# from .my_helper import processing_logic


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
                    return redirect("index.html")
                    # return HttpResponse()
                else:
                    return HttpResponse("Your account is not active")

            else:
                return HttpResponse("Invalid username or password.")
    else:
        form = LogInForm()
    context = {"form": form}
    return render(request, "shop/login.html", context)
