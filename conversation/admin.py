from django.contrib import admin
from . import models


@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):

    """ Message Admin Deifinition """

    list_display = ("__str__", "created")
    raw_id_fields = ("user",)


@admin.register(models.Conversation)
class ConversationAdmin(admin.ModelAdmin):

    """ Conversation Admin Difinition """

    fieldsets = (("Participants", {"fields": ("participants",),}),)

    filter_horizontal = ("participants",)

    list_display = ("__str__", "count_messages", "count_participants")
