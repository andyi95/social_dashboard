import asyncio

import os
import sys
import time

from telethon.errors import UsernameInvalidError

from django.conf import settings
from django.utils import timezone

from services.api import TelegramAPI, VkAPI
from telethon.tl.patched import Message
from telethon.tl.types import User
from telethon.tl.functions.channels import GetFullChannelRequest

import datetime
from celery import shared_task
PROJECT_NAME = 'backend'


async def get_posts(api: TelegramAPI, channel, group):
    objs = []
    i = 0
    last_post = Post.objects.filter(group_id=group.id, group__social_media_type='telegram').order_by(
        '-post_id').limit(1)
    max_id = last_post[0].post_id if last_post else 0
    async for message in api.client.iter_messages(channel, min_id=max_id):
        i += 1
        message: Message
        qs = Post.objects.filter(post_id=message.id, group__social_media_type='telegram', date=message.date)
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
            Post.objects.bulk_create(objs)
    Post.objects.bulk_create(objs)
    return objs


async def get_group(api: TelegramAPI, channel_name: str = ''):
    try:
        channel = await api.get_channel(channel_name)
    except (ValueError, UsernameInvalidError):
        # logging.debug('No channel found')
        return
    if isinstance(channel, User):
        return
    group = Group.objects.filter(group_id=channel.id, name=channel.username, social_media_type='telegram').first()
    if not group:
        channel_info = await api.client(GetFullChannelRequest(channel=channel))
        group = Group(
            group_id=channel.id, name=channel.username,
            screen_name=channel.title, social_media_type='telegram',
            description=channel_info.full_chat.about
        )
        group.save()

    await get_posts(api, channel, group)


async def process_groups(api = None, dialogs = None):
    if not api.client.is_connected():
        api.client.start()
    async for item in api.client.iter_dialogs():
        await get_group(api, item.name)


def parse_vk(api: VkAPI, group_ids = None):
    group_ids = os.getenv('GROUP_IDS', group_ids)
    for group_id in group_ids.split(','):
        v_group = api.get_group(group_id)
        if not v_group:
            continue
        g_dict = {
            'name': v_group.name,
            'screen_name': v_group.screen_name,
            'social_media_type': 'vk',
            'is_closed': v_group.is_closed,
            'description': v_group.description
        }
        group, _ = Group.objects.get_or_create(group_id=v_group.id, **g_dict)
        Group.objects.filter(group_id=v_group.id).update(**g_dict)
        for i in range(0, 100):
            v_posts = v_group.get_posts(i * 100)
            if not v_posts:
                break
            for v_post in v_posts:
                post, _ = Post.objects.get_or_create(
                    post_id=v_post.id, group=group
                )
                post.date = timezone.make_aware(v_post.date, timezone=timezone.get_current_timezone())
                post.marked_as_ads = v_post.marked_as_ads
                post.text = v_post.text
                post.likes_count = v_post.likes_count
                post.views_count = v_post.views_count
                post.comment_count = v_post.comments_count
                post.save()
            print(f'Got {i} batch. Last post {post}')
            time.sleep(0.1)


@shared_task
def collect_tg_posts():
    api = TelegramAPI()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(process_groups(api))
    # loop.run_until_complete(process_groups(api))

def collect_vk_posts():
    api = VkAPI()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    # api = TelegramAPI()
    loop.run_until_complete(parse_vk(api))


if __name__ == '__main__':
    sys.path.extend(['C:\\dev\\social_dashboard', 'C:\\dev\\social_dashboard\\backend',
                     'C:\\Program Files\\JetBrains\\PyCharm 2022.3.2\\plugins\\python\\helpers\\pycharm',
                     'C:\\Program Files\\JetBrains\\PyCharm 2022.3.2\\plugins\\python\\helpers\\pydev'])

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
    import django
    if 'setup' in dir(django):
        django.setup()
    from apps.dashboard.models import Post, PostWord, Group, PostStats
    # collect_tg_posts()
    collect_vk_posts()
