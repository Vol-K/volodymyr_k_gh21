from django.urls import path
from . import views

#
urlpatterns = [
    path("index.html", views.index, name="user_index2"),
    path("", views.index, name="user_index"),
]
