"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from . import views


class YourCustomAdminSite(admin.AdminSite):
    ...

    def get_urls(
        self,
    ):
        return [
            path(
                "custom_page/",
                self.admin_view(self.custom_page),
                name="custom_page",
            ),
        ] + super().get_urls()


#
urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("user_side.urls")),
    path("user/", include("user_side.urls")),
    path("login/", views.user_login, name="user_login"),
    path("register/", views.user_register, name="register_new_user"),
    path("logout/", views.log_out, name="user_logout"),
]
