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
