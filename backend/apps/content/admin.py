from django.contrib import admin

from apps.content.models import Article



@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'title')
