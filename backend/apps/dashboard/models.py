from django.db import models


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
        managed = False
        db_table = 'account'


class Group(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    screen_name = models.CharField(max_length=255, blank=True, null=True)
    is_closed = models.BooleanField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    contact_id = models.IntegerField(blank=True, null=True)
    group_id = models.IntegerField(blank=True, null=True)
    social_media_type = models.CharField(max_length=255, blank=True, null=True, verbose_name='тип соц. сети')

    class Meta:
        managed = False
        db_table = 'group'


class Post(models.Model):
    post_id = models.IntegerField(blank=True, null=True)
    group = models.ForeignKey(Group, models.DO_NOTHING, blank=True, null=True, related_name='posts')
    date = models.DateTimeField(blank=True, null=True, verbose_name='Publication timestamp in MSC tz')
    marked_as_ads = models.BooleanField(blank=True, null=True)
    post_type = models.CharField(max_length=32, blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    likes_count = models.IntegerField(blank=True, null=True)
    repost_count = models.IntegerField(blank=True, null=True)
    views_count = models.IntegerField(blank=True, null=True)
    comment_count = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'post'

    def __str__(self):
        return f'Пост от {self.date.date()} текст {self.text[:20]}'



class PostStats(models.Model):
    likes_count = models.IntegerField()
    repost_count = models.IntegerField()
    views_count = models.IntegerField()
    comment_count = models.IntegerField()
    post = models.ForeignKey(Post, models.DO_NOTHING, related_name='stats')

    class Meta:
        managed = False
        db_table = 'poststats'

# class PostWordQuerySet(models.QuerySet):
#     def stats(self):
#
class PostWord(models.Model):
    word = models.CharField(max_length=255, blank=True, null=True)
    post = models.ForeignKey(Post, models.DO_NOTHING, blank=True, null=True, related_name='words')
    date = models.DateField(blank=True, null=True, verbose_name='Publication date of original post in MSC tz')
    count = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'postword'

    def __str__(self):
        return f'Слово {self.word} кол. {self.count} дата {self.date}'

class Comment(models.Model):
    from_field = models.ForeignKey(Account, models.DO_NOTHING, db_column='from_id', blank=True, null=True,
                                   verbose_name='ID of comment author')  # Field renamed because it was a Python
    # reserved
    # word.
    post = models.ForeignKey('Post', models.DO_NOTHING, blank=True, null=True)
    owner = models.ForeignKey('Group', models.DO_NOTHING, blank=True, null=True, verbose_name='ID of group feed with '
                                                                                             'the '
                                                                                     'comment')
    date = models.DateTimeField(blank=True, null=True, verbose_name='Publication timestamp in MSC tz')
    text = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'comment'