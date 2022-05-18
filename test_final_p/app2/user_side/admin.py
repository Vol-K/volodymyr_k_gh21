from django.contrib import admin
from .models import (AllUsers, AllTeams, ListOfMatches, FinalTable,
                     ListOfUsersMatchForecast)


#
class AllUsersAdmin(admin.ModelAdmin):
    list_display = ("user_id", "user_name")


class AllTeamsAdmin(admin.ModelAdmin):
    list_display = ("team_name", "team_points", "team_position")


class ListOfMatchesAdmin(admin.ModelAdmin):
    list_display = ("round_numder", "match_in_round", "home_team",
                    "visitor_team", "teams_together", "match_date",
                    "match_time", "forecast_availability", "home_team_result",
                    "visitor_team_result")


class ListOfUsersMatchForecastAdmin(admin.ModelAdmin):
    list_display = ("match_id", "user_id", "teams_together",
                    "home_team_forecast", "visitor_team_forecast",
                    "round_numder", "user_points", "forecast_type",
                    "match_in_round")


class FinalTableAdmin(admin.ModelAdmin):
    list_display = ("user_name", "user_position", "user_points",
                    "user_potential_points", "user_average_point_per_match",
                    "user_all_predicted_matches", "user_predicted_match_score",
                    "user_predicted_match_result", "user_predicted_express",
                    "user_not_predicted_express", "user_achive_guru_tutu",
                    "user_team_name")


# Registering all models.
admin.site.register(AllUsers, AllUsersAdmin)
admin.site.register(AllTeams, AllTeamsAdmin)
admin.site.register(ListOfMatches, ListOfMatchesAdmin)
admin.site.register(ListOfUsersMatchForecast, ListOfUsersMatchForecastAdmin)
admin.site.register(FinalTable, FinalTableAdmin)
