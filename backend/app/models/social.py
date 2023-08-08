from datetime import datetime

from tortoise import fields
from tortoise.models import Model


class Account(Model):
    first_name = fields.CharField(max_length=255, default='')
    last_name = fields.CharField(max_length=255, default='')
    deactivated = fields.BooleanField(default=False)
    about = fields.TextField(null=True, default=None)
    activities = fields.TextField(null=True)
    bdate = fields.DatetimeField(null=True)
    last_seen = fields.DatetimeField(null=True)


class Group(Model):
    group_id = fields.IntField(default=0)
    name = fields.CharField(max_length=255)
    screen_name = fields.CharField(max_length=512)
    is_closed=fields.BooleanField(default=False)
    description = fields.TextField()
    contact_id = fields.IntField()
    social_media_type = fields.CharField(max_length=255, description='тип соц. сети')
    posts: fields.ReverseRelation['Post']


class Post(Model):
    post_id = fields.IntField(index=True)
    date = fields.DatetimeField(name='Publication timestamp in MSC tz', index=True)
    marked_as_ads = fields.BooleanField(default=False)
    post_type = fields.CharField(max_length=255)
    text = fields.TextField()
    group: fields.ForeignKeyRelation[Group] = fields.ForeignKeyField(
        'models.Group', related_name='posts'
    )

    def __str__(self):
        return f'Post {self.post_id} from {datetime.date(self.date)}'


class Comment(Model):
    author: fields.ForeignKeyRelation[Account] = fields.ForeignKeyField(
        'models.Account', related_name='comments'
    )
    post: fields.ForeignKeyRelation[Post] = fields.ForeignKeyField(
        'models.Post', related_name='comments'
    )

class PostStats(Model):
    post: fields.ForeignKeyRelation[Post] = fields.ForeignKeyField(
        'models.Post', related_name='stats'
    )
    likes_count = fields.IntField()
    repost_count = fields.IntField()
    views_count = fields.IntField()
    comment_count = fields.IntField()


class PostWord(Model):
    word = fields.CharField(max_length=255)
    date = fields.DateField()
    count = fields.SmallIntField()
    post: fields.ForeignKeyRelation[Post] = fields.ForeignKeyField(
        'models.Post', related_name='words'
    )

    def __str__(self):
        return f'Word {self.word} count {self.count} from {self.post}'
