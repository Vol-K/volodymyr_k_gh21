# Import all necessary moduls:
# 1) from Django package
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group  # , User

# 2) Local import.
from .models import (AllTeams, ListOfMatches, FinalTable,
                     ListOfUsersMatchForecast, CustomUser)


# Setting all options for fields by model "CustomUser".
class CustomUserAdmin(UserAdmin):
    list_display = ("id", "username", "email",
                    "is_staff", "is_superuser", "last_login", "send_reminder")
    exclude = ("password", )
    list_filter = ("last_login",)
    search_fields = ("username", "id", "last_login")
    list_display_links = ("username",)
    readonly_fields = ("id", "username", "first_name", "last_name", "email",
                       "last_login", "date_joined", "groups", "user_permissions")


# Setting all options for fields by model "AllTeams".
class AllTeamsAdmin(admin.ModelAdmin):
    list_display = ("team_name", "team_points", "team_position")
    exclude = ("team_id",)
    readonly_fields = ("team_points", "team_position")


# Setting all options for fields by model "ListOfMatches".
class ListOfMatchesAdmin(admin.ModelAdmin):
    list_display = ("round_number", "home_team", "visitor_team",
                    "teams_together", "match_date", "match_time",
                    "home_team_result", "visitor_team_result")
    exclude = ("match_id", "match_in_round",
               "teams_together", "forecast_availability")
    list_filter = ("round_number",)
    search_fields = ("teams_together", "visitor_team",
                     "home_team", "match_date")
    list_display_links = ("teams_together",)


# Setting all options for fields by model "ListOfUsersMatchForecast".
class ListOfUsersMatchForecastAdmin(admin.ModelAdmin):
    list_display = ("match_id", "user_id", "teams_together",
                    "home_team_forecast", "visitor_team_forecast",
                    "round_number", "user_points", "forecast_type",
                    "match_in_round")
    exclude = ("forecast_id",)
    list_filter = ("round_number", "user_points")
    search_fields = ("teams_together", "forecast_type")
    list_display_links = ("teams_together",)


# Setting all options for fields by model "FinalTable".
class FinalTableAdmin(admin.ModelAdmin):
    list_display = ("user_id", "user_position", "user_points",
                    "user_potential_points", "user_average_point_per_match",
                    "user_all_predicted_matches", "user_predicted_match_score",
                    "user_predicted_match_result", "user_predicted_express",
                    "user_not_predicted_express", "user_achive_guru_turu",
                    "user_team_name")
    exclude = ("id",)
    search_fields = ("user_name",)
    readonly_fields = ("user_id", "user_name", "user_position", "user_points",
                       "user_potential_points", "user_average_point_per_match",
                       "user_all_predicted_matches",
                       "user_predicted_match_score",
                       "user_predicted_match_result", "user_predicted_express",
                       "user_not_predicted_express",
                       )


# First of all - its customizing 'Admin' page views.
# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
admin.site.register(CustomUser, CustomUserAdmin)

# And after, registed all models.
admin.site.register(AllTeams, AllTeamsAdmin)
admin.site.register(ListOfMatches, ListOfMatchesAdmin)
admin.site.register(ListOfUsersMatchForecast, ListOfUsersMatchForecastAdmin)
admin.site.register(FinalTable, FinalTableAdmin)
