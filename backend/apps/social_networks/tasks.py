import asyncio

from celery import shared_task
from apps.dashboard.models import Post, PostWord, Group, PostStats
from services.api import VkAPI
from services.worker import parse_vk


@shared_task()
def collect_vk_posts():
    api = VkAPI()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    # api = TelegramAPI()
    loop.run_until_complete(parse_vk(api))