from django.contrib import admin
# from django.contrib.auth.models import User

from .models import (AllUsers, AllTeams, ListOfMatches, FinalTable,
                     ListOfUsersMatchForecast)


#
class CustomPageAdmin(admin.AdminSite):
    pass


#
class AllUsersAdmin(admin.ModelAdmin):
    list_display = ("user_name",)
    exclude = ("user_id", "pass_hash")
    search_fields = ("user_name",)
    readonly_fields = ("user_id", "user_name", )


#
class AllTeamsAdmin(admin.ModelAdmin):
    list_display = ("team_name", "team_points", "team_position")
    exclude = ("team_id",)
    # readonly_fields = ("team_name", "team_points", "team_position")


#
class ListOfMatchesAdmin(admin.ModelAdmin):
    list_display = ("round_numder", "match_in_round", "home_team",
                    "visitor_team", "teams_together", "match_date",
                    "match_time", "forecast_availability", "home_team_result",
                    "visitor_team_result")
    exclude = ("match_id", "teams_together")
    search_fields = ("teams_together", "visitor_team",
                     "home_team", "match_date")


#
class ListOfUsersMatchForecastAdmin(admin.ModelAdmin):
    list_display = ("match_id", "user_id", "teams_together",
                    "home_team_forecast", "visitor_team_forecast",
                    "round_numder", "user_points", "forecast_type",
                    "match_in_round")
    exclude = ("forecast_id",)
    search_fields = ("teams_together", "forecast_type")


#
class FinalTableAdmin(admin.ModelAdmin):
    list_display = ("user_name", "user_position", "user_points",
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
                       "user_not_predicted_express", "user_achive_guru_turu",
                       "user_team_name")


class MyAdminSite(admin.AdminSite):
    def get_app_list(self, request):
        app_list = super().get_app_list(request)
        app_list += [
            {
                "name": "My Custom App",
                "app_label": "my_test_app",
                # "app_url": "/admin/test_view",
                "models": [
                    {
                        "name": "tcptraceroute",
                        "object_name": "tcptraceroute",
                        "admin_url": "/admin/test_view",
                        "view_only": True,
                    }
                ],
            }
        ]
        return app_list


# Registering all models.
admin.site.register(AllUsers, AllUsersAdmin)
admin.site.register(AllTeams, AllTeamsAdmin)
admin.site.register(ListOfMatches, ListOfMatchesAdmin)
admin.site.register(ListOfUsersMatchForecast, ListOfUsersMatchForecastAdmin)
admin.site.register(FinalTable, FinalTableAdmin)
