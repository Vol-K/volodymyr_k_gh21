from django.shortcuts import render, redirect
# from .admin import DummyModelAdmin
from .admin_side_support import func_calculate_points_by_user_forecasts
from .forms import ActivateDIsableRound, CalculateUserPointsForm
from user_side.models import ListOfMatches, ListOfUsersMatchForecast


# Create your views here.
def my_custom_view(request):
    # from .admin import DummyModelAdmin
    if request.user.is_superuser:
        if request.method == "POST" and "open_close_round" in request.POST:
            # form = ActivateDIsableRound(request.POST, request=request)
            # print("EHUUUUUUU", form.data["rounds_list"])
            # rounds_list = request.POST.get('rounds_list')
            # form.fields['rounds_list'].choices = rounds_list

            # if form.is_valid():
            #     form_data = form.cleaned_data
            #     print("EHUUUUUUU", form_data)

            # else:
            #     form_errors = form.errors.as_data()
            #     print("form_errors", form_errors)
            # print(form)

            select_rounds_number = request.POST.get('rounds_list')

            all_matches = ListOfMatches.objects.all()
            matches_in_selected_round = all_matches.filter(
                round_numder=select_rounds_number)

            other_matches = all_matches.exclude(
                round_numder=select_rounds_number)
            matches_in_selected_round.update(forecast_availability="yes")
            other_matches.update(forecast_availability="no")

            return redirect("../dummymodel")

        elif request.method == "POST" and "calculate_points" in request.POST:
            print("calculate_points")
            return redirect("../dummymodel")
        elif request.method == "POST" and "clean_fintable" in request.POST:
            print("clean_fintable")
            return redirect("../dummymodel")
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
        print("loser")
