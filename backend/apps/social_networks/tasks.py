import asyncio

from celery import shared_task
from apps.dashboard.models import Post, PostWord, Group, PostStats
from apps.social_networks.models import Account
from services.api import VkAPI
from services.worker import parse_vk


@shared_task()
def collect_vk_posts():
    api = VkAPI()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    # api = TelegramAPI()
    loop.run_until_complete(parse_vk(api))

@shared_task()
def retrieve_vk_profile(account: Account):
    token = account.tokens.first().token
    api = VkAPI(access_token=token)
    me = api.get_me()
    account.screen_name = me['screen_name']
    account.username = me['screen_name']
    account.save()
