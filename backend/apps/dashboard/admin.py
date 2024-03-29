from django.contrib import admin

from apps.dashboard.models import Post, PostWord, Account, Group

from django.apps import apps
app = apps.get_app_config('dashboard')
for model_name, model in app.models.items():
    if model_name in ['post', 'group']:
        continue
    admin.site.register(model)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('post_id', 'short_text', 'group', 'date', 'post_type')
    list_filter = ('group', 'post_type')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('group').with_short_text()

    def short_text(self, obj):
        return obj.short_text
    short_text.short_description = 'Short text'


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'screen_name', 'group_id', )
