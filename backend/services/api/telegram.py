from telethon.sync import TelegramClient
# from telethon import sync
import os
from dotenv import load_dotenv
load_dotenv()


class TelegramAPI:
    """
    TODO: improve auth process and session store
    """
    def __init__(self):
        app_id = os.getenv('TELEGRAM_APP_ID')
        app_secret = os.getenv('TELEGRAM_APP_SECRET')
        # with TelegramClient('client', int(app_id), app_secret) as client:
        #     client.loop.run_until_complete(client.send_message('me', 'Hello, myself!'))
        #     self.client = client
        #     a = 1
        self.client = TelegramClient('client', int(app_id), app_secret)

    def get_chat(self, name: str = ''):
        entity = self.client.get_entity(name)
        messages = self.client.get_messages(entity.id)
        return messages

    def get_channel(self, name=''):
        entity = self.client.get_entity(name)
        return entity

    def get_chats(self):
        chats = self.client.get_dialogs()
        return chats

    def __del__(self):
        print('going disconnect')
        self.client.disconnect()
