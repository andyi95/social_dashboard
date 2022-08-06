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
        self.client = TelegramClient('client', int(app_id), app_secret)
        self.client.start()

    def get_chat(self, name: str = ''):
        entity = self.client.get_entity(name)
        messages = self.client.get_messages(entity.id)

    def get_chats(self):
        chats = self.client.get_dialogs()
        return chats
