from rest_framework.routers import DefaultRouter
from apps.social_networks import views
from django.urls import path, include
router = DefaultRouter()

router.register('accounts', views.SocialAccountsViewSet, basename='accounts')
urlpatterns = [
    path('social/', include(router.urls)),
]