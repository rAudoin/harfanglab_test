from django.contrib import admin

# Register your models here.

from .models import Game, Platform


@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ["name", "studio", "release_date", "ratings"]
    search_fields = ["name"]
