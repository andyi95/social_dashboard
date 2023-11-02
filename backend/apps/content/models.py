from django.db import models
from django.utils.translation import gettext_lazy as _
from tinymce.models import HTMLField
from apps.core.models import TimeStamptedModel


class Article(models.Model):
    title = models.CharField(_('title'), max_length=255)
    content = HTMLField(_('content'))
    date = models.DateField(_('entry date'))

    class Meta:
        verbose_name = _('article entry')
        verbose_name_plural = _('articles entries')
