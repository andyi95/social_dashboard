from django.contrib import admin

from apps.dashboard.models import Post, PostWord, Account, Group

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('post_id', 'group', 'date', 'post_type')

