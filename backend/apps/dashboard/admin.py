from django.contrib import admin

from apps.dashboard.models import Post, PostWord, Account, Group, PostStats

from django.apps import apps
app = apps.get_app_config('dashboard')
# for model_name, model in app.models.items():
#     if model_name in ['post', 'group', 'poststats']:
#         continue
#     admin.site.register(model)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('post_id', 'short_text', 'group', 'date', 'post_type')
    list_filter = ('group', 'post_type')
    search_fields = ('text', )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('group').with_short_text()

    def short_text(self, obj):
        return obj.short_text
    short_text.short_description = 'Short text'


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'screen_name', 'group_id', )

@admin.register(PostStats)
class StatsAdmin(admin.ModelAdmin):
    list_display = ('post', 'likes_count', 'views_count', 'created_at', 'id', )
    autocomplete_fields = ('post', )

@admin.register(PostWord)
class WordAdmin(admin.ModelAdmin):
    list_display = ('word', 'post', 'date', 'count', )
    autocomplete_fields = ('post', )