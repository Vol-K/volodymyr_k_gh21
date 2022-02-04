from django.urls import path
from . import views


urlpatterns = [
    path("phone.html", views.phone, name="phone_page"),
    path("computers.html", views.computers, name="pc_page"),
    path("television.html", views.television, name="tv_page"),
]
