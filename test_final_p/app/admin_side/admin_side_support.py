# Import all necessary moduls:
# 1) from Selenium package.
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

# 2) from Django package.
from django.db.models import Sum

# 3) from Other packages.
from bs4 import BeautifulSoup
from pathlib import Path
from datetime import datetime, date

# 4) Local import.
from user_side.models import (
    ListOfMatches,
    ListOfUsersMatchForecast,
    FinalTable,
    AllTeams
)
from .send_emails_support import (
    send_match_error_message_to_admin,
    send_round_error_message_to_admin
)


# Logic for looking scores of every match on active round, used Selenium.
def looking_for_scores_of_matches_in_round():

    ##! PC (local server) options !##
    # Setup options for "Google Chrome" by local server.
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")

    # Select webdriver path and open browser
    webdriver_path = Path(Path.cwd(), "chromedriver")
    wd = Chrome(options=options, executable_path=webdriver_path)

    # Link to the form which must be filled.
    page_link = "https://www.flashscore.com/football/"

    wd.get(page_link)
    wait = WebDriverWait(wd, 10)

    # Start to scrap data from website.
    finished_match_list = []
    eurocups_playing_days = ["Tuesday", "Wednesday", "Thursday", "1", "2", "2"]
    for day in eurocups_playing_days:
        print(day)
        # Click on calendar for move to previus day.
        calendar_select_yesterday = WebDriverWait(wd, 90).until(
            EC.element_to_be_clickable(
                (By.CLASS_NAME, "calendar__navigation--yesterday")
            )
        ).click()

        # Getting data from the website calendar, to prevent matcheing of
        # "team name" on other match pair (in other days).
        date_from_calendar = WebDriverWait(wd, 90).until(
            EC.element_to_be_clickable(
                (By.CLASS_NAME, "calendar__datepicker")
            )
        )

        # Convert calendar date to "datetime" format.
        splited_on_date_month = date_from_calendar.text[:-3].split("/")
        current_year = date.today().year

        date_str = (str(current_year)+"-" +
                    splited_on_date_month[1]+"-"+splited_on_date_month[0])
        year_date_time_from_calendar = datetime.strptime(
            date_str, "%Y-%m-%d").date()

        # Get "all matches" from soup.
        raw_list_of_matches = WebDriverWait(wd, 90).until(
            EC.visibility_of_all_elements_located(
                (By.CLASS_NAME, "event__match--twoLine"))
        )
        matches_in_round = ListOfMatches.objects.filter(
            forecast_availability="yes")

        current_round = matches_in_round[0].round_number

        # Compare home&visitor teams name with teams from soup.
        for match in matches_in_round:
            db_home_team = match.home_team
            db_visitor_team = match.visitor_team

            for raw_match in raw_list_of_matches:
                raw_matches_html = raw_match.get_attribute('innerHTML')
                raw_matches_soup = BeautifulSoup(raw_matches_html, "lxml")

                home_team_name = raw_matches_soup.select(
                    ".event__participant--home")
                visitor_team_name = raw_matches_soup.select(
                    ".event__participant--away")
                try:
                    match_status = raw_matches_soup.select(
                        ".event__stage")[0].text
                except IndexError:
                    match_status = "Неправильний статус матча на сайті"

                # Prevent uncorrect scripts start, when one team play in
                # other game in closest time from our match.
                if (home_team_name[0].text == db_home_team and
                        visitor_team_name[0].text != db_visitor_team and
                        match.match_date == year_date_time_from_calendar):

                    finished_match_list.append("no")
                    match_data = {
                        "match_status": match_status,
                        "teams_together": (
                            home_team_name[0].text +
                            " " +
                            visitor_team_name[0].text
                        )
                    }
                    send_match_error_message_to_admin(match_data)
                elif (home_team_name[0].text != db_home_team and
                      visitor_team_name[0].text == db_visitor_team and
                      match.match_date == year_date_time_from_calendar):

                    finished_match_list.append("no")
                    match_data = {
                        "match_status": match_status,
                        "teams_together": (
                            home_team_name[0].text +
                            " " +
                            visitor_team_name[0].text
                        )
                    }
                    send_match_error_message_to_admin(match_data)

                # Laucn deep compare script, check names of teams and
                # date of current match.
                elif (home_team_name[0].text == db_home_team and
                      visitor_team_name[0].text == db_visitor_team and
                      match.match_date == year_date_time_from_calendar):

                    visitor_team_name = raw_matches_soup.select(
                        ".event__participant--away")
                    home_team_score = raw_matches_soup.select(
                        ".event__score--home")
                    visitor_team_score = raw_matches_soup.select(
                        ".event__score--away")

                    if (home_team_name[0].text == db_home_team and
                            visitor_team_name[0].text == db_visitor_team):

                        # Check is digints
                        home_team_score_isdigit_check = (
                            home_team_score[0].text.isdigit()
                        )
                        visitor_team_score_isdigit_check = (
                            visitor_team_score[0].text.isdigit()
                        )

                        # Check is score of match are digits.
                        if (not home_team_score_isdigit_check or
                                not visitor_team_score_isdigit_check):
                            finished_match_list.append("no")

                            match_data = {
                                "match_status": match_status,
                                "teams_together": (
                                    home_team_name[0].text +
                                    " " +
                                    visitor_team_name[0].text
                                )
                            }
                            send_match_error_message_to_admin(match_data)

                        # Update match-info on DataBase & "finished_match_list".
                        else:
                            finished_match_list.append("yes")

                            match.home_team_result = home_team_score[0].text
                            match.visitor_team_result = visitor_team_score[0].text
                            match.save()

    # Checkig is it ok with all matches in round (found all results).
    if "no" in finished_match_list:
        match_data = {
            "round_number": current_round,
        }
        send_round_error_message_to_admin(match_data)

    # Start proccess of calculation User points by forecasts.
    else:
        func_calculate_points_by_user_forecasts()


# Calculating points based on User forecast on each match.
def func_calculate_points_by_user_forecasts():
    # Make nessesary sets.
    input_matches_in_round = ListOfMatches.objects.filter(
        forecast_availability="yes").filter(
            home_team_result__isnull=False,
            visitor_team_result__isnull=False
    )
    input_round_number = input_matches_in_round[0].round_number
    all_forecasts = ListOfUsersMatchForecast.objects.filter(
        round_number=input_round_number)
    list_of_user_hwo_did_forecast = all_forecasts.values("user_id").distinct()

    # Calculate points proccess (from User point of view).
    for user in list_of_user_hwo_did_forecast:
        forecasts_by_user = all_forecasts.filter(
            user_id=user["user_id"], round_number=input_round_number)

        for forecast in forecasts_by_user:
            results = input_matches_in_round.filter(
                match_id=forecast.match_id_id)

            # Prevent start calculation proccess if DataBase doesnt
            # have scores of match.
            if results:
                home_team_score = results[0].home_team_result
                visitor_team_score = results[0].visitor_team_result

                # Two way of calculation of points by "User" forecasts.
                # If user has "ordinary" type of forecasts.
                user_type_of_forecast = forecasts_by_user.values(
                    "forecast_type").distinct()[0]["forecast_type"]
                if user_type_of_forecast == "ordinary":

                    # For the precision user forecast - 2 points.
                    if (home_team_score == forecast.home_team_forecast and
                            visitor_team_score == forecast.visitor_team_forecast):
                        forecast.user_points = "2"
                        forecast.save()

                    # For the positive user forecast (draw/win_home/win_visitor) - 1 point.
                    elif ((home_team_score == visitor_team_score and
                            forecast.home_team_forecast == forecast.visitor_team_forecast) or
                            (home_team_score > visitor_team_score and
                             forecast.home_team_forecast > forecast.visitor_team_forecast) or
                            (home_team_score < visitor_team_score and
                             forecast.home_team_forecast < forecast.visitor_team_forecast)):
                        forecast.user_points = "1"
                        forecast.save()

                    # For bad user forecast (guessed nothing)
                    else:
                        forecast.user_points = "0"
                        forecast.save()

                # Or if user has "express" type of forecasts.
                elif user_type_of_forecast == "express":
                    # For the precision user forecast - 2 points.
                    if ((home_team_score == visitor_team_score and
                            forecast.home_team_forecast == forecast.visitor_team_forecast) or
                            (home_team_score > visitor_team_score and
                             forecast.home_team_forecast > forecast.visitor_team_forecast) or
                            (home_team_score < visitor_team_score and
                             forecast.home_team_forecast < forecast.visitor_team_forecast)):
                        forecast.user_points = "2"
                        forecast.save()

                    else:
                        forecasts_by_user.update(user_points=0)
                        break

    # Updating whole statistic information & based on it ranked:
    # 1) about "User" inside "Fintable".
    update_user_statistic_in_fintab(input_round_number)
    # 2) about "Teams" inside "Allteams".
    update_userteam_statistic_in_allteams()
    # 3) ranking.
    sort_fintable()
    sort_allteams()


# Make visible&available specify round fore the new users forecast.
def open_round_for_users_forecast(number_of_round):
    # Get all matches from DB, and separated its for two parts:
    # firts - will be available for the forecast, second - not available.
    all_matches = ListOfMatches.objects.all()
    matches_in_selected_round = all_matches.filter(
        round_number=number_of_round)
    other_matches = all_matches.exclude(
        round_number=number_of_round)

    # Updated "forecast_availability" attribute inside all matches in DB.
    matches_in_selected_round.update(forecast_availability="yes")
    other_matches.update(forecast_availability="no")


# Reset values in DataBase tables to the default.
def reset_db_values_to_default():
    # By "user_points" attribute of "ListOfUsersMatchForecast".
    all_forecasts_by_users = ListOfUsersMatchForecast.objects.all()
    all_forecasts_by_users.update(user_points=None)

    # By "team_position" attribute of "AllTeams".
    all_teams_statistics = AllTeams.objects.all()
    all_teams_statistics.update(team_position=0)

    # By "user_points" of "FinalTable".
    all_users_statistic = FinalTable.objects.all()
    all_users_statistic.update(
        user_position=0,
        user_points=0,
        user_potential_points=0,
        user_average_point_per_match=0.0,
        user_all_predicted_matches=0,
        user_predicted_match_score=0,
        user_predicted_match_result=0,
        user_predicted_express=0,
        user_not_predicted_express=0,
        user_achive_guru_turu=0
    )


# Update/create forecast`s statustic information for every "User".
def update_user_statistic_in_fintab(input_round_number):
    # Initialize necessary models with all data.
    all_forecasts = ListOfUsersMatchForecast.objects.all()
    users_statistics = FinalTable.objects.all()

    # Calculate statistic numbers for every user & write its to DataBase.
    for user in users_statistics:
        all_forecasts_by_user = ListOfUsersMatchForecast.objects.filter(
            user_id=user.user_id)

        # Calculating some auxiliary statistics data.
        total_points_sum = all_forecasts_by_user.aggregate(Sum("user_points"))
        forecasted_matches = all_forecasts_by_user.count()

        # Save a new data by "User".
        if total_points_sum["user_points__sum"]:
            user.user_points = total_points_sum["user_points__sum"]
        else:
            user.user_points = 0

        user.user_potential_points = forecasted_matches * 2

        try:
            user.user_average_point_per_match = (
                round((total_points_sum["user_points__sum"] /
                      forecasted_matches), 2))
        except TypeError:
            user.user_average_point_per_match = 0

        user.user_all_predicted_matches = forecasted_matches
        user.user_predicted_match_score = all_forecasts_by_user.filter(
            user_points=2).count()
        user.user_predicted_match_result = all_forecasts_by_user.filter(
            user_points=1).count()

        # Check are express forecasts successful or not.
        express_forecast_points = all_forecasts_by_user.filter(
            round_number=input_round_number,
            forecast_type="express"
        ).aggregate(Sum("user_points"))

        if express_forecast_points["user_points__sum"] is None:
            user.user_predicted_express += 0
            user.user_not_predicted_express += 0

        elif express_forecast_points["user_points__sum"] > 0:
            user.user_predicted_express += 1

        # else:
        elif express_forecast_points["user_points__sum"] == 0:
            user.user_not_predicted_express += 1

        user.save()


# Calculate points by each represented teams(groups) of Users.
def update_userteam_statistic_in_allteams():
    all_represented_teams = AllTeams.objects.all()
    users_statistics = FinalTable.objects.all()

    for team in all_represented_teams:
        points_by_all_team_memders = users_statistics.filter(
            user_team_name=team).aggregate(Sum("user_points"))
        team.team_points = points_by_all_team_memders["user_points__sum"]
        team.save()


# Ranked represented teams(groups) of Users by "points" & save ranks in DataBase.
def sort_allteams():
    all_represented_teams = AllTeams.objects.all().order_by("-team_points")

    rank = 1
    list_position = 0
    sorted_flag = False
    while not sorted_flag:

        if list_position <= (len(all_represented_teams) - 1):
            points_by_first_db_row = (
                all_represented_teams[list_position].team_points)
            teams_with_equal_points = all_represented_teams.filter(
                team_points=points_by_first_db_row)
            teams_with_equal_points.update(team_position=rank)
            rank += 1
            list_position += len(teams_with_equal_points)

        else:
            sorted_flag = True


# Ranked Users (exclude admin): first stage  by "points",
# after that by quantity of "predicted match score",
# after that by "average point per match", and
# save all ranks in DataBase.
def sort_fintable():
    users_statistics = FinalTable.objects.all().order_by(
        "-user_points",
        "-user_predicted_match_score",
        "-user_average_point_per_match"
    )

    rank = 1
    list_position = 0
    sorted_flag = False
    while not sorted_flag:

        if list_position <= (len(users_statistics) - 1):
            points_by_first_db_row = (
                users_statistics[list_position].user_points)
            users_with_equal_points = users_statistics.filter(
                user_points=points_by_first_db_row)

            # When more that one user has equal points quantity.
            if len(users_with_equal_points) > 1:
                predicted_match_score_by_first_db_row = (
                    users_with_equal_points[0].user_predicted_match_score)
                users_with_equal_predicted_match_score = (
                    users_with_equal_points.filter(user_predicted_match_score=(
                        predicted_match_score_by_first_db_row)))

                # When more that one user has equal predicted match scores.
                if len(users_with_equal_predicted_match_score) > 1:
                    user_average_point_per_match_by_first_db_row = (
                        users_with_equal_predicted_match_score[0].user_average_point_per_match)
                    users_with_equal_user_average_point_per_match = (
                        users_with_equal_predicted_match_score.filter(
                            user_average_point_per_match=(
                                user_average_point_per_match_by_first_db_row)))

                    # When more that one user has equal average points per match.
                    if len(users_with_equal_user_average_point_per_match) > 1:
                        users_with_equal_predicted_match_score.update(
                            user_position=rank)
                    else:
                        users_with_equal_user_average_point_per_match.update(
                            user_position=rank)
                        exclude_user = (
                            users_with_equal_user_average_point_per_match[0].user_id_id)
                        users_with_equal_predicted_match_score.exclude(
                            user_id_id=exclude_user).update(user_position=(rank+1))

                # Wen only one user has this predicted match scores.
                else:
                    users_with_equal_user_average_point_per_match.update(
                        user_position=rank)

                rank = rank + len(users_with_equal_predicted_match_score)
                list_position += len(users_with_equal_predicted_match_score)

            # Wen only one user has this points quantity.
            else:
                users_with_equal_points.update(user_position=rank)
                rank = rank + len(users_with_equal_points)
                list_position += len(users_with_equal_points)

        else:
            sorted_flag = True
