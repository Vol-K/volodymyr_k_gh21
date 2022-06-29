# Import all necessary moduls:
# 1) from Django package.
from django.urls import path

# 2) Local import.
from . import views


# List of supported urls of application.
urlpatterns = [
    path("index.html", views.index, name="index_adress"),
    path("", views.index, name="blank_index_adress"),
    path("teams-and-members.html",
         views.teams_and_members, name="teams_and_members"),
    path("forecast-by-other.html",
         views.forecast_by_other, name="forecast_by_other"),
    path("fintable.html",
         views.fintable, name="fintable"),
    path("make-forecast.html",
         views.make_forecast, name="make_forecast"),
    path("change-forecast.html",
         views.change_forecast, name="make_forecast"),
    path("account.html",
         views.user_account, name="user_account"),
    path("club-rules.html",
         views.club_rules, name="club_rules"),
]
