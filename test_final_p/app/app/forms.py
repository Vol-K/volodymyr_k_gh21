from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from user_side.models import ListOfUsersMatchForecast, ListOfMatches


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
    forecast_option = [('ordinary', 'Ординар'), ('express', 'Експрес')]

    teams_together = forms.ModelChoiceField(
        empty_label="(Nothing)",
        queryset=None
        # queryset=ListOfMatches.objects.exclude(
        #     forecast_availability="no").values_list('teams_together', flat=True),
        # to_field_name="home_team"
    )
    team_home_user_forecast = forms.IntegerField(min_value=0)
    team_visitor_user_forecast = forms.IntegerField(min_value=0)
    forecast_type = forms.CharField(
        label='forecast_type', widget=forms.RadioSelect(choices=forecast_option))

    class Meta:
        model = ListOfUsersMatchForecast
        fields = ["teams_together", "team_home_user_forecast",
                  "team_visitor_user_forecast", "forecast_type"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['teams_together'].queryset = ListOfMatches.objects.exclude(
            forecast_availability="no")
