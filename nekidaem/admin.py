from django.contrib import admin

from . import models


class BlogAdmin(admin.ModelAdmin):
    list_display = ('author', 'theme')


class NoteAdmin(admin.ModelAdmin):
    list_display = ('author', 'title', 'body', 'time', 'notification_message')


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('blog', 'subscriber')


class NoteStatusAdmin(admin.ModelAdmin):
    list_display = ('note', 'subscriber', 'status')


admin.site.register(models.Blog, BlogAdmin)
admin.site.register(models.Note, NoteAdmin)
admin.site.register(models.Subscription, SubscriptionAdmin)
admin.site.register(models.NoteStatus, NoteStatusAdmin)

