# Import all necessary moduls:
# 1) from Django package.
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator

# User email validation.
def validate_user_emal(email_to_validate):
    validator = EmailValidator(allowlist=["gmail.com", "ukr.net", "meta.ua"])
    try:
        validator(email_to_validate)
        return True
    except ValidationError:
        return False


# Add "New User" to the DataBase (inside "Fintab" table).
def initialize_new_user_in_fintab(user_data):
    # Func nessesary import (to prevent circular imports)
    from user_side.models import FinalTable, CustomUser

    # Create a User instance.
    new_user_instance = CustomUser.objects.filter(id=user_data["user_id"])

    # Initialize a model
    user_in_fintab = FinalTable()
    # Inserting data and after that it's save to DB.
    user_in_fintab.user_id = new_user_instance[0]
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
    # Func nessesary import (to prevent circular imports)
    from user_side.models import CustomUser

    new_user = CustomUser.objects.create_user(user_data["user_login"],
                                              user_data["user_email"],
                                              user_data["user_pass"])
    user_info = {"user_login": new_user.username, "user_id": new_user.id}
    add_user_to_fintab = initialize_new_user_in_fintab(user_info)

    return new_user


# Prepare & create a dynamic "choices" dropdaown list for "FinTable" model.
def custom_choices():
    # Func nessesary import (to prevent circular imports)
    from user_side.models import AllTeams

    all_teams_in_db = AllTeams.objects.all().values_list("team_name")
    all_teams_in_db = list(all_teams_in_db)
    user_team_choices = []
    for team in all_teams_in_db:
        user_team_choices.append((team[0], team[0]))
    user_team_choices = tuple(user_team_choices)

    return user_team_choices
