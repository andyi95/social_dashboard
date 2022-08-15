from sqlalchemy import Boolean, Column, DateTime, ForeignKey
from sqlalchemy.types import Date, String, Text, SmallInteger, Integer
from sqlalchemy.orm import relationship
from app.db.base import Base
from sqlalchemy import Index


class Account(Base):
    id = Column(Integer, primary_key=True)
    first_name = Column(String(255))
    last_name = Column(String(255))
    deactivated = Column(Boolean, default=False)
    is_closed = Column(Boolean, default=True)
    about = Column(String, nullable=True)
    activities = Column(Text, nullable=True)
    bdate = Column(DateTime, nullable=True)
    last_seen = Column(DateTime, nullable=True)

    def __repr__(self):
        return f'Account id {self.id}, {self.first_name} {self.last_name}'


class Group(Base):
    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, default=0)
    name = Column(String(512))
    screen_name = Column(String(255))
    is_closed = Column(Boolean, default=False)
    description = Column(Text)
    contact_id = Column(Integer, )
    social_media_type = Column(String(255), default='vk')

    def __repr__(self):
        return f'Group {self.screen_name} id {self.id}'


class Post(Base):
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, index=True)
    owner_id = Column(Integer, ForeignKey('group.id'), index=True)
    date = Column(DateTime, comment='Publication timestamp in MSC tz', index=True)
    marked_as_ads = Column(Boolean, default=False)
    post_type = Column(String)
    text = Column(Text)
    likes_count = Column(Integer)
    repost_count = Column(Integer)
    views_count = Column(Integer)
    comment_count = Column(Integer)

    group = relationship('Group')

    def __repr__(self):
        return f'Post id {self.post_id}: {self.text[:31]}'


class Comment(Base):
    id = Column(Integer, primary_key=True)
    from_id = Column(
        Integer, ForeignKey('account.id'), comment='ID of comment author', nullable=True
    )
    post_id = Column(Integer, ForeignKey('post.id'))
    owner_id = Column(
        Integer, ForeignKey('group.id'), index=True,
        comment='ID of group feed with the comment'
    )
    date = Column(DateTime, comment='Publication timestamp in MSC tz')
    text = Column(Text)

    post = relationship(Post, primaryjoin=post_id == Post.post_id, foreign_keys=Post.post_id)
    author = relationship(Account, primaryjoin=from_id == Account.id, post_update=True)
    group = relationship('Group')

    def __repr__(self):
        return f'Comment id {self.id}: {self.text[:31]}'


class PostWord(Base):
    id = Column(Integer, autoincrement=True, index=True, primary_key=True)
    word = Column(String(length=255), index=True)
    post_id = Column(Integer, ForeignKey('post.id'), index=True)
    date = Column(Date, comment='Publication date of original post in MSC tz', index=True)
    count = Column(Integer, default=1)
    post = relationship(Post, primaryjoin=post_id == Post.id, foreign_keys=Post.id)

    def __repr__(self):
        return f'Word {self.word} in post {self.post}'
