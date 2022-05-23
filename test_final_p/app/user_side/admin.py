from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth.models import User, Group

from .models import (AllTeams, ListOfMatches, FinalTable,
                     ListOfUsersMatchForecast)

from etc.admin import CustomModelPage
from django.db import models


#! типу працює, треба думати над рендером кнопок та іншого
class MyPage(CustomModelPage):
    title = 'My custom page'

    # Define some fields you want to proccess data from.
    my_field = models.CharField('some title', max_length=10)
    my_field_2 = models.CharField('some title', max_length=10)

    my_field_3 = models.CharField('some title', max_length=10)

    def save(self):
        # Here implement data handling.
        super().save()


# Register the page within Django admin.
MyPage.register()


#! Спроба номер два
class YourCustomAdminSite(admin.AdminSite):
    pass


#
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username",  "first_name",
                    "last_name", "email", "is_staff", "is_superuser", "last_login")
    list_filter = ("last_login",)
    search_fields = ("username", "id", "last_login")
    list_display_links = ("username",)


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
    list_filter = ("round_numder",)
    search_fields = ("teams_together", "visitor_team",
                     "home_team", "match_date")
    list_display_links = ("teams_together",)


#
class ListOfUsersMatchForecastAdmin(admin.ModelAdmin):
    list_display = ("match_id", "user_id", "teams_together",
                    "home_team_forecast", "visitor_team_forecast",
                    "round_numder", "user_points", "forecast_type",
                    "match_in_round")
    exclude = ("forecast_id",)
    list_filter = ("round_numder", "user_points")
    search_fields = ("teams_together", "forecast_type")
    list_display_links = ("teams_together",)


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


# Registering all models:
# First - its customizing 'Admin' page views.
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.unregister(Group)

# And other models.
admin.site.register(AllTeams, AllTeamsAdmin)
admin.site.register(ListOfMatches, ListOfMatchesAdmin)
admin.site.register(ListOfUsersMatchForecast, ListOfUsersMatchForecastAdmin)
admin.site.register(FinalTable, FinalTableAdmin)
