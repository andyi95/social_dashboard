from django.urls import include, path
from rest_framework import routers
from apps.content.views import ArticleViewSet


router = routers.DefaultRouter()
router.register('', ArticleViewSet, basename='posts')
urlpatterns = [
    path('content/', include(router.urls)),
]

