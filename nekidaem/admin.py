from django.contrib import admin

from . import models


class BlogAdmin(admin.ModelAdmin):
    list_display = ('author', 'theme')


class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'title', 'body', 'time', 'notification_message')


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('blog', 'subscriber')


class PostStatusAdmin(admin.ModelAdmin):
    list_display = ('post', 'subscriber', 'status')


admin.site.register(models.Blog, BlogAdmin)
admin.site.register(models.Post, PostAdmin)
admin.site.register(models.Subscription, SubscriptionAdmin)
admin.site.register(models.PostStatus, PostStatusAdmin)

