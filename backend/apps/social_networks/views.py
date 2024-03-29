from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import APIException, ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from apps.social_networks.models import Account
from apps.social_networks.serializers import AccountSerializer
from services.api import VkAPI

from datetime import timedelta
from django.utils import timezone


class SocialAccountsViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    @action(['get'], detail=True, url_path='vk/check')
    def check_vk(self, request, pk=None):
        account: Account = self.get_object()
        if not account.tokens.exists():
            raise ValidationError('No tokens for this account')
        token = account.tokens.first()
        api = VkAPI(access_token=token.token)
        try:
            info = api.get_scopes()
        except Exception as e:
            raise APIException(e)
        return Response(info)

    @action(['get'], detail=False, url_path='vk/auth_url')
    def vk_auth_url(self, request, pk=None):
        """
        Получить ссылку для авторизации вк.
        """
        api = VkAPI(access_token='')
        uri = self.request.query_params.get('redirect_uri')
        return Response({'url': api.get_oauth_url(uri)})

    @action(['post'], detail=True, url_path='vk/token')
    def vk_auth_token(self, request, pk=None):
        code = request.data.get('code')
        uri = request.data.get('redirect_uri')
        api = VkAPI(access_token='')
        response = api.exchange_auth_code(code, uri)
        if 'error' in response.keys():
            raise APIException(response)
        token = response.get('access_token')
        expires_at = timezone.now() + timedelta(seconds=response.get('expires_in'))
        account = self.get_object()
        account.tokens.create(token=token, expires_at=expires_at)
        return Response({'token': token})
