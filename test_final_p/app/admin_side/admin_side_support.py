# Import all necessary moduls:
# 1) from Selenium package.
# from selenium import webdriver
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.common.by import By

# 2) from Django package.
from django.db.models import Sum
from django.core.mail import send_mail
from django.contrib.auth.models import User

# 3) from Other packages.
from bs4 import BeautifulSoup
from pathlib import Path
from datetime import datetime

# 4) Local import.
from user_side.models import (ListOfMatches, ListOfUsersMatchForecast,
                              FinalTable, AllTeams)


#
def looking_for_scores_of_matches_in_round():

    # ##! HEROKU (cloud server) options !##
    # # Setup options for "Google Chrome" by Heroku server.
    # options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    # options.add_argument("--no-sandbox")
    # options.add_argument("disable-dev-shm-usage")

    # # Select webdriver path and open browser.
    # webdriver_path = Path(Path.cwd(), "chromedriver")
    # wd = webdriver.Chrome(
    #     chrome_options=options, executable_path=webdriver_path)

    ##! PC (local server) options !##
    # Setup options for "Google Chrome" by local server.
    options = Options()
    options.add_argument('--headless')
    options.add_argument("--no-sandbox")

    # Select webdriver path and open browser
    webdriver_path = Path(Path.cwd(), "chromedriver")
    wd = Chrome(options=options, executable_path=webdriver_path)

    ##! Спільна частина !##
    # Link to the form which must be filled.
    page_link = "https://www.flashscore.com/football/"

    wd.get(page_link)
    wait = WebDriverWait(wd, 10)

    #
    eurocups_playing_days = ["Tuesday", "Wednesday", "Thursday", "1"]
    for day in eurocups_playing_days:
        # Click on calendar for move to previus day.
        calendar_select_yesterday1 = WebDriverWait(wd, 90).until(
            EC.element_to_be_clickable(
                (By.CLASS_NAME, "calendar__navigation--yesterday")
            )
        ).click()

        #
        raw_list_of_matches = WebDriverWait(wd, 90).until(
            EC.visibility_of_all_elements_located(
                (By.CLASS_NAME, "event__match--twoLine"))
        )

        matches_in_round = ListOfMatches.objects.filter(
            forecast_availability="yes")
        current_round = matches_in_round[0].round_numder

        #
        for match in matches_in_round:
            db_home_team = match.home_team
            db_visitor_team = match.visitor_team

            for ii in raw_list_of_matches:
                raw_matches_html = ii.get_attribute('innerHTML')
                raw_matches_soup = BeautifulSoup(raw_matches_html, "lxml")

                home_team_name = raw_matches_soup.select(
                    ".event__participant--home")

                #!  Запобіжник щоб зря не йти далі
                if home_team_name[0].text != db_home_team:
                    pass
                else:
                    visitor_team_name = raw_matches_soup.select(
                        ".event__participant--away")
                    # print("visitor_team_name", visitor_team_name[0].text)
                    home_team_score = raw_matches_soup.select(
                        ".event__score--home")
                    visitor_team_score = raw_matches_soup.select(
                        ".event__score--away")

                    if (home_team_name[0].text == db_home_team and
                            visitor_team_name[0].text == db_visitor_team):

                        #
                        home_team_score_isdigit_check = (
                            home_team_score[0].text.isdigit()
                        )
                        visitor_team_score_isdigit_check = (
                            visitor_team_score[0].text.isdigit()
                        )

                        if (not home_team_score_isdigit_check or
                                not visitor_team_score_isdigit_check):
                            print(
                                home_team_name[0].text,
                                visitor_team_name[0].text,
                                "--- SEND EMAIL TO ADMIN ---"
                            )
                            match_status = raw_matches_soup.select(
                                ".event__stage")[0].text
                            print("match_status", match_status)

                            match_data = {
                                "match_status": match_status,
                                "teams_together": home_team_name[0].text + " " + visitor_team_name[0].text
                            }
                            send_message_to_admin_email(match_data)
                        #
                        else:
                            # print(home_team_name[0].text, home_team_score[0].text,
                            #       visitor_team_score[0].text, visitor_team_name[0].text)

                            match.home_team_result = home_team_score[0].text
                            match.visitor_team_result = visitor_team_score[0].text
                            match.save()
                            print(db_home_team, " - ", db_visitor_team)
                            print("------")

    # Start proccess of calculation User points by forecasts.
    # func_calculate_points_by_user_forecasts()


#
def func_calculate_points_by_user_forecasts():
    input_matches_in_round = ListOfMatches.objects.filter(
        forecast_availability="yes")
    input_round_numder = input_matches_in_round[0].round_numder

    all_forecasts = ListOfUsersMatchForecast.objects.filter(
        round_numder=input_round_numder)

    list_of_user_hwo_did_forecast = all_forecasts.values("user_id").distinct()

    # Calculate points proccess (from User point of view).
    for user in list_of_user_hwo_did_forecast:
        forecasts_by_user = all_forecasts.filter(
            user_id=user["user_id"], round_numder=input_round_numder)

        for forecast in forecasts_by_user:

            results = input_matches_in_round.filter(
                match_id=forecast.match_id)

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

    # Updating whole statistic information:
    # 1) about "User" inside "Fintable".
    update_user_statistic_in_fintab()

    # 2) about "Teams" inside "Allteams".
    update_userteam_statistic_in_allteams()


#
def print_time():
    current_date_time = datetime.now().replace(microsecond=0)
    current_date_time_timestamp = datetime.timestamp(current_date_time)
    # print(current_date_time)
    # print(current_date_time_timestamp)
    xxx = ListOfMatches.objects.filter(
        forecast_availability="yes")

    # for ii in xxx:
    #     print("xxx -- home_team_result", ii.home_team_result)
    #     print("xxx -- visitor_team_result", ii.visitor_team_result)

    xxx2 = xxx.filter(home_team_result__isnull=True,
                      visitor_team_result__isnull=True)
    # print(xxx2)
    # if xxx2.exists():
    #     for ii in xxx2:
    #         print("xxx2 - home_team_result", ii.home_team_result)
    #         print("xxx2 - visitor_team_result", ii.visitor_team_result)
    # else:
    #     print("not exist")

    my_date = xxx.latest('match_date', "match_time")

    match_date_time = datetime.combine(
        my_date.match_date, my_date.match_time)
    match_date_time_timestamp = datetime.timestamp(match_date_time)
    # print(match_date_time)
    # print(match_date_time_timestamp)
    score_exist_list = []
    if current_date_time_timestamp < match_date_time_timestamp:
        print("не час")
    elif current_date_time_timestamp > match_date_time_timestamp:
        print("Вже час уууррррааааа")
        for match in xxx:
            print(match)
            if match.home_team_result:
                score_exist_list.append("yes")
            else:
                score_exist_list.append("no")
        print(score_exist_list)
        if "no" in score_exist_list:
            print("no in score_exist_list")
            looking_for_scores_of_matches_in_round()
        else:
            print("--- pass ---")
            pass


#
def open_round_for_users_forecast(number_of_round):
    # Get all matches from DB, and separated its for two parts:
    # firts - will be available for the forecast, second - not available.
    all_matches = ListOfMatches.objects.all()
    matches_in_selected_round = all_matches.filter(
        round_numder=number_of_round)
    other_matches = all_matches.exclude(
        round_numder=number_of_round)

    # Updated "forecast_availability" attribute inside all matches in DB.
    matches_in_selected_round.update(forecast_availability="yes")
    other_matches.update(forecast_availability="no")


# Reset values in DataBase tables to the default.
def reset_db_values_to_default():
    # By "user_points" attribute of "ListOfUsersMatchForecast".
    all_forecasts_by_users = ListOfUsersMatchForecast.objects.all()
    all_forecasts_by_users.update(user_points=None)

    # By "user_points" of "FinalTable".
    all_users_statistic = FinalTable.objects.all()
    all_users_statistic.update(
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
def update_user_statistic_in_fintab():
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
            user.user_average_point_per_match = round((total_points_sum["user_points__sum"] /
                                                       forecasted_matches), 2)
        except TypeError:
            user.user_average_point_per_match = 0

        user.user_all_predicted_matches = forecasted_matches
        user.user_predicted_match_score = all_forecasts_by_user.filter(
            user_points=2).count()
        user.user_predicted_match_result = all_forecasts_by_user.filter(
            user_points=1).count()
        user.user_predicted_express = "11"
        user.user_not_predicted_express = "11"
        user.save()


#
def send_message_to_admin_email(input_data):
    admin_emal = "cozak@meta.ua"
    send_mail(
        f"Щось трапилося з матчем '{input_data['teams_together']}',",
        f"матч був '{input_data['match_status']}'",
        "karbivnychyi.volodymyr@gmail.com",
        [admin_emal],
        fail_silently=False,
    )


#
def update_userteam_statistic_in_allteams():
    all_represented_teams = AllTeams.objects.all()
    users_statistics = FinalTable.objects.all()

    for team in all_represented_teams:
        xx = users_statistics.filter(
            user_team_name=team).aggregate(Sum("user_points"))
        team.team_points = xx["user_points__sum"]
        team.save()


#
def sort_allteams():
    all_represented_teams = AllTeams.objects.all().order_by("-team_points")

    rank = 1
    list_position = 0
    sorted_flag = False
    while not sorted_flag:
        if list_position <= (len(all_represented_teams) - 1):
            points_by_first_db_row = all_represented_teams[list_position].team_points
            teams_with_equal_points = all_represented_teams.filter(
                team_points=points_by_first_db_row)
            teams_with_equal_points.update(team_position=rank)
            rank += 1
            list_position += len(teams_with_equal_points)
        else:
            sorted_flag = True


#
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
            points_by_first_db_row = users_statistics[list_position].user_points
            users_with_equal_points = users_statistics.filter(
                user_points=points_by_first_db_row)

            if len(users_with_equal_points) > 1:
                predicted_match_score_by_first_db_row = users_with_equal_points[
                    0].user_predicted_match_score
                users_with_equal_predicted_match_score = users_with_equal_points.filter(
                    user_predicted_match_score=predicted_match_score_by_first_db_row)

                # users_with_equal_predicted_match_score.update(
                #     user_position=rank)
                # rank = rank + len(users_with_equal_predicted_match_score)

                if len(users_with_equal_predicted_match_score) > 1:
                    user_average_point_per_match_by_first_db_row = users_with_equal_predicted_match_score[
                        0].user_average_point_per_match
                    users_with_equal_user_average_point_per_match = users_with_equal_predicted_match_score.filter(
                        user_average_point_per_match=user_average_point_per_match_by_first_db_row)

                    if len(users_with_equal_user_average_point_per_match) > 1:
                        users_with_equal_predicted_match_score.update(
                            user_position=rank)
                    else:
                        users_with_equal_user_average_point_per_match.update(
                            user_position=rank)
                        exclude_user = users_with_equal_user_average_point_per_match[0].user_id_id
                        users_with_equal_predicted_match_score.exclude(
                            user_id_id=exclude_user).update(user_position=(rank+1))
                    # rank = rank + len(users_with_equal_predicted_match_score)
                    # list_position += len(users_with_equal_predicted_match_score)

                else:
                    users_with_equal_user_average_point_per_match.update(
                        user_position=rank)

                rank = rank + len(users_with_equal_predicted_match_score)
                list_position += len(users_with_equal_predicted_match_score)

            else:
                users_with_equal_points.update(user_position=rank)
                rank = rank + len(users_with_equal_points)
                list_position += len(users_with_equal_points)

            # users_with_equal_points.update(user_position=rank)
            # rank += 1
            # list_position += len(users_with_equal_points)

        else:
            sorted_flag = True


#
def every_hour_done_forecasts_check():
    current_date_time = datetime.now().replace(microsecond=0)
    current_date_time_timestamp = datetime.timestamp(current_date_time)
    # print(current_date_time)
    # print(current_date_time_timestamp)
    matches_in_round = ListOfMatches.objects.filter(
        forecast_availability="yes")

    match_datetimes = matches_in_round.earliest('match_date', "match_time")
    print(match_datetimes.match_date, match_datetimes.match_time)

    xxx = matches_in_round.filter(
        match_date=match_datetimes.match_date, match_time=match_datetimes.match_time)
    for ii in xxx:
        print(ii)

    all_users = User.objects.exclude(username="admin")

    # for ii in all_users:
    #     print(ii)
    pass
