# Import all necessary moduls:
# 1) from Django package.
from django.contrib.auth.models import User
from django.db.models import Min

# 2) from Other packages.
from datetime import datetime, timedelta

# 3) Local import.
import online_users.models
from .models import (
    # AllTeams,
    ListOfMatches,
    # FinalTable,
    ListOfUsersMatchForecast,
    CustomUser
)


# Wrighting user forecast to the DataBase.
def func_add_user_forecast_to_db(user_data):
    # Create a User & Match instances to model related fields.
    # user = User.objects.filter(id=user_data["user_id"])
    user = CustomUser.objects.filter(id=user_data["user_id"])
    match = ListOfMatches.objects.filter(match_id=user_data["match_id"])

    # Initialize a model
    user_forecasts = ListOfUsersMatchForecast()

    # Inserting data and after that it's save to DB.
    # user_forecasts.match_id = user_data["match_id"]
    user_forecasts.match_id = match[0]
    user_forecasts.user_id = user[0]
    user_forecasts.teams_together = user_data["teams_together"]
    user_forecasts.home_team_forecast = user_data["home_team_forecast"]
    user_forecasts.visitor_team_forecast = user_data["visitor_team_forecast"]
    user_forecasts.round_number = user_data["round_number"]
    user_forecasts.forecast_time = user_data["forecast_time"]
    user_forecasts.forecast_type = user_data["forecast_type"]
    user_forecasts.match_in_round = user_data["match_in_round"]
    user_forecasts.save()


# Modifying user forecast into DataBase.
def func_change_user_forecast(
        user_id, match_id, forecast_for_home_team,
        forecast_for_visitor_team, new_forecast_time):

    # Initialize a model
    new_user_forecasts = ListOfUsersMatchForecast.objects.get(
        user_id=user_id, match_id=match_id)

    # Inserting new data and after that it's save to DB.
    new_user_forecasts.home_team_forecast = forecast_for_home_team
    new_user_forecasts.visitor_team_forecast = forecast_for_visitor_team
    new_user_forecasts.forecast_time = new_forecast_time
    new_user_forecasts.save()


# Checking - if have user enough time to make a forecast, or
# how many time still before the start of match.
# def func_check_time_of_user_forecast(match_date, match_time):
def func_check_time_of_user_forecast(match_details, forecast_details="ordinary", input_iser_id=0):

    #     current_date_time = datetime.now().replace(microsecond=0)
    #     current_date_time_timestamp = datetime.timestamp(current_date_time)

    #     match_date_time = datetime.combine(match_date, match_time)
    #     match_date_time_timestamp = datetime.timestamp(match_date_time)

    current_date_time = datetime.now().replace(microsecond=0)
    current_date_time_timestamp = datetime.timestamp(current_date_time)

    if forecast_details == "ordinary":
        match_date_time = datetime.combine(
            match_details.match_date, match_details.match_time)
        match_date_time_timestamp = datetime.timestamp(match_date_time)

    elif forecast_details.forecast_type == "express":
        express_details = ListOfUsersMatchForecast.objects.filter(
            user_id_id=forecast_details.user_id_id,
            round_number=match_details.round_number).annotate(Min('match_id_id'))
        # .latest('match_date', "match_time")

        express_earlest_match_date_time = ListOfMatches.objects.filter(
            match_id=express_details[0].match_id_id)
        match_date_time = datetime.combine(
            express_earlest_match_date_time[0].match_date,
            express_earlest_match_date_time[0].match_time
        )

        match_date_time_timestamp = datetime.timestamp(match_date_time)
    if match_date_time_timestamp > current_date_time_timestamp:
        check_status = True
    else:
        check_status = False

    return check_status, current_date_time


# Check quantity of Users who online on website at that time.
def quantity_of_online_users(request):
    user_status = online_users.models.OnlineUserActivity.get_user_activities(
        timedelta(seconds=60))
    users = (user for user in user_status)

    quantity_online_users = 0
    for user in users:
        quantity_online_users += 1

    if not request.session.get("online_users"):
        oline_users = request.session.setdefault(
            "online_users", quantity_online_users)
    else:
        request.session[
            "online_users"] = quantity_online_users
        # Modified session.
        request.session.modified = True

    return quantity_online_users
