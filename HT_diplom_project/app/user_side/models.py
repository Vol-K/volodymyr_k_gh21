# Import all necessary moduls:
# 1) from Django package.
from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import AbstractUser

# 2) Local import.
from app.app_support import custom_choices


# Modify User model.
class CustomUser(AbstractUser):
    send_reminder = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Зареєстровані Користувачі"
        verbose_name_plural = "Зареєстровані Користувачі"


# List of Teams (band of users).
class AllTeams(models.Model):
    team_id = models.BigAutoField(
        auto_created=True, primary_key=True, serialize=False,
        verbose_name="Team ID")
    team_name = models.CharField(max_length=25)
    team_points = models.PositiveIntegerField(
        default=0,
        blank=True,
    )
    team_position = models.PositiveIntegerField(default=0, blank=True)

    def __str__(self):
        return self.team_name

    class Meta:
        verbose_name = "Команди (учасників)"
        verbose_name_plural = "Команди (учасників)"


# List of all matches.
class ListOfMatches(models.Model):
    match_id = models.BigAutoField(
        auto_created=True, primary_key=True, serialize=False,
        verbose_name="Match ID")
    round_number = models.PositiveIntegerField(default=1)
    match_in_round = models.PositiveIntegerField(default=1)
    home_team = models.CharField(max_length=20, default="")
    visitor_team = models.CharField(max_length=20, default="")
    teams_together = models.CharField(max_length=41, default="")
    match_date = models.DateField(auto_now=False, auto_now_add=False)
    match_time = models.TimeField(auto_now=False, auto_now_add=False,)
    forecast_availability = models.CharField(max_length=3, default="no")
    home_team_result = models.PositiveIntegerField(null=True, blank=True)
    visitor_team_result = models.PositiveIntegerField(null=True, blank=True)

    # Modifyed "teams_together" & "match_in_round" fields.
    def save(self, *args, **kwargs):
        self.teams_together = self.home_team + " - " + self.visitor_team

        # Get number of last match in round.
        def counter_match_in_round(inside_round_number):
            last_match_in_round_number = ListOfMatches.objects.filter(
                round_number=inside_round_number).count()
            return last_match_in_round_number

        last_match_in_round = counter_match_in_round(self.round_number)
        if not last_match_in_round:
            self.match_in_round = 1
        else:
            self.match_in_round = last_match_in_round + 1

        super(ListOfMatches, self).save(*args, **kwargs)

    def __str__(self):
        return self.teams_together

    class Meta:
        verbose_name = "Список матчів"
        verbose_name_plural = "Список матчів"


# List of users all matches predicted.
class ListOfUsersMatchForecast(models.Model):
    forecast_id = models.BigAutoField(
        auto_created=True, primary_key=True, serialize=False,
        verbose_name="Forecast ID")
    match_id = models.ForeignKey(ListOfMatches, on_delete=models.CASCADE)
    user_id = models.ForeignKey(
        CustomUser, on_delete=models.DO_NOTHING, related_name="user_forecasts")
    teams_together = models.CharField(max_length=41, default="")
    home_team_forecast = models.PositiveIntegerField()
    visitor_team_forecast = models.PositiveIntegerField()
    round_number = models.PositiveIntegerField(default=1)
    forecast_time = models.DateTimeField(auto_now_add=True)
    user_points = models.PositiveIntegerField(null=True, blank=True)
    forecast_type = models.CharField(max_length=9)
    match_in_round = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.teams_together

    class Meta:
        verbose_name = "Прогнози всіх учасників"
        verbose_name_plural = "Прогнози всіх учасників"


# Final table (table of user forecast results).
class FinalTable(models.Model):

    # Prepare empty "choices" instanse for the further update.
    user_team_choices = ()

    user_id = models.ForeignKey(
        CustomUser, on_delete=models.DO_NOTHING, related_name="user_fintable")
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
    user_team_name = models.CharField(
        max_length=225, blank=True, choices=user_team_choices)

    # Create a dynamic "choices" dropdaown list (based on "AllTeams" model).
    def __init__(self, *args, **kwargs):
        super(FinalTable, self).__init__(*args, **kwargs)
        self._meta.get_field(
            "user_team_name").choices = custom_choices()

    def __str__(self):
        return self.user_name

    class Meta:
        verbose_name = "Підсумкова таблиця"
        verbose_name_plural = "Підсумкова таблиця"
