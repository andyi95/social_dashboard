from django.db import models

from apps.core.models import TimeStamptedModel


class SocialTypes(models.TextChoices):
    VK = 'VK', 'Vk'
    TG = 'TG', 'Telegram'
    IG = 'IG', 'Instagram'
    FB = 'FB', 'Facebook'


class TokenType(models.TextChoices):
    ACCESS = 'ACC'
    REFRESH = 'REF'


class Account(models.Model):
    """Basic class of social network account of user."""
    type = models.CharField(choices=SocialTypes.choices, default=SocialTypes.VK, max_length=32)
    username = models.CharField(
        max_length=255, default='', blank=True
    )
    link = models.CharField(
        max_length=512, default='', blank=True
    )
    user = models.ForeignKey(
        'user.User', on_delete=models.CASCADE, related_name='accounts'
    )

    class Meta:
        verbose_name = 'social network'
        verbose_name_plural = 'social networks'


class Token(models.Model):
    token = models.CharField(max_length=255, verbose_name='social media access token')
    expires_at = models.DateTimeField(
        null=True, default=None, verbose_name='expires at'
    )
    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name='tokens'
    )
    type = models.CharField(max_length=16, choices=TokenType.choices, default=TokenType.ACCESS)

    class Meta:
        verbose_name = 'Access token'
        verbose_name_plural = 'Access tokens'

    def __str__(self):
        return {self.token}


class TrackingGroup(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    group_id = models.CharField(max_length=255 )
    name = models.CharField(max_length=255)
    last_updated = models.DateTimeField(null=True, default=None)

