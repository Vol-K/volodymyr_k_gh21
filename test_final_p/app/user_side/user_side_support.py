from .models import (AllTeams, ListOfMatches, FinalTable,
                     ListOfUsersMatchForecast)
from django.contrib.auth.models import User

from datetime import datetime


# Wrighting user forecast to the DataBase.
def func_add_user_forecast_to_db(user_data):
    # Create a User instance to model related field.
    user = User.objects.filter(id=user_data["user_id"])

    # Initialize a model
    user_forecasts = ListOfUsersMatchForecast()
    # Inserting data and after that it's save to DB.
    user_forecasts.match_id = user_data["match_id"]
    user_forecasts.user_id = user[0]
    user_forecasts.teams_together = user_data["teams_together"]
    user_forecasts.home_team_forecast = user_data["home_team_forecast"]
    user_forecasts.visitor_team_forecast = user_data["visitor_team_forecast"]
    user_forecasts.round_numder = user_data["round_numder"]
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
def func_check_time_of_user_forecast(match_date, match_time):

    current_date_time = datetime.now().replace(microsecond=0)
    current_date_time_timestamp = datetime.timestamp(current_date_time)

    match_date_time = datetime.combine(match_date, match_time)
    match_date_time_timestamp = datetime.timestamp(match_date_time)

    if match_date_time_timestamp > current_date_time_timestamp:
        check_status = True
    else:
        check_status = False

    return check_status, current_date_time
