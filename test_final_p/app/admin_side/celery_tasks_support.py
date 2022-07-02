# Import all necessary moduls:
# 1) from Other packages.
from datetime import datetime

# 2) Local import.
from user_side.models import (
    ListOfMatches, ListOfUsersMatchForecast, CustomUser)
from .send_emails_support import (
    send_reminder_to_user, send_round_error_message_to_admin)
from .admin_side_support import looking_for_scores_of_matches_in_round


# Checking start time of each match in round, and send email reminder for Users
# who didn't make forecast for each match.
def done_forecasts_check():
    # Prepare data from DataBase (from tables: Users, Matches, Forecasts)
    matches_in_round = ListOfMatches.objects.filter(
        forecast_availability="yes")
    all_users = CustomUser.objects.exclude(
        username="admin").filter(send_reminder=1)
    users_forecasts = ListOfUsersMatchForecast.objects.all()

    # Check current time & convert to the timestamp
    current_datetime = datetime.now().replace(microsecond=0)
    current_datetime_ts = datetime.timestamp(current_datetime)

    # Start "check forecasts & send reminder" proccess for each match.
    for match in matches_in_round:
        match_datetime = datetime.combine(
            match.match_date, match.match_time)
        match_datetime_ts = datetime.timestamp(match_datetime)
        time_delta = match_datetime_ts - current_datetime_ts

        # Send reminder only for matches which start time less
        # than one hour from current time.
        if time_delta <= 3600 and time_delta > 0:

            for user in all_users:
                check_forecasts_by_user = users_forecasts.filter(
                    user_id_id=user.id, match_id=match.match_id)

                if not check_forecasts_by_user:
                    output_data = {
                        "user_name": user.username,
                        "user_email": user.email,
                        "match": match.teams_together
                    }
                    send_reminder_to_user(output_data)
                    print(match)
                    print(user)
                    print("send_reminder")


#
def logic_to_start_score_checking():
    # Checking current date & time.
    current_date_time = datetime.now().replace(microsecond=0)
    current_date_time_timestamp = datetime.timestamp(current_date_time)

    all_matches = ListOfMatches.objects.filter(
        forecast_availability="yes")

    # Allow process if available matches exist only.
    if all_matches:

        # Get date & time of latest match of active round, and convert its to the timestamp.
        round_latest_date = all_matches.latest('match_date', "match_time")
        round_latest_match_date_time = datetime.combine(
            round_latest_date.match_date, round_latest_date.match_time)
        round_latest_match_date_time_timestamp = datetime.timestamp(
            round_latest_match_date_time)

        # Statemet to start script or no.
        score_exist_list = []
        if current_date_time_timestamp < round_latest_match_date_time_timestamp:
            print("no time for looking_for_scores_of_matches_in_round")
            pass

        elif current_date_time_timestamp > round_latest_match_date_time_timestamp:
            print("start -- looking_for_scores_of_matches_in_round")
            for match in all_matches:
                # if match.home_team_result:
                if (match.home_team_result is not None and
                        match.visitor_team_result is not None):
                    score_exist_list.append("yes")

                else:
                    score_exist_list.append("no")

            # print(score_exist_list)
            check_list = ["yes", "no"]
            if set(check_list).issubset(score_exist_list):
                send_round_error_message_to_admin(
                    {"round_number": all_matches[0].round_number})

            elif "no" in set(score_exist_list):
                looking_for_scores_of_matches_in_round()
