from django import forms


# Log in form for the website users. 
class LogInForm(forms.Form):

    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
