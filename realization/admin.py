from django.contrib import admin
from .models import Thread, Message


@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ("id", "get_participants", "created", "updated")
    search_fields = ("participants__username",)

    def get_participants(self, obj):
        return ", ".join([user.username for user in obj.participants.all()])

    get_participants.short_description = "Participants"


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "sender", "text", "thread", "created", "is_read")
    search_fields = ("sender__username", "text")
    list_filter = ("is_read", "created")
