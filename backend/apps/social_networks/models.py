from django.db import models
from fernet_fields.fields import EncryptedCharField


class Token(models.Model):
    class SocialTypes(models.TextChoices):
        VK = 'VK', 'Vk'
        TG = 'TG', 'Telegram'
        IG = 'IG', 'Instagram'
        FB = 'FB', 'Facebook'
    token = EncryptedCharField(max_length=255, verbose_name='social media access token')
    expires_at = models.DateTimeField(
        null=True, default=None, verbose_name='expires at'
    )
    type = models.CharField(choices=SocialTypes.choices, default=SocialTypes.VK, max_length=32)

    class Meta:
        verbose_name = 'Access token'
        verbose_name_plural = 'Access tokens'

    def __str__(self):
        return {self.token}
