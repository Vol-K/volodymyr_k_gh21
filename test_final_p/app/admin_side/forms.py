# Import all necessary moduls:
# 1) from Django package.
from django import forms

# 2) from Other packages.
from user_side.models import ListOfMatches


# Form for activate / deativate specify round.
class ActivateDisableRound(forms.Form):
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
                values_list('round_number', flat=True).distinct()
                # values("round_number").distinct()
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


# Form to manual launch process of looking the scores of matches
# inside active round.
class LookingMatchesScoreForm(forms.Form):
    start_process = forms.CharField(
        label="looking_matches_score", initial="yes", required=False)


# Form to manual launch proccess of calculation points for
# the users frecasts by each match inside active round.
class CalculateUserPointsForm(forms.Form):
    start_process = forms.CharField(
        label="calculate_points", initial="yes", required=False)


# Form for reset data on Fintable.
class CleanFintableForm(forms.Form):
    start_process = forms.CharField(
        label="clean_fintable", initial="yes", required=False)
