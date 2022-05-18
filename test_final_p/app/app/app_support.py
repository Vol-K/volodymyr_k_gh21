from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from user_side.models import AllTeams, ListOfMatches, ListOfUsersMatchForecast, FinalTable

# User email validation.


def validate_user_emal(email_to_validate):
    validator = EmailValidator(allowlist=["gmail.com", "localhost"])
    try:
        validator(email_to_validate)
        return True
    except ValidationError:
        return False


#
def initialize_new_user_in_fintab(user_data):
    user_in_fintab = FinalTable()
    user_in_fintab.user_id = user_data["user_id"]
    user_in_fintab.user_name = user_data["user_login"]
    user_in_fintab.user_position = 0
    user_in_fintab.user_points = 0
    user_in_fintab.user_potential_points = 0
    user_in_fintab.user_average_point_per_match = 0
    user_in_fintab.user_all_predicted_matches = 0
    user_in_fintab.user_predicted_match_score = 0
    user_in_fintab.user_predicted_express = 0
    user_in_fintab.user_predicted_match_result = 0
    user_in_fintab.user_predicted_express = 0
    user_in_fintab.user_not_predicted_express = 0
    user_in_fintab.user_achive_guru_turu = 0
    user_in_fintab.user_team_name = ""
    user_in_fintab.save()


# Addecd user to the all tables in the DB.
def add_user_to_all_tables(user_data):
    new_user = User.objects.create_user(user_data["user_login"],
                                        user_data["user_email"],
                                        user_data["user_pass"])
    user_info = {"user_login": new_user.username, "user_id": new_user.id}
    add_user_to_fintab = initialize_new_user_in_fintab(user_info)

    return new_user
