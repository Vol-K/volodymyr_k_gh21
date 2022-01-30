from django.contrib import admin
from .models import Askstories, Showstories, Newstories, Jobstories

# Register your models here.
class AskstoriesAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "by", "id_item")
    list_display_links = ("title", "id_item",)
    list_filter = ("title", "id_item", )


class ShowstoriesAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "by", "id_item")
    list_display_links = ("title", "id_item", )
    ist_filter = ("title", "id_item", )


class NewstoriesAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "by", "id_item")
    list_display_links = ("title", "id_item", )
    ist_filter = ("title", "id_item", )


class JobstoriesAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "by", "id_item")
    list_display_links = ("title", "id_item",)
    ist_filter = ("title", "id_item", )


admin.site.register(Askstories, AskstoriesAdmin)
admin.site.register(Showstories, ShowstoriesAdmin)
admin.site.register(Newstories, NewstoriesAdmin)
admin.site.register(Jobstories, JobstoriesAdmin)