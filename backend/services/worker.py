from services.api import VkAPI, TelegramAPI
from app.db.session import Session
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError, NoResultFound
from app.db.base import Post, Group
session = Session()
from telethon.tl.patched import Message
from telethon.tl.functions.channels import GetFullChannelRequest

# class PostRetriever:
#     def get_posts(self, owner_id, req_limit=4800):

def get_posts(api: TelegramAPI, channel_name: str = ''):
    try:
        channel = api.get_channel(channel_name)
    except ValueError:
        print('No channel found')
        return
    group = session.query(Group).filter_by(
        group_id=channel.id, name=channel.username,
        social_media_type='telegram'
    ).scalar()
    if not group:
        channel_info = api.client(GetFullChannelRequest(channel=channel))
        group = Group(
            group_id=channel.id, name=channel.username,
            screen_name=channel.title, social_media_type='telegram',
            description=channel_info.full_chat.about
        )
        session.add(group)
        session.commit()
    else:
        return
    # messages = api.get_chat(channel_name)
    objs = []
    for message in api.client.iter_messages(channel):
        message: Message
        objs.append(Post(
            post_id=message.id, owner_id=group.id, date=message.date, marked_as_ads=False, repost_count=message.forwards,
            views_count=message.views, text=message.text
        ))
    session.add_all(objs)
    session.commit()
    return objs

if __name__ == '__main__':
    api = TelegramAPI()
    dialogs = api.client.get_dialogs()

    for item in api.client.iter_dialogs():
        get_posts(api, item.name)
