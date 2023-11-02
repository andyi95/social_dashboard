
from rest_framework.viewsets import ReadOnlyModelViewSet
from apps.content.models import Article
from apps.content.serializers import ArticleSerializer


class ArticleViewSet(ReadOnlyModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
