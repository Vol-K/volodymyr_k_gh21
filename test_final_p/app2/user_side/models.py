from django.db import models
from requests import options


# Create your models here.
# List of all users.
class AllUsers(models.Model):
    user_id = models.PositiveIntegerField()
    user_name = models.CharField(max_length=25)
    pass_hash = models.CharField(max_length=94)


# List of Teams (band of users).
class AllTeams(models.Model):
    team_id = models.PositiveIntegerField()
    team_name = models.CharField(max_length=25)
    team_points = models.PositiveIntegerField(default=0)
    team_position = models.PositiveIntegerField(default=0)


# List of all matches.
class ListOfMatches(models.Model):
    match_id = models.PositiveIntegerField()
    round_numder = models.PositiveIntegerField(default=1)
    match_in_round = models.PositiveIntegerField(default=1)
    home_team = models.CharField(max_length=20, default="")
    visitor_team = models.CharField(max_length=20, default="")
    teams_together = models.CharField(max_length=41, default="")
    match_date = models.CharField(max_length=10)
    match_time = models.CharField(max_length=5)
    forecast_availability = models.CharField(max_length=3)
    home_team_result = models.PositiveIntegerField()
    visitor_team_result = models.PositiveIntegerField()


# List of user match predicted.
class ListOfUsersMatchForecast(models.Model):
    forecast_id = models.PositiveIntegerField()
    match_id = models.PositiveIntegerField()
    user_id = models.PositiveIntegerField()
    teams_together = models.CharField(max_length=41, default="")
    home_team_forecast = models.PositiveIntegerField()
    visitor_team_forecast = models.PositiveIntegerField()
    round_numder = models.PositiveIntegerField(default=1)
    forecast_time = models.CharField(max_length=9)
    user_points = models.PositiveIntegerField()
    forecast_type = models.CharField(max_length=7)
    match_in_round = models.PositiveIntegerField(default=1)


# Final table (table of user forecast results).
class FinalTable(models.Model):
    user_id = models.PositiveIntegerField()
    user_name = models.CharField(max_length=25)
    user_position = models.PositiveIntegerField(default=0)
    user_points = models.PositiveIntegerField(default=0)
    user_potential_points = models.PositiveIntegerField(default=0)
    user_average_point_per_match = models.FloatField(default=0.0)
    user_all_predicted_matches = models.PositiveIntegerField(default=0)
    user_predicted_match_score = models.PositiveIntegerField(default=0)
    user_predicted_match_result = models.PositiveIntegerField(default=0)
    user_predicted_express = models.PositiveIntegerField(default=0)
    user_not_predicted_express = models.PositiveIntegerField(default=0)
    user_achive_guru_tutu = models.PositiveIntegerField(default=0)
    user_team_name = models.CharField(max_length=25)
