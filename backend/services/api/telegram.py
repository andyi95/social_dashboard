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
        session_file = os.path.join(os.getenv('SESSION_DIR', '.'), 'telegram_client.session')
        self.client = TelegramClient(session_file, int(app_id), app_secret, system_version='4.16.30-vxCUSTOM')

    async def start_client(self):
        if not await self.client.is_user_authorized():
            await self.client.start()
        else:
            print('Client already connected')

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

    # def __del__(self):
    #     print('going disconnect')
    #     self.client.disconnect()

    async def __aenter__(self):
        await self.start_client()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print('Disconnecting client')
        await self.client.disconnect()
        