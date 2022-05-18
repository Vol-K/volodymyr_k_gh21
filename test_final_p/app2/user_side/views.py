from django.shortcuts import render, redirect


# Create your views here.
def index(request):
    context = {}
    return render(request, "user_side/index2.html", context)


#
def fintable(request):
    pass


#
def user_login(request):
    pass


#
def user_register(request):
    pass


#
def change_forecast(request):
    pass


#
def forecast_by_other(requst):
    pass


#
def teams_and_members(request):
    pass


#
def user_accaunt(request):
    pass
