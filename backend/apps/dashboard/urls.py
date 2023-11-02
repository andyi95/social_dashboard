from django.urls import include, path
from rest_framework import routers
from apps.dashboard.views import PostStatsViewSet, PostsViewSet

router = routers.DefaultRouter()
router.register('stats', PostStatsViewSet, basename='stats')
router.register('posts', PostsViewSet, basename='posts')

urlpatterns = [
    path('dashboard/', include(router.urls)),
]
