from django.urls import path
from . import views


urlpatterns = [
    path("phone.html", views.phone, name="phone_page"),
    path("computers.html", views.computers, name="pc_page"),
    path("television.html", views.television, name="tv_page"),
    path("editproduct.html", views.edit_product, name="edit"),
    path("edited", views.edited, name="edited"),
    path("add_to_cart", views.ajax_add_to_cart, name="ajax_add_to_cart"),
    path("cart.html", views.user_cart, name="user_cart"),
]
