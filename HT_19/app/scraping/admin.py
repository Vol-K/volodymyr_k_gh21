from django.contrib import admin
from .models import Askstories, Showstories, Newstories, Jobstories


# Customizing of models output: what and how will be shown on 'Admin' side.
class AskstoriesAdmin(admin.ModelAdmin):
    list_display = (
        "id", "id_item", "by", "title", "descendants", "score", "time")
    list_display_links = ("title", "id_item",)


class ShowstoriesAdmin(admin.ModelAdmin):
    list_display = (
        "id", "id_item", "by", "title", "descendants", "score", "time")
    list_display_links = ("title", "id_item",)


class NewstoriesAdmin(admin.ModelAdmin):
    list_display = (
        "id", "id_item", "by", "title", "descendants", "score", "time")
    list_display_links = ("title", "id_item",)


class JobstoriesAdmin(admin.ModelAdmin):
    list_display = ("id", "id_item", "by", "title", "score", "time")
    list_display_links = ("title", "id_item",)


admin.site.register(Askstories, AskstoriesAdmin)
admin.site.register(Showstories, ShowstoriesAdmin)
admin.site.register(Newstories, NewstoriesAdmin)
admin.site.register(Jobstories, JobstoriesAdmin)
