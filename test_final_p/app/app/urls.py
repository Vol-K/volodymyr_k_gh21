# Import all necessary moduls:
# 1) from Django package.
from django.contrib import admin
from django.urls import include, path

# 2) Local import.
from . import views


# List of supported urls of application.
urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("user_side.urls")),
    path("user/", include("user_side.urls")),
    path("login/", views.user_login, name="user_login"),
    path("register/", views.user_register, name="register_new_user"),
    path("logout/", views.log_out, name="user_logout"),
]
admin.autodiscover()
