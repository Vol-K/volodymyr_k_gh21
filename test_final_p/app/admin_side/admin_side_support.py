from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup
from pathlib import Path
# from time import sleep
from datetime import datetime


from user_side.models import ListOfMatches, ListOfUsersMatchForecast


#
def func_calculate_points_by_user_forecasts():
    # options = ChromeOptions()
    options = Options()

    # options.headless = True
    options.add_argument('--headless')
    options.add_argument("--no-sandbox")

    # Link to the form which must be filled.a
    page_link = "https://www.flashscore.com/football/"
    # print(Path(Path.cwd()))
    # Select webdriver path and open browser
    webdriver_path = Path(Path.cwd(), "chromedriver")
    # webdriver_path = Path(Path.cwd(), "norlys", "chromedriver")

    wd = Chrome(options=options, executable_path=webdriver_path)

    wd.get(page_link)
    wait = WebDriverWait(wd, 10)

    # Click on calendar for move to previus day.
    calendar_select_yesterday1 = WebDriverWait(wd, 90).until(EC.element_to_be_clickable(
        (By.CLASS_NAME, "calendar__navigation--yesterday"))).click()

    calendar_select_yesterday1 = WebDriverWait(wd, 90).until(EC.element_to_be_clickable(
        (By.CLASS_NAME, "calendar__navigation--yesterday"))).click()

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

    print("The End falks")


# def procces_delayed():
def print_time():
    xxx = datetime.now().replace(microsecond=0)
    xxx_timestamp = datetime.timestamp(xxx)
    my_date = "2022-06-05 22:45:59"
    my_date_timestamp = datetime.timestamp(
        datetime.strptime(my_date, "%Y-%m-%d %H:%M:%S"))
    if xxx_timestamp < my_date_timestamp:
        print("не час")
    elif xxx_timestamp > my_date_timestamp:
        print("Вже час уууррррааааа")
    # print("18:50", xxx)
