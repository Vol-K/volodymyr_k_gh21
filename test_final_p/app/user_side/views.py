# from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.shortcuts import render, redirect
# from django.http import HttpResponse

# from datetime import datetime

from .models import AllTeams, ListOfMatches, ListOfUsersMatchForecast, FinalTable
from .user_side_support import (
    func_add_user_forecast_to_db,
    func_check_time_of_user_forecast,
    func_change_user_forecast
)
from app.forms import (MakeForecastForm, ChangeForecastForm,
                       DeleteAllForecastsForm)


#
def index(request):
    context = {}
    # Blocked access to the page for not authorized user.
    if request.user.is_authenticated and not request.user.is_superuser:
        context["username"] = request.user.username
        return render(request, "user_side/index.html", context)
    else:
        return render(request, "user_side/index.html", context)


#! Треба блокувати зміни до початку першого експреса
# Creating a match forecast by user (include all limitations).
def make_forecast(request):
    if request.user.is_authenticated:

        # Getting information from 'Form' (user forecast), and processing
        # of all data (checking, validating, writhing/show error message).
        if request.method == "POST":
            form = MakeForecastForm(request.POST, request=request)

            form_errors = form.errors.as_data()
            print(form_errors)

            if form.is_valid():
                form_data = form.cleaned_data

                # Getting detail information about match.
                match_all_details = ListOfMatches.objects.filter(
                    teams_together=form_data["teams_together"])

                # Check for prevent dubicate forecast by user.
                check_for_dublicat_forecast = (
                    ListOfUsersMatchForecast.objects.filter(
                        user_id=request.user.id,
                        match_id=match_all_details[0].match_id,
                    )
                )
                # Check time availabilty for the forecast (time block).
                check_date_time_forecast = func_check_time_of_user_forecast(
                    match_all_details[0].match_date,
                    match_all_details[0].match_time
                )

                # Procces of checking all possible 'blocks' fo the rorecast.
                # Activate time block.
                if not check_date_time_forecast[0]:
                    popup_message = (
                        "Вибачте, операція доступна тільки до початку матча.")
                    messages.info(request, popup_message, extra_tags="general")
                    return redirect("../make-forecast.html")

                # Prevent to make a duplicate of forecast.
                elif check_for_dublicat_forecast:
                    popup_message_general = (
                        "Вибачте, у вас є прогноз на цей матч"
                    )
                    messages.info(request, popup_message_general,
                                  extra_tags="general")
                    return redirect("../make-forecast.html")

                # If user do not create a dublicate of forecast
                # and time enought before start of the match.
                else:
                    # Checking for only one 'forecast_type' in current round
                    # by one user.
                    check_for_one_only_forecast_type = (
                        ListOfUsersMatchForecast.objects.filter(
                            user_id=request.user.id,
                            round_numder=match_all_details[0].round_numder
                        ).values("forecast_type").distinct()
                    )

                    if check_for_one_only_forecast_type:

                        # Check
                        if len(check_for_one_only_forecast_type) > 1:
                            popup_message_forecast_type = (
                                "Вибачте, в даному турі у вас присутні "
                                "два типи прогнозів."
                            )
                            messages.info(request, popup_message_forecast_type,
                                          extra_tags="forecast_type")

                            popup_message_general = (
                                "Будь-ласка, Зверніться до адміністратора"
                            )
                            messages.info(request, popup_message_general,
                                          extra_tags="general")
                            return redirect("../make-forecast.html")

                        elif len(check_for_one_only_forecast_type) == 1:

                            # Preventing to make a two different forecast type.
                            # For 'ordinary'.
                            if (check_for_one_only_forecast_type[0]
                                ["forecast_type"]) == ("ordinary") and (
                                    form_data["forecast_type"] != "ordinary"):
                                popup_message_forecast_type = (
                                    "Вибачте, обрано некоректний тип прогноза, "
                                    "вам доступні тільки 'Ординар'."
                                )
                                messages.info(
                                    request,
                                    popup_message_forecast_type,
                                    extra_tags="general"
                                )
                                popup_message_general = ("Спробуйте ще раз.")
                                messages.info(request, popup_message_general,
                                              extra_tags="general")
                                return redirect("../make-forecast.html")
                            # For 'express'.
                            elif (check_for_one_only_forecast_type[0]
                                  ["forecast_type"]) == "express" and (
                                    form_data["forecast_type"] != "express"):
                                popup_message_forecast_type = (
                                    "Вибачте, обрано некоректний тип прогноза,"
                                    " вам доступні тільки 'Експрес'."
                                )
                                messages.info(
                                    request,
                                    popup_message_forecast_type,
                                    extra_tags="forecast_type"
                                )
                                popup_message_general = ("Спробуйте ще раз.")
                                messages.info(request, popup_message_general,
                                              extra_tags="general")
                                return redirect("../make-forecast.html")

                # Combining all information about "user forecast on match"
                # to the 'dict', and write its to the DB.
                user_data = {
                    "user_id": request.user.id,
                    "match_id": match_all_details[0].match_id,
                    "teams_together": form_data["teams_together"],
                    "home_team_forecast": form_data["team_home_user_forecast"],
                    "visitor_team_forecast": form_data[
                        "team_visitor_user_forecast"],
                    "round_numder": match_all_details[0].round_numder,
                    "match_in_round": match_all_details[0].match_in_round,
                    "forecast_type": form_data["forecast_type"],
                    "forecast_time": check_date_time_forecast[1]
                }
                func_add_user_forecast_to_db(user_data)

                popup_message = (
                    "Ви зробили прогноз на матч "
                    f"'{form_data['teams_together']}'")
                messages.info(request, popup_message, extra_tags="general")

            else:
                popup_message = (
                    "Вибачте, внесено некоректну інформацію, спробуйте ще раз")
                messages.info(request, popup_message, extra_tags="general")

            return redirect("../make-forecast.html")

        # Generate 'Form' for first user visit to the page.
        else:
            form = MakeForecastForm(request=request)
            predicted_matches = ListOfUsersMatchForecast.objects.filter(
                user_id=request.user.id)
            context = {"form": form,
                       "username": request.user.username,
                       "predicted_matches": list(predicted_matches)}
            return render(request, "user_side/make-forecast.html", context)

    # Blocking access to the page for not authorized user.
    else:
        popup_message = (
            "Сторінка 'Зробити прогноз' доступна тільки для "
            "зареєстрованих користувачів.")
        messages.info(request, popup_message, extra_tags="general")
        return redirect("../index.html")


#! Треба блокувати зміни до початку першого експреса
# A change of existing match forecast by user.
def change_forecast(request):
    if request.user.is_authenticated:
        if request.method == "POST" and "change" in request.POST:

            form = ChangeForecastForm(request.POST, request=request)

            if form.is_valid():
                form_data = form.cleaned_data

                # Check is form forecasts field are not empty,
                # exclude "0" (zero) type of value in the field.
                if (not form_data["team_home_user_forecast"] or
                    not form_data["team_visitor_user_forecast"]) and (
                    form_data["team_home_user_forecast"] is None or
                        form_data["team_visitor_user_forecast"] is None):

                    popup_message = (
                        "Поля з рахунками обов'язкові для заповнення, "
                        "спробуйте ще раз.")
                    messages.info(request, popup_message, extra_tags="general")
                    return redirect("../change-forecast.html")

                # Getting forecast and match details.
                forecast_details = ListOfUsersMatchForecast.objects.filter(
                    user_id=request.user.id,
                    teams_together=form_data["teams_together"]
                )
                match_details = ListOfMatches.objects.filter(
                    match_id=forecast_details[0].match_id)

                # Checking for action availability (time block).
                check_date_time_forecast = func_check_time_of_user_forecast(
                    match_details[0].match_date,
                    match_details[0].match_time
                )

                if check_date_time_forecast[0]:

                    func_change_user_forecast(
                        request.user.id,
                        forecast_details[0].match_id,
                        form_data["team_home_user_forecast"],
                        form_data["team_visitor_user_forecast"],
                        check_date_time_forecast[1]
                    )

                else:
                    popup_message = (
                        "Вибачте, операція доступна тільки до початку матча.")
                    messages.info(request, popup_message, extra_tags="general")

            else:
                popup_message = (
                    "Вибачте, внесено некоректну інформацію, "
                    "спробуйте ще раз.")
                messages.info(request, popup_message, extra_tags="general")

            return redirect("../make-forecast.html")

        #
        elif request.method == "POST" and "delete" in request.POST:
            form = ChangeForecastForm(request.POST, request=request)

            if form.is_valid():
                form_data = form.cleaned_data

                # Getting forecast and match details.
                forecast_details = ListOfUsersMatchForecast.objects.filter(
                    user_id=request.user.id,
                    teams_together=form_data["teams_together"]
                )
                match_details = ListOfMatches.objects.filter(
                    match_id=forecast_details[0].match_id)

                # Checking for action availability (time block).
                check_date_time_forecast = func_check_time_of_user_forecast(
                    match_details[0].match_date,
                    match_details[0].match_time
                )

                if check_date_time_forecast[0]:
                    forecast_details.delete()
                    popup_message = (
                        "Ви щойно видалили прогноз на матч "
                        f"'{form_data['teams_together']}'.")
                    messages.info(request, popup_message,
                                  extra_tags="general")

                else:
                    popup_message = (
                        "Вибачте, операція доступна тільки до початку матча.")
                    messages.info(request, popup_message, extra_tags="general")

            else:
                popup_message = (
                    "Вибачте, внесено некоректну інформацію, "
                    "спробуйте ще раз.")
                messages.info(request, popup_message, extra_tags="general")

            return redirect("../make-forecast.html")

        #
        elif request.method == "POST" and "delelete_all" in request.POST:
            form = DeleteAllForecastsForm(request.POST)

            if form.is_valid():

                #! Окрема лоігка для 'експресів' треба.

                # Checking for action availability (time block).

                # Checking which round are active now.
                round_details = ListOfMatches.objects.filter(
                    forecast_availability="yes").values("round_numder").distinct()

                user_forecasts_in_corrent_round = ListOfUsersMatchForecast.objects.filter(
                    user_id=request.user.id,
                    round_numder=round_details[0]["round_numder"]
                )
                user_forecasts_in_corrent_round.delete()

                popup_message = (
                    "Ви щойно видалили всі прогнози в даному турі")
                messages.info(request, popup_message, extra_tags="general")

            #
            else:
                # form_errors = form.errors.as_data()
                # print(form_errors)
                popup_message = (
                    "Вибачте, внесено некоректну інформацію, "
                    "спробуйте ще раз.")
                messages.info(request, popup_message, extra_tags="general")

            return redirect("../make-forecast.html")

        # Generate 'Form' for first user visit to the page.
        else:
            form = ChangeForecastForm(request=request)
            delete_form = DeleteAllForecastsForm()
            forecasted_matches = ListOfUsersMatchForecast.objects.filter(
                user_id=request.user.id)
            context = {"username": request.user.username,
                       "forecasted_matches": forecasted_matches,
                       "form": form,
                       "delete_form": delete_form}
            return render(request, "user_side/change-forecast.html", context)

    # Blocking access to the page for not authorized user.
    else:
        popup_message = (
            "Сторінка 'Змінити прогноз' доступна тільки для "
            "зареєстрованих користувачів.")
        messages.info(request, popup_message)
        return redirect("../index.html")


#! Треба блокувати зміни до початку першого експреса


# Showing rank table of all users, with additional statistics.
def fintable(request):
    if request.user.is_authenticated:
        fintable_info = FinalTable.objects.all().order_by(
            "-user_points",
            "-user_predicted_match_score",
            "-user_average_point_per_match"
        )
        teams_rank = AllTeams.objects.all().order_by("team_position")
        context = {"fintable": list(fintable_info),
                   "username": request.user.username,
                   "teams_rank": list(teams_rank)}
        return render(request, "user_side/fintable.html", context)

    # Blocking access to the page for not authorized user.
    else:
        popup_message = (
            "Сторінка 'Підсумкова таблиця' доступна тільки для "
            "зареєстрованих користувачів.")
        messages.info(request, popup_message)
        return redirect("../index.html")


# Showing forecasted of matches from other users,
# excluded forecasts by user who send request.
def forecast_by_other(request):

    if request.user.is_authenticated:
        # Get all forecasts and excluded forecasts by user who send request.
        forecasts_list = ListOfUsersMatchForecast.objects.exclude(
            user_id=request.user.id)
        # forecasts_list = ListOfUsersMatchForecast.objects.all()

        context = {"username": request.user.username,
                   "match_forecasts": forecasts_list}
        return render(request, "user_side/forecast-by-other.html", context)

    # Blocking access to the page for not authorized user.
    else:
        popup_message = (
            "Сторінка 'Прогнози інших користувачів' доступна тільки для "
            "зареєстрованих користувачів.")
        messages.info(request, popup_message)
        return redirect("../index.html")


# Showing list of 'teams' and their member
def teams_and_members(request):
    if request.user.is_authenticated:

        # Ordering list by name of team & user points.
        teams_and_members_data = FinalTable.objects.exclude(
            user_team_name__exact="").order_by(
                "user_team_name",
                "-user_points"
        )
        context = {"username": request.user.username,
                   "team_and_members": list(teams_and_members_data)}
        return render(request, "user_side/teams-and-members.html", context)

    # Blocking access to the page for not authorized user.
    else:
        popup_message = (
            "Сторінка 'Команди та їх учасники' доступна тільки для "
            "зареєстрованих користувачів.")
        messages.info(request, popup_message)
        return redirect("../index.html")


#
def user_account(request):
    context = {}
    if request.user.is_authenticated:
        context["username"] = request.user.username
        return render(request, "user_side/account.html", context)

    # Blocking access to the page for not authorized user.
    else:
        popup_message = (
            "Сторінка 'Акаунт' доступна тільки для "
            "зареєстрованих користувачів.")
        messages.info(request, popup_message)
        return redirect("../index.html")
