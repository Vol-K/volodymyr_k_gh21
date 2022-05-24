from django.db import models
from requests import options


# List of Teams (band of users).
class AllTeams(models.Model):
    team_id = models.BigAutoField(
        auto_created=True, primary_key=True, serialize=False,
        verbose_name="Team ID")
    team_name = models.CharField(max_length=25)
    team_points = models.PositiveIntegerField(default=0, blank=True)
    team_position = models.PositiveIntegerField(default=0, blank=True)

    class Meta:
        verbose_name_plural = "Команди (учасників)"


# List of all matches.
class ListOfMatches(models.Model):
    match_id = models.BigAutoField(
        auto_created=True, primary_key=True, serialize=False,
        verbose_name="Match ID")
    round_numder = models.PositiveIntegerField(default=1)
    match_in_round = models.PositiveIntegerField(default=1)
    home_team = models.CharField(max_length=20, default="")
    visitor_team = models.CharField(max_length=20, default="")
    teams_together = models.CharField(max_length=41, default="")
    match_date = models.DateField(auto_now=False, auto_now_add=False)
    match_time = models.TimeField(auto_now=False, auto_now_add=False,)
    forecast_availability = models.CharField(max_length=3)
    home_team_result = models.PositiveIntegerField(null=True, blank=True)
    visitor_team_result = models.PositiveIntegerField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.teams_together = self.home_team + " - " + self.visitor_team
        super(ListOfMatches, self).save(*args, **kwargs)

    def __str__(self):
        return self.teams_together

    class Meta:
        verbose_name_plural = "Список мітчів"


# List of user match predicted.
class ListOfUsersMatchForecast(models.Model):
    forecast_id = models.BigAutoField(
        auto_created=True, primary_key=True, serialize=False,
        verbose_name="Forecast ID")
    match_id = models.PositiveIntegerField()
    user_id = models.PositiveIntegerField()
    teams_together = models.CharField(max_length=41, default="")
    home_team_forecast = models.PositiveIntegerField()
    visitor_team_forecast = models.PositiveIntegerField()
    round_numder = models.PositiveIntegerField(default=1)
    forecast_time = models.DateTimeField(auto_now_add=True)
    user_points = models.PositiveIntegerField(null=True, blank=True)
    forecast_type = models.CharField(max_length=7)
    match_in_round = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.teams_together

    class Meta:
        verbose_name_plural = "Прогнози всіх користувачів"


# Final table (table of user forecast results).
class FinalTable(models.Model):
    user_id = models.PositiveIntegerField()
    user_name = models.CharField(max_length=25)
    user_position = models.PositiveIntegerField(default=0, blank=True)
    user_points = models.PositiveIntegerField(default=0)
    user_potential_points = models.PositiveIntegerField(default=0)
    user_average_point_per_match = models.FloatField(default=0.0)
    user_all_predicted_matches = models.PositiveIntegerField(default=0)
    user_predicted_match_score = models.PositiveIntegerField(default=0)
    user_predicted_match_result = models.PositiveIntegerField(default=0)
    user_predicted_express = models.PositiveIntegerField(default=0)
    user_not_predicted_express = models.PositiveIntegerField(default=0)
    user_achive_guru_turu = models.PositiveIntegerField(default=0)
    user_team_name = models.CharField(max_length=25, blank=True)

    class Meta:
        verbose_name_plural = "Підсумкова таблиця"
