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
        empty_label=".......",
        queryset=None
    )
    team_home_user_forecast = forms.IntegerField(min_value=0)
    team_visitor_user_forecast = forms.IntegerField(min_value=0)
    forecast_type = forms.CharField(
        label='forecast_type',
        widget=forms.RadioSelect(choices=forecast_option),
        initial="ordinary")

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
            matches = matches.exclude(match_id=element.match_id)

        #
        if matches:
            self.fields["teams_together"].queryset = matches
        else:
            self.fields["teams_together"].queryset = (
                ListOfMatches.objects.none())


#
class ChangeForecastForm(forms.Form):
    operation_option = [('change', 'Change'), ('delete', 'Delete')]

    teams_together = forms.ModelChoiceField(
        empty_label=".......",
        queryset=None
    )
    team_home_user_forecast = forms.IntegerField(min_value=0)
    team_visitor_user_forecast = forms.IntegerField(min_value=0)
    match_operaion = forms.CharField(
        label='match_operaion',
        widget=forms.RadioSelect(choices=operation_option),
        initial="change"
    )

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        if request:
            self.fields["teams_together"].queryset = (
                ListOfUsersMatchForecast.objects.filter(
                    user_id=request.user.id))
