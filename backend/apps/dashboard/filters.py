from django_filters import rest_framework as filters
from apps.dashboard.models import Post, PostWord


class PostFilter(filters.FilterSet):
    date = filters.DateRangeFilter()

    class Meta:
        model = PostWord
        fields = ('date', 'post', 'count', )