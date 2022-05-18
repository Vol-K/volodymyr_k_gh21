from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from user_side.models import ListOfUsersMatchForecast


# 'Log in' form for the website users.
class LogInForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


# 'Registration of the new user' form.
class RegisterForm(UserCreationForm):
    # username = forms.CharField()
    # password_1 = forms.CharField(widget=forms.PasswordInput)
    # password_2 = forms.CharField(widget=forms.PasswordInput)
    # user_email = forms.CharField(widget=forms.EmailInput)
    user_email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "password1", "password2", "user_email"]


#
class MakeForecastForm(forms.Form):
    teams_together = forms.CharField()
    team_home_user_forecast = forms.IntegerField()
    team_visitor_user_forecast = forms.IntegerField()
    forecast_type = forms.CharField()

    class Meta:
        model = ListOfUsersMatchForecast
        fields = ["teams_together", "team_home_user_forecast",
                  "team_visitor_user_forecast", "forecast_type"]
