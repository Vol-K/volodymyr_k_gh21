from . models import AllUsers, AllTeams, ListOfMatches, ListOfUsersMatchForecast, FinalTable


def xxxx():
    matches_to_forecast = ListOfMatches.objects.exclude(
        forecast_availability="no")

    output_list = []
    for element in matches_to_forecast:
        print(element.teams_together)
        output_list.append(
            tuple(element.teams_together, element.teams_together))
    return output_list


#
def add_user_forecast_to_db(user_data):
    user_forecasts = ListOfUsersMatchForecast()
    #
    user_forecasts.match_id = user_data["match_id"]
    user_forecasts.user_id = user_data["user_id"]
    user_forecasts.teams_together = user_data["teams_together"]
    user_forecasts.home_team_forecast = user_data["home_team_forecast"]
    user_forecasts.visitor_team_forecast = user_data["visitor_team_forecast"]
    user_forecasts.round_numder = user_data["round_numder"]
    user_forecasts.forecast_time = user_data["forecast_time"]
    # user_forecasts.user_points = ""
    user_forecasts.forecast_type = user_data["forecast_type"]
    user_forecasts.match_in_round = user_data["match_in_round"]
    user_forecasts.save()
