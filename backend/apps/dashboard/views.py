from django.db.models import Q, QuerySet, Max, Min, Count, Sum
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.decorators import action
from apps.dashboard.filters import PostFilter, StatsFilter
from apps.dashboard.models import Post, PostWord, Group
from apps.dashboard.serializers import DetailStatSerializer, WordStatSerializer, PostSerializer, GroupSerializer
from services.worker import collect_tg_posts


class PostsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Post.objects.select_related('group').all()
    serializer_class = PostSerializer
    filterset_class = PostFilter
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ['date', 'likes_count', 'views_count', 'comment_count']

    @action(methods=['get'], detail=True)
    def comments(self, request, pk=None, **kwargs):
        return Response()


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class PostStatsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PostWord.objects.all()
    filterset_class = StatsFilter

    lookup_url_kwarg = 'word'

    def get_serializer_class(self):
        if self.action == 'list':
            return WordStatSerializer
        return DetailStatSerializer

    def list(self, request, *args, **kwargs):
        qs: QuerySet[PostWord] = self.get_queryset()
        qs = qs.values('word').annotate(
            post_id=Max('post_id'), count=Sum('count'), date=Max('date')
        ).order_by('-count')
        limit = int(self.request.query_params['limit']) if 'limit' in self.request.query_params else 100
        qs = self.filter_queryset(qs)[:limit]
        serializer = WordStatSerializer(qs, many=True, read_only=True, context=self.get_serializer_context())
        return Response(serializer.data)

    def retrieve(self, request, word=None, *args, **kwargs):
        qs = PostWord.objects.filter(word=word).values('date').annotate(
            post_count=Count('post')
        ).order_by('-date')
        if 'limit' in request.query_params:
            qs = qs[:int(request.query_params['limit'])]
        serializer = DetailStatSerializer(qs, many=True, read_only=True)
        return Response(serializer.data)

    @action(methods=['get', 'post'], detail=False)
    def start_task(self, request, *args, **kwargs):
        collect_tg_posts.delay()
        return Response()
