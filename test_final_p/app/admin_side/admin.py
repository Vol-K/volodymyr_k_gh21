from django.contrib import admin
from django.db import models

from django.shortcuts import render, redirect
from django.urls import path

from .views import my_custom_view


#
class DummyModel(models.Model):

    class Meta:
        verbose_name_plural = 'Dummy Model'
        app_label = 'admin_side'


#
class DummyModelAdmin(admin.ModelAdmin):
    model = DummyModel
    # is_superuser = models.BooleanField(default=False)

    # def has_perm(self, perm, obj=None):
    #     return self.is_admin

    # def has_module_perms(self, app_label):
    #     return self.is_admin

    def get_urls(self):
        view_name = '{}_{}_changelist'.format(
            self.model._meta.app_label, self.model._meta.model_name)
        return [
            path('', my_custom_view, name=view_name),
        ]

    def get_app_list(self, request):
        app_list = super().get_app_list(request)
        # reorder the app list as you like
        return app_list


#
admin.site.site_header = "Адмін панель Клуба"
admin.site.index_title = ""

#
admin.site.register(DummyModel, DummyModelAdmin)
