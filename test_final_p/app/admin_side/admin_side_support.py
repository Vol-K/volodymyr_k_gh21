from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.common.by import By

from django.db.models import Sum

from bs4 import BeautifulSoup
from pathlib import Path
# from time import sleep
from datetime import datetime


from user_side.models import (ListOfMatches, ListOfUsersMatchForecast,
                              FinalTable)


#
def func_calculate_points_by_user_forecasts():
    # options = ChromeOptions()
    options = Options()
    options.add_argument('--headless')
    options.add_argument("--no-sandbox")

    # Select webdriver path and open browser
    webdriver_path = Path(Path.cwd(), "chromedriver")
    wd = Chrome(options=options, executable_path=webdriver_path)

    # Link to the form which must be filled.a
    page_link = "https://www.flashscore.com/football/"

    wd.get(page_link)
    wait = WebDriverWait(wd, 10)

    #
    eurocups_playing_days = ["Tuesday", "Wednesday", "Thursday"]
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
            # print(raw_matches_soup)
            home_team_name = raw_matches_soup.select(
                ".event__participant--home")
            # print(home_team_name[0].text)

            #!  Запобіжник щоб зря не йти далі
            #!
            visitor_team_name = raw_matches_soup.select(
                ".event__participant--away")
            home_team_score = raw_matches_soup.select(
                ".event__score--home")
            visitor_team_score = raw_matches_soup.select(
                ".event__score--away")
            if home_team_name[0].text == db_home_team and visitor_team_name[0].text == db_visitor_team:
                print(home_team_name[0].text, home_team_score[0].text,
                      visitor_team_score[0].text, visitor_team_name[0].text)

                match.home_team_result = home_team_score[0].text
                match.visitor_team_result = visitor_team_score[0].text
                match.save()
                break
            print("------")

    #!
    #! Блок саме для реального обрахунку результатів.
    all_forecasts = ListOfUsersMatchForecast.objects.filter(
        round_numder=current_round)

    list_of_user_hwo_did_forecast = all_forecasts.values("user_id").distinct()

    # Calculate points proccess (per User view).
    for user in list_of_user_hwo_did_forecast:
        forecasts_by_user = all_forecasts.filter(
            user_id=user["user_id"], round_numder=current_round)

        for forecast in forecasts_by_user:

            results = matches_in_round.filter(match_id=forecast.match_id)

            home_team_score = results[0].home_team_result
            visitor_team_score = results[0].visitor_team_result
            # print(results[0].home_team_result, results[0].visitor_team_result)

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

        # print(user["user_id"])
    update_user_statistic_in_fintab()
    print("The End falks")


# def procces_delayed():
def print_time():
    xxx = datetime.now().replace(microsecond=0)
    print(xxx)
    xxx_timestamp = datetime.timestamp(xxx)
    my_date = "2022-06-06 22:45:59"
    my_date_timestamp = datetime.timestamp(
        datetime.strptime(my_date, "%Y-%m-%d %H:%M:%S"))
    if xxx_timestamp < my_date_timestamp:
        print("не час")
    elif xxx_timestamp > my_date_timestamp:
        print("Вже час уууррррааааа")
    # print("18:50", xxx)


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


#
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
        user.user_points = total_points_sum["user_points__sum"]
        user.user_potential_points = forecasted_matches * 2
        user.user_average_point_per_match = total_points_sum["user_points__sum"] / \
            forecasted_matches
        user.user_all_predicted_matches = forecasted_matches
        user.user_predicted_match_score = all_forecasts_by_user.filter(
            user_points=2).count()
        user.user_predicted_match_result = all_forecasts_by_user.filter(
            user_points=1).count()
        user.user_predicted_express = "11"
        user.user_not_predicted_express = "11"
        user.save()

    print("DONE")
