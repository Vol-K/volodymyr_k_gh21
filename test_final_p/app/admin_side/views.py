# Import all necessary moduls:
# 1) from Django package.
from django.shortcuts import render, redirect
from django.contrib import messages

# 2) Local import.
from .forms import (ActivateDisableRound, CalculateUserPointsForm,
                    LookingMatchesScoreForm)
from .admin_side_support import (
    open_round_for_users_forecast,
    reset_db_values_to_default
)
from admin_side.tasks import points_calculation_manual, looking_for_scores_manual
from user_side.models import ListOfMatches


# Create additional (not connected to model) page for Django admin view.
def my_custom_view(request):
    if request.user.is_superuser:

        # Making matches in specified round available for the User forecast.
        if request.method == "POST" and "open_close_round" in request.POST:
            select_rounds_number = request.POST.get('rounds_list')
            open_round_for_users_forecast(select_rounds_number)
            return redirect("../custommodel")

        # Manual activating of the Points calculation script by User forecasts.
        elif request.method == "POST" and "calculate_points" in request.POST:
            points_calculation_manual.delay()
            return redirect("../custommodel")

        # Manual activating of the Points
        elif request.method == "POST" and "looking_matches_score" in request.POST:
            looking_for_scores_manual.delay()
            return redirect("../custommodel")

        # Reset specified values in DB to the defauld:
        # 1) "user_points" attribute of "ListOfUsersMatchForecast" model.
        # 2) all attributes (except: "user_id", "user_name", "user_team_name")
        # of "Fintable" model.
        elif request.method == "POST" and "clean_fintable" in request.POST:
            reset_db_values_to_default()
            return redirect("../custommodel")

        # Prepare contex for GET request of page.
        else:
            form = ActivateDisableRound(request=request)
            calculate_points = CalculateUserPointsForm()
            looking_matches_score = LookingMatchesScoreForm()
            all_matches = ListOfMatches.objects.all()
            rounds_and_forecast_availability = all_matches.values(
                "round_number", "forecast_availability").distinct()

            context = {
                "form": form,
                "rounds_and_forecast_availability":
                rounds_and_forecast_availability,
                "calculate_points": calculate_points,
                "looking_matches_score": looking_matches_score
            }

            return render(request, "admin/custom-page.html", context)

    # Blocking not authorize access.
    else:
        popup_message = (
            "Сторінка 'DummyModelAdmin' доступна тільки для "
            "зареєстрованих користувачів.")
        messages.info(request, popup_message)
        return redirect("/admin")
