from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse

from . models import AllUsers, AllTeams, ListOfMatches, ListOfUsersMatchForecast, FinalTable
from app.forms import MakeForecastForm


#
def index(request):
    context = {}
    # Blocked access to the page for not authorized user.
    if request.user.is_authenticated:
        context["username"] = request.user.username
        return render(request, "user_side/index.html", context)
    else:
        return render(request, "user_side/index.html", context)


#
def make_forecast(request):
    # Blocked access to the page for not authorized user.
    if request.user.is_authenticated:
        if request.method == "POST":
            form = MakeForecastForm(request.POST)
            form_errors = form.errors.as_data()
            print(form_errors)
            if form.is_valid():
                form_data = form.cleaned_data
                print(form_data)
            else:
                print("BAAASSSSS")
            context = {"username": request.user.username}
        else:
            form = MakeForecastForm()
            matches_to_forecast = ListOfMatches.objects.exclude(
                forecast_availability="no")
            context = {"form": form,
                       "username": request.user.username,
                       "matches_to_forecast": matches_to_forecast}

        return render(request, "user_side/make-forecast.html", context)
    else:
        popup_message = (
            "Сторінка 'Зробити прогноз' доступна тільки для "
            "зареєстрованих користувачів.")
        messages.info(request, popup_message)
        return redirect("../index.html")


# Showing rank table of all users, with additional statistics.
def fintable(request):
    # Blocked access to the page for not authorized user.
    if request.user.is_authenticated:
        fintable_info = FinalTable.objects.all()  # ! Виписати сортіровки
        teams_rank = AllTeams.objects.all().order_by("-team_position")
        context = {"fintable": list(fintable_info),
                   "username": request.user.username,
                   "teams_rank": list(teams_rank)}
        return render(request, "user_side/fintable.html", context)
    else:
        popup_message = (
            "Сторінка 'Підсумкова таблиця' доступна тільки для "
            "зареєстрованих користувачів.")
        messages.info(request, popup_message)
        return redirect("../index.html")


#
def change_forecast(request):
    context = {}
    # Blocked access to the page for not authorized user.
    if request.user.is_authenticated:
        context["username"] = request.user.username
        return render(request, "user_side/change-forecast.html", context)
    else:
        popup_message = (
            "Сторінка 'Змінити прогноз' доступна тільки для "
            "зареєстрованих користувачів.")
        messages.info(request, popup_message)
        return redirect("../index.html")


#
def forecast_by_other(request):

    # Blocked access to the page for not authorized user.
    if request.user.is_authenticated:
        # forecasts_list = ListOfUsersMatchForecast.objects.exclude(
        #     user_id=request.user.id)
        forecasts_list = ListOfUsersMatchForecast.objects.all()
        context = {"username": request.user.username,
                   "match_forecasts": forecasts_list}
        return render(request, "user_side/forecast-by-other.html", context)
    else:
        popup_message = (
            "Сторінка 'Прогнози інших користувачів' доступна тільки для "
            "зареєстрованих користувачів.")
        messages.info(request, popup_message)
        return redirect("../index.html")


# Showing
def teams_and_members(request):
    # Blocked access to the page for not authorized user.
    if request.user.is_authenticated:
        xx = request.user.id
        print(xx)
        #! Дописать сортіровку по командам, та балах учасників
        teams_and_members_data = FinalTable.objects.exclude(
            user_team_name__isnull=True)
        context = {"username": request.user.username,
                   "team_and_members": list(teams_and_members_data)}
        return render(request, "user_side/teams-and-members.html", context)
    else:
        popup_message = (
            "Сторінка 'Команди та їх учасники' доступна тільки для "
            "зареєстрованих користувачів.")
        messages.info(request, popup_message)
        return redirect("../index.html")


#
def user_account(request):
    context = {}
    # Blocked access to the page for not authorized user.
    if request.user.is_authenticated:
        context["username"] = request.user.username
        return render(request, "user_side/account.html", context)
    else:
        popup_message = (
            "Сторінка 'Акаунт' доступна тільки для "
            "зареєстрованих користувачів.")
        messages.info(request, popup_message)
        return redirect("../index.html")
