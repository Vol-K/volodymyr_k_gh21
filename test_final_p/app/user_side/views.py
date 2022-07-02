# Import all necessary moduls:
# 1) from Django package.
from django.contrib import messages
from django.shortcuts import render, redirect

# 2) Local import.
from .models import (AllTeams, ListOfMatches,
                     ListOfUsersMatchForecast, FinalTable, CustomUser)
from .user_side_support import (
    func_add_user_forecast_to_db,
    func_check_time_of_user_forecast,
    func_change_user_forecast,
    quantity_of_online_users
)
from app.forms import (MakeForecastForm, ChangeForecastForm,
                       DeleteAllForecastsForm, ChangeSendEmailReminderForm)


# Main/landing page of the website/project.
def index(request):

    # Show welcome message for User and show some statistical info about him.
    if request.user.is_authenticated and not request.user.is_superuser:
        user_statistics = FinalTable.objects.filter(user_id_id=request.user.id)
        online_users = quantity_of_online_users(request)
        context = {"username": request.user.username,
                   "online_users": online_users,
                   "user_statistics": user_statistics[0]}

        return render(request, "user_side/index.html", context)

    # Blocked access to the page for not authorized user.
    else:
        return render(request, "user_side/index.html")


# Creating a match forecast by user (include all limitations).
def make_forecast(request):
    if request.user.is_authenticated and not request.user.is_superuser:

        # Getting information from 'Form' (user forecast), and processing
        # of all data (checking, validating, writhing/show error message).
        if request.method == "POST":
            form = MakeForecastForm(request.POST, request=request)

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
                    match_all_details[0]
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
                            round_number=match_all_details[0].round_number
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
                    "round_number": match_all_details[0].round_number,
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
                user_id=request.user.id).order_by(
                    "-round_number",
                    "match_in_round"
            )
            online_users = quantity_of_online_users(request)
            context = {"form": form,
                       "username": request.user.username,
                       "predicted_matches": list(predicted_matches),
                       "online_users": online_users}
            return render(request, "user_side/make-forecast.html", context)

    # Blocking access to the page for not authorized user.
    else:
        popup_message = (
            "Сторінка 'Зробити прогноз' доступна тільки для "
            "зареєстрованих користувачів.")
        messages.info(request, popup_message, extra_tags="general")
        return redirect("../index.html")


# A change of existing match forecast by user.
def change_forecast(request):
    if request.user.is_authenticated and not request.user.is_superuser:
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
                    match_id=forecast_details[0].match_id_id)

                # Checking for action availability (time block).
                check_date_time_forecast = func_check_time_of_user_forecast(
                    match_details[0],
                    forecast_details[0],
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
                        "Вибачте, операція доступна тільки до початку матча / експреса матчів.")
                    messages.info(request, popup_message, extra_tags="general")

            else:
                popup_message = (
                    "Вибачте, внесено некоректну інформацію, "
                    "спробуйте ще раз.")
                messages.info(request, popup_message, extra_tags="general")

            return redirect("../make-forecast.html")

        # Main processing logic for delete of selected match.
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
                    match_id=forecast_details[0].match_id_id)

                # Checking is this action availabile in that time for
                # ime block for "ordynary" forecast type.
                check_date_time_forecast = func_check_time_of_user_forecast(
                    match_details[0],
                    forecast_details[0],
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
                        "Вибачте, операція доступна тільки до початку матча "
                        "/ експреса матчів.")
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

                # Checking for action availability (time block).
                # Checking which round are active now.
                round_details = ListOfMatches.objects.filter(
                    forecast_availability="yes").values(
                        "round_number"
                ).distinct()

                user_forecasts_in_corrent_round = (
                    ListOfUsersMatchForecast.objects.filter(
                        user_id=request.user.id,
                        round_number=round_details[0]["round_number"]
                    )
                )

                # Prevent to change express forecast when first match
                # from express was started
                if (user_forecasts_in_corrent_round[0].forecast_type == "ordinary"):
                    user_forecasts_in_corrent_round.delete()

                    popup_message = (
                        "Ви щойно видалили всі прогнози в даному турі")
                    messages.info(request, popup_message, extra_tags="general")

                elif (user_forecasts_in_corrent_round[0].forecast_type == "express"):
                    # Getting forecast and match details.
                    forecast_details = ListOfUsersMatchForecast.objects.filter(
                        user_id=request.user.id,
                        teams_together=user_forecasts_in_corrent_round[0].teams_together
                    )
                    match_details = ListOfMatches.objects.filter(
                        match_id=forecast_details[0].match_id_id)

                    check_date_time_forecast = func_check_time_of_user_forecast(
                        match_details[0],
                        forecast_details[0],
                    )

                    if check_date_time_forecast[0]:
                        forecast_details.delete()
                        popup_message = (
                            "Ви щойно видалили прогноз на матч "
                            f"'{match_details[0]['teams_together']}'.")
                        messages.info(request, popup_message,
                                      extra_tags="general")

                    else:
                        popup_message = (
                            "Вибачте, операція доступна тільки до початку матча "
                            "/ експреса матчів.")
                        messages.info(request, popup_message,
                                      extra_tags="general")

            #
            else:
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
            online_users = quantity_of_online_users(request)
            context = {"username": request.user.username,
                       "forecasted_matches": forecasted_matches,
                       "form": form,
                       "delete_form": delete_form,
                       "online_users": online_users}
            return render(request, "user_side/change-forecast.html", context)

    # Blocking access to the page for not authorized user.
    else:
        popup_message = (
            "Сторінка 'Змінити прогноз' доступна тільки для "
            "зареєстрованих користувачів.")
        messages.info(request, popup_message)
        return redirect("../index.html")


# Showing rank table of all users, with additional statistics.
def fintable(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        fintable_info = FinalTable.objects.all().order_by(
            "-user_points",
            "-user_predicted_match_score",
            "-user_average_point_per_match"
        )
        teams_rank = AllTeams.objects.all().order_by("team_position")
        # show_all_rounds = ListOfMatches.objects.all().values("round_number").distinct()
        show_all_rounds = ListOfMatches.objects.all().values(
            "round_number", "forecast_availability").distinct()
        active_round = show_all_rounds.filter(
            forecast_availability="yes")

        try:
            active_round = active_round[0]["round_number"]
        except IndexError:
            show_all_rounds = [{"round_number": 0,
                               "forecast_availability": "no"}]
            active_round = 0

        online_users = quantity_of_online_users(request)
        context = {"fintable": list(fintable_info),
                   "username": request.user.username,
                   "teams_rank": list(teams_rank),
                   "show_all_rounds": show_all_rounds,
                   "active_round": active_round,
                   "online_users": online_users}

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

    if request.user.is_authenticated and not request.user.is_superuser:
        # Get all forecasts and excluded forecasts by user who send request.
        forecasts_list = ListOfUsersMatchForecast.objects.exclude(
            user_id=request.user.id)
        online_users = quantity_of_online_users(request)
        context = {"username": request.user.username,
                   "match_forecasts": forecasts_list,
                   "online_users": online_users}
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
    if request.user.is_authenticated and not request.user.is_superuser:

        # Ordering list by name of team & user points.
        teams_and_members_data = FinalTable.objects.exclude(
            user_team_name__exact="").order_by(
                "user_team_name",
                "-user_points"
        )
        online_users = quantity_of_online_users(request)
        context = {"username": request.user.username,
                   "team_and_members": list(teams_and_members_data),
                   "online_users": online_users}
        return render(request, "user_side/teams-and-members.html", context)

    # Blocking access to the page for not authorized user.
    else:
        popup_message = (
            "Сторінка 'Команди та їх учасники' доступна тільки для "
            "зареєстрованих користувачів.")
        messages.info(request, popup_message)
        return redirect("../index.html")


# Access to change "send email notification" about forecasts by Iser.
def user_account(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        if request.method == "POST" and "change_reminder" in request.POST:
            form = ChangeSendEmailReminderForm(request.POST)

            if form.is_valid():
                form_data = form.cleaned_data

                current_user = CustomUser.objects.filter(id=request.user.id)
                current_user.update(send_reminder=int(
                    form_data["change_reminder"]))

                popup_message = (
                    "Ви щойно змінили налаштування надсилання нагадувань")
                messages.info(request, popup_message, extra_tags="general")
                return redirect("../account.html")

        # Generate 'Form' for first user visit to the page.
        else:
            # Getting only one available option to change.
            current_user_reminder_status = CustomUser.objects.filter(
                id=request.user.id)[0].send_reminder

            form = ChangeSendEmailReminderForm(request=request)
            online_users = quantity_of_online_users(request)
            context = {"username": request.user.username,
                       "form": form,
                       "current_reminder_status": current_user_reminder_status,
                       "online_users": online_users}
            return render(request, "user_side/account.html", context)

    # Blocking access to the page for not authorized user.
    else:
        popup_message = (
            "Сторінка 'Акаунт' доступна тільки для "
            "зареєстрованих користувачів.")
        messages.info(request, popup_message)
        return redirect("../index.html")


# Represent "Club rules" for registered Users.
def club_rules(request):
    if request.user.is_authenticated and not request.user.is_superuser:

        online_users = quantity_of_online_users(request)
        context = {"online_users": online_users}
        return render(request, "user_side/club-rules.html", context)

    # Blocking access to the page for not authorized user.
    else:
        popup_message = (
            "Сторінка 'Акаунт' доступна тільки для "
            "зареєстрованих користувачів.")
        messages.info(request, popup_message)
        return redirect("../index.html")
