from django.urls import include, path
from rest_framework import routers
from apps.dashboard import views

router = routers.DefaultRouter()
router.register('stats', views.PostStatsViewSet, basename='stats')
router.register('posts', views.PostsViewSet, basename='posts')
router.register('groups', views.GroupViewSet, basename='groups')


urlpatterns = [
    path('dashboard/', include(router.urls)),
]
