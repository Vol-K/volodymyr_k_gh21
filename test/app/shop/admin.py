from django.contrib import admin
from .models import TeleVision, Phones, PersonalComputers


# Customizing of models output: what and how will be shown on 'Admin' side.
class TeleVisionAdmin(admin.ModelAdmin):
    list_display = (
        "id", "brand", "model", "description", "price", "available")
    list_display_links = ("brand", "model",)


class PhonesAdmin(admin.ModelAdmin):
    list_display = (
        "id", "brand", "model", "description", "price", "available")
    list_display_links = ("brand", "model",)


class PersonalComputersAdmin(admin.ModelAdmin):
    list_display = (
        "id", "brand", "model", "description", "price", "available")
    list_display_links = ("brand", "model",)


admin.site.register(TeleVision, TeleVisionAdmin)
admin.site.register(Phones, PhonesAdmin)
admin.site.register(PersonalComputers, PersonalComputersAdmin)
