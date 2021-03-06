# Import all necessary moduls:
# 1) from Django package.
from django.contrib import admin
from django.db import models
from django.urls import path

# 2) Local import.
from .views import my_custom_view


# Create a custom model to get page url on admin side.
class CustomModel(models.Model):

    class Meta:
        verbose_name_plural = 'Кастомні Admin операції'
        app_label = 'admin_side'


# Setup empty model "CustomModel", without any fields.
class CustomModelAdmin(admin.ModelAdmin):
    model = CustomModel

    # Get access for url.
    def get_urls(self):
        view_name = '{}_{}_changelist'.format(
            self.model._meta.app_label, self.model._meta.model_name)
        return [
            path('', my_custom_view, name=view_name),
        ]

    def get_app_list(self, request):
        app_list = super().get_app_list(request)
        return app_list


# Customising Admin site.
admin.site.site_header = "Адмін панель Клуба"
admin.site.index_title = ""

# Registing model.
admin.site.register(CustomModel, CustomModelAdmin)
