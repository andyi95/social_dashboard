import datetime
import os

from telethon.errors import UsernameInvalidError

os.environ['PYTHONASYNCIODEBUG'] = '1'

from services.api import TelegramAPI, VkAPI
from app.models import Post, Group
from telethon.tl.patched import Message
from telethon.tl.types import User
from telethon.tl.functions.channels import GetFullChannelRequest
import logging
import sys
from app.core.config import DB_URL
from tortoise import Tortoise
import asyncio
from api.models import Post as PostModel, Group as GroupModel

logging.basicConfig(
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

async def get_posts(api: TelegramAPI, channel, group):
    objs = []
    i = 0
    last_post = await Post.filter(group_id=group.id, group__social_media_type='telegram').order_by('-post_id').limit(1)
    max_id = last_post[0].post_id if last_post else 0
    async for message in api.client.iter_messages(channel, min_id=max_id):
        i += 1
        message: Message
        qs = await Post.filter(post_id=message.id, group__social_media_type='telegram', date=message.date)
        if qs or not message.text:
            continue
        dt = message.date.replace(tzinfo=datetime.timezone.utc)
        objs.append(Post(
            post_id=message.id, group_id=group.id, date=dt, marked_as_ads=False,
            repost_count=message.forwards,
            views_count=message.views, text=message.text, post_type='telegram'
        ))
        if i % 1000 == 0:
            print('creating 1000 posts')
            await Post.bulk_create(objs)
    await Post.bulk_create(objs)
    return objs


async def get_group(api: TelegramAPI, channel_name: str = ''):
    try:
        channel = await api.get_channel(channel_name)
    except (ValueError, UsernameInvalidError):
        logging.debug('No channel found')
        return
    if isinstance(channel, User):
        return
    group = await Group.filter(group_id=channel.id, name=channel.username, social_media_type='telegram').first()
    if not group:
        channel_info = await api.client(GetFullChannelRequest(channel=channel))
        group = Group(
            group_id=channel.id, name=channel.username,
            screen_name=channel.title, social_media_type='telegram',
            description=channel_info.full_chat.about
        )
        await group.save()

    await get_posts(api, channel, group)


async def process_groups(api = None, dialogs = None):
    await api.client.connect()
    await Tortoise.init(
        db_url=DB_URL,
        modules={'models': ['app.models']},
    )

    async for item in api.client.iter_dialogs():
        await get_group(api, item.name)


async def parse_vk(api: VkAPI, group_ids = None):
    group_ids = os.getenv('GROUP_IDS', group_ids)
    for group_id in group_ids.split(','):
        group = api.get_group(group_id)
        if not group:
            continue


if __name__ == '__main__':
    api = TelegramAPI()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(process_groups(api))


