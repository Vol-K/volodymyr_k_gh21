from django import forms
from user_side.models import ListOfMatches


#
class ActivateDIsableRound(forms.Form):
    # xxx = ListOfMatches.objects.all().values_list(
    #     'round_numder', flat=True).distinct()
    rounds_list = forms.ModelChoiceField(
        empty_label=".......",
        queryset=None
    )

    # Modifying the 'teams_together' field of form.
    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        if request:

            # Preparring of supporting data.
            self.fields["rounds_list"].queryset = (
                ListOfMatches.objects.all().
                values_list('round_numder', flat=True).distinct()
                # values("round_numder").distinct()
            )
    # class Meta:
    #     model = models.FeatureModel
    #     fields = ['role', 'feature']
    # for ii in rounds_list:
    #     print(ii)
    # # Create a field.
    # if rounds_list_request:
    #     self.fields["rounds_list"].queryset = rounds_list_request
    # else:
    #     self.fields["rounds_list"].queryset = (
    #         ListOfMatches.objects.none())


#
class LookingMatchesScoreForm(forms.Form):
    start_process = forms.CharField(
        label="looking_matches_score", initial="yes", required=False)

#
class CalculateUserPointsForm(forms.Form):
    start_process = forms.CharField(
        label="calculate_points", initial="yes", required=False)


#
class CleanFintableForm(forms.Form):
    start_process = forms.CharField(
        label="clean_fintable", initial="yes", required=False)
