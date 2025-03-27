from django.db import models
from django.db.models.functions import ExtractMonth, Lower, Substr, Trunc
from django.utils import timezone


class Account(models.Model):
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    deactivated = models.BooleanField(blank=True, null=True)
    is_closed = models.BooleanField(blank=True, null=True)
    about = models.CharField(max_length=255, blank=True, null=True)
    activities = models.TextField(blank=True, null=True)
    bdate = models.DateTimeField(blank=True, null=True)
    last_seen = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'account'
        verbose_name = 'Social Media Account'
        ordering = ('first_name', 'last_name')


class Group(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    screen_name = models.CharField(max_length=255, blank=True, null=True)
    is_closed = models.BooleanField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    contact_id = models.IntegerField(blank=True, null=True)
    group_id = models.BigIntegerField(blank=True, null=True)
    social_media_type = models.CharField(max_length=255, blank=True, null=True, verbose_name='тип соц. сети')

    class Meta:
        managed = True
        db_table = 'group'
        verbose_name = 'Social Media Group'
        ordering = ('name', 'id')

    def __str__(self):
        return self.name


class PostQuerySet(models.QuerySet):
    def with_short_text(self):
        return self.annotate(short_text=Substr('text', 1, 100))


class Post(models.Model):
    id = models.BigAutoField(primary_key=True)
    post_id = models.BigIntegerField(blank=True, null=True)
    group = models.ForeignKey(Group, models.DO_NOTHING, blank=True, null=True, related_name='posts')
    date = models.DateTimeField(blank=True, null=True, verbose_name='Publication timestamp in MSC tz')
    marked_as_ads = models.BooleanField(blank=True, null=True)
    post_type = models.CharField(max_length=32, blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    likes_count = models.IntegerField(blank=True, null=True)
    repost_count = models.IntegerField(blank=True, null=True)
    views_count = models.IntegerField(blank=True, null=True)
    comment_count = models.IntegerField(blank=True, null=True)
    tags_old = models.ManyToManyField('Tag', related_name='posts_old', blank=True)
    tags = models.ManyToManyField('Tag', through='PostTag', related_name='posts', blank=True)
    objects = PostQuerySet.as_manager()

    class Meta:
        managed = True
        db_table = 'post'
        verbose_name = 'Social Media Post'
        ordering = ('date', 'id')
        constraints = [
            models.UniqueConstraint('id', 'date', name='unique_id_date')
        ]
        indexes = [
            models.Index(Trunc('date', 'day'), name='post_date_date_idx')
        ]

    def __str__(self):
        return self.text[:50] if self.text else 'No text'


class PostHistory(models.Model):
    id = models.BigAutoField(primary_key=True)
    post = models.ForeignKey(Post, models.SET_NULL, blank=True, null=True, related_name='history')
    date = models.DateTimeField(blank=True, null=True)
    text = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Post History'
        verbose_name_plural = 'Post Histories'

    def __str__(self):
        return self.text[:50] if self.text else 'No text'

class PostStats(models.Model):
    id = models.BigAutoField(primary_key=True)
    likes_count = models.IntegerField()
    repost_count = models.IntegerField()
    views_count = models.IntegerField()
    comment_count = models.IntegerField()
    post = models.ForeignKey(Post, models.DO_NOTHING, related_name='stats', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = True
        db_table = 'poststats'
        verbose_name = 'Social Media Post Stats'
        ordering = ('created_at', 'id')

    def __str__(self):
        return f'stats for post {self.post}'


class PostWord(models.Model):
    id = models.BigAutoField(primary_key=True)
    word = models.CharField(max_length=255, blank=True, null=True)
    post = models.ForeignKey(Post, models.DO_NOTHING, blank=True, null=True, related_name='words')
    date = models.DateField(blank=True, null=True, verbose_name='Publication date of original post in MSC tz')
    count = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'postword'
        verbose_name = 'Word in Social Media Post'

    def __str__(self):
        return self.word


class Comment(models.Model):
    id = models.BigAutoField(primary_key=True)
    from_field = models.ForeignKey(Account, models.DO_NOTHING, db_column='from_id', blank=True, null=True,
                                   verbose_name='ID of comment author')
    post = models.ForeignKey('Post', models.DO_NOTHING, blank=True, null=True)
    owner = models.ForeignKey('Group', models.DO_NOTHING, blank=True, null=True, verbose_name='ID of group feed with '
                                                                                             'the '
                                                                                     'comment')
    date = models.DateTimeField(blank=True, null=True, verbose_name='Publication timestamp in MSC tz')
    text = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'comment'


class PostTag(models.Model):
    id = models.BigAutoField(primary_key=True)
    post = models.ForeignKey(Post, models.DO_NOTHING, blank=True, null=True)
    tag = models.ForeignKey('Tag', models.DO_NOTHING, blank=True, null=True)
    tagged_at = models.DateTimeField(null=True, verbose_name='tagged at')

    class Meta:
        verbose_name = 'Post Tag'
        verbose_name_plural = 'Post Tags'


class Tag(models.Model):
    name = models.CharField(max_length=64, verbose_name='tag')
    description = models.TextField(verbose_name='tag description')

    class Meta:
        verbose_name = 'tag'
        verbose_name_plural = 'tags'
        constraints = [
            models.UniqueConstraint(Lower('name'), 'name', name='unique_lower_name')
        ]

    def __str__(self):
        return self.name
