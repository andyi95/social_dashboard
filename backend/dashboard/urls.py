from django.urls import include, path
from rest_framework import routers
from dashboard.views import PostViewSet

dashboard_router = routers.DefaultRouter()
dashboard_router.register('', PostViewSet, basename='posts')
urlpatterns = [
    path('dashboard/', include(dashboard_router.urls)),
]
