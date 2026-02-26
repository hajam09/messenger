from django.contrib import admin

from core.models import Room


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("id", "user_1", "user_2", "last_message")
    search_fields = ("user_1__username", "user_2__username")

