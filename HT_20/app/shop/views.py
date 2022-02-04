from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages


# from volodymyr_k_gh21/HT_20/app/shop/forms import LogInForm

def phone(request):
    return render(request, "shop/phone.html")


def computers(request):
    return render(request, "shop/computers.html")


def television(request):
    return render(request, "shop/television.html")
