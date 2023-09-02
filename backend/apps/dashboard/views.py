from django.db.models import Q, QuerySet, Max, Min, Count, Sum
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from apps.dashboard.filters import PostFilter
from apps.dashboard.models import Post, PostWord
from apps.dashboard.serializers import DetailStatSerializer, WordStatSerializer
from services.worker import collect_tg_posts

class PostViewSet(viewsets.ModelViewSet):
    queryset = PostWord.objects.all()
    filterset_class = PostFilter
    lookup_url_kwarg = 'word'

    def list(self, request, *args, **kwargs):
        qs: QuerySet[PostWord] = self.get_queryset()
        qs = qs.values('word').annotate(
            post_id=Max('post_id'), count=Sum('count'), date=Max('date')
        ).order_by('-count')[:1000]
        qs = self.filter_queryset(qs)
        serializer = WordStatSerializer(qs, many=True, read_only=True, context=self.get_serializer_context())
        return Response(serializer.data)

    def retrieve(self, request, word=None, *args, **kwargs):
        qs = PostWord.objects.filter(word=word).values('date').annotate(
            post_count=Count('post')
        ).order_by('-date')
        serializer = DetailStatSerializer(qs, many=True, read_only=True)
        return Response(serializer.data)

    @action(methods=['get', 'post'], detail=False)
    def start_task(self, request, *args, **kwargs):
        collect_tg_posts.delay()
        return Response()
