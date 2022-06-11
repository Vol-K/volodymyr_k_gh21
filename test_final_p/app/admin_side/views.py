# Import all necessary moduls:
# 1) from Django package.
from django.shortcuts import render, redirect
from django.contrib import messages

# 2) Local import.
from .forms import ActivateDIsableRound, CalculateUserPointsForm
from .admin_side_support import (
    func_calculate_points_by_user_forecasts,
    print_time,
    open_round_for_users_forecast,
    reset_db_values_to_default,
)
from admin_side.tasks import processing_logic
from user_side.models import ListOfMatches, ListOfUsersMatchForecast


#
def my_custom_view(request):
    if request.user.is_superuser:

        # Making matches in specified round available for the User forecast.
        if request.method == "POST" and "open_close_round" in request.POST:
            select_rounds_number = request.POST.get('rounds_list')
            open_round_for_users_forecast(select_rounds_number)

            return redirect("../dummymodel")

        # MAnual activating of the Points calculation script by User forecasts.
        elif request.method == "POST" and "calculate_points" in request.POST:
            print("--- calculate_points ---")
            func_calculate_points_by_user_forecasts()
            print("--- done ---")
            # processing_logic.delay()
            return redirect("../dummymodel")

        # Reset specified values in DB to the defauld:
        # 1) "user_points" attribute of "ListOfUsersMatchForecast" model.
        # 2) all attributes (except: "user_id", "user_name", "user_team_name")
        # of "Fintable" model.
        elif request.method == "POST" and "clean_fintable" in request.POST:
            print("--- clean_fintable & ListOfUsersMatchForecast ---")
            reset_db_values_to_default()
            print("--- done ---")
            return redirect("../dummymodel")

        # Prepare contex for GET request of page.
        else:
            form = ActivateDIsableRound(request=request)
            calculate_points = CalculateUserPointsForm()
            all_matches = ListOfMatches.objects.all()
            rounds_and_forecast_availability = all_matches.values(
                "round_numder", "forecast_availability").distinct()

            context = {"app_list": "ccc",
                       "form": form,
                       "rounds_and_forecast_availability":
                       rounds_and_forecast_availability,
                       "calculate_points": calculate_points}

            return render(request, "admin/test-custom-copy.html", context)

    else:
        popup_message = (
            "Сторінка 'DummyModelAdmin' доступна тільки для "
            "зареєстрованих користувачів.")
        messages.info(request, popup_message)
        return redirect("/admin")
