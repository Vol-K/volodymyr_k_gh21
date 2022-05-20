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
    user_email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "password1", "password2", "user_email"]


#
class MakeForecastForm(forms.Form):
    forecast_option = [('ordinary', 'Ординар'), ('express', 'Експрес')]

    teams_together = forms.ModelChoiceField(
        empty_label="Список",
        queryset=None
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
        request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        # if request:
        matches = ListOfMatches.objects.filter(
            forecast_availability="yes")
        forecasts = ListOfUsersMatchForecast.objects.filter(
            user_id=request.user.id)

        #
        for element in forecasts:
            print("XXXX", element.teams_together)
            matches = matches.exclude(match_id=element.match_id)

        print("mat", matches)
        #
        if len(matches) == 0:
            self.fields["teams_together"].queryset = ListOfMatches.objects.none()
        else:
            self.fields["teams_together"].queryset = matches
        # else:
        #     self.fields["teams_together"].queryset = ListOfMatches.objects.none()

        print("teans", self.fields["teams_together"].queryset)
