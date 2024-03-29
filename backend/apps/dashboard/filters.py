from django_filters import rest_framework as filters
from apps.dashboard.models import Post, PostWord


class StatsFilter(filters.FilterSet):
    date = filters.DateRangeFilter()

    class Meta:
        model = PostWord
        fields = ('date', 'post', 'count', )


class PostFilter(filters.FilterSet):
    date = filters.DateRangeFilter()

    class Meta:
        model = Post
        fields = ('date', 'group', 'likes_count', 'views_count', 'comment_count', 'marked_as_ads', )
