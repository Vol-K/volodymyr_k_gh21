# Import all necessary moduls:
# 1) from Django package.
from random import choices
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.safestring import mark_safe

# 2) Local import.
from user_side.models import (
    ListOfUsersMatchForecast, ListOfMatches, CustomUser)


# 'Log in' form for the website users.
class LogInForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(LogInForm, self).__init__(*args, **kwargs)
        self.fields['password'].widget.attrs['autocomplete'] = 'off'
        self.fields['password'].widget = forms.HiddenInput()


# 'Registration of the new user' form.
class RegisterForm(UserCreationForm):
    user_email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = ["username", "password1", "password2", "user_email"]


# 'Form' for create an one forecast by user.
class MakeForecastForm(forms.Form):
    forecast_option = [('ordinary', 'Ординар'), ('express', 'Експрес')]

    teams_together = forms.ModelChoiceField(
        empty_label=".......",
        queryset=None,
    )
    team_home_user_forecast = forms.IntegerField(min_value=0, max_value=11)
    team_visitor_user_forecast = forms.IntegerField(min_value=0, max_value=11)
    forecast_type = forms.CharField(
        label='forecast_type',
        widget=forms.RadioSelect(
            choices=forecast_option,
            attrs={'class': 'form-check-inline'},
        ),
        initial="ordinary")

    class Meta:
        model = ListOfUsersMatchForecast
        fields = ["teams_together", "team_home_user_forecast",
                  "team_visitor_user_forecast", "forecast_type"]

    # Modifying the 'teams_together' field of form.
    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        if request:

            # Preparring of supporting data.
            matches = ListOfMatches.objects.filter(
                forecast_availability="yes")
            forecasts = ListOfUsersMatchForecast.objects.filter(
                user_id=request.user.id)
            for element in forecasts:
                matches = matches.exclude(match_id=element.match_id_id)

            # Create a field.
            if matches:
                self.fields["teams_together"].queryset = matches
            else:
                self.fields["teams_together"].queryset = (
                    ListOfMatches.objects.none())


# 'Form' for change or delete one forecast by user.
class ChangeForecastForm(forms.Form):

    teams_together = forms.ModelChoiceField(
        empty_label=".......",
        queryset=None
    )
    team_home_user_forecast = forms.IntegerField(
        min_value=0, max_value=11, required=False)
    team_visitor_user_forecast = forms.IntegerField(
        min_value=0, max_value=11, required=False)
    change_forecast = forms.CharField(
        label="change_forecast", initial="yes", required=False)
    delete_forecast = forms.CharField(
        label="delete_forecast", initial="yes", required=False)

    # Modifying the 'teams_together' field of form.
    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        if request:
            # Create a list of matches available for changes/delete.
            available_round_number = ListOfMatches.objects.filter(
                forecast_availability="yes").values("round_number").distinct()
            self.fields["teams_together"].queryset = (
                ListOfUsersMatchForecast.objects.filter(
                    user_id=request.user.id,
                    round_number=available_round_number[0]["round_number"]))


# 'Form' for delete all forecasts by user in current round.
class DeleteAllForecastsForm(forms.Form):
    delete_all = forms.CharField(
        label="delete_all", initial="yes", required=False)


# Forn for changing "send_reminder" attribute by User.
class ChangeSendEmailReminderForm(forms.Form):
    reminder_choices = [
        ('', '----'),
        (0, "Ні"),
        (1, "Так")
    ]
    change_reminder = forms.ChoiceField(choices=reminder_choices)

    # Modifying the 'change_reminder' field of form.
    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        # Getting only one "real available" option to change (from DataBase),
        # and modify field choice options.
        if request:
            current_user_reminder_status = CustomUser.objects.filter(
                id=request.user.id)
            if current_user_reminder_status[0].send_reminder:
                reminder_choices2 = [('', '----'), (0, "Ні")]
            else:
                reminder_choices2 = [('', '----'), (1, "Так")]

            self.fields["change_reminder"] = forms.ChoiceField(
                choices=reminder_choices2, required=True)
