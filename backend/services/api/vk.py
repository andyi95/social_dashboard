import json
import os
import random
from dataclasses import dataclass

import requests
from collections import namedtuple
from typing import Optional, Union
from urllib.parse import urlencode
from dotenv import load_dotenv
from .exceptions import APIException, TokenException, TooManyRequests
from time import sleep
load_dotenv()

User = namedtuple('User', 'id username first_name last_name link')

@dataclass
class Comment:
    id: str
    from_id: str
    date: str
    text: str


@dataclass
class Post:
    id: str
    from_id: str
    owner_id: str
    date: str
    post_type: str
    text: str
    likes_count: int
    repost_count: int
    comments_count: int
    views_count: int = 0
    marked_as_ads: bool = False


@dataclass
class Group:
    id: str
    name: str
    screen_name: str = ''
    is_closed: str = ''
    description: str = ''
    api: 'VkAPI' = None

    def get_posts(self, offset: int = 0, count: int = 100):
        url = self.api.base_url + 'wall.get'
        params = {
            'owner_id': self.id, 'offset': offset, 'count': count
        } | self.api.params
        response = self.api.get_object(url, params)
        response = response['response']['items']
        posts = []
        for item in response:
            posts.append(Post(
                id=item.get('id', ''), from_id=item.get('from_id'), post_type=item.get('post_type'), text=item.get('text'),
                date=item.get('date'), likes_count=item.get('likes', {}).get('count'),
                comments_count=item.get('comments', {}).get('count'), repost_count=item.get('reposts', {}).get('count'),
                owner_id=item.get('owner_id', self.id)
            ))
        return posts


class VkAPI:
    def __init__(self, access_token: str = ''):
        self.access_token = access_token if access_token else os.getenv('VK_API_TOKEN')
        self.app_id = os.getenv('VK_API_ID')
        self.session = requests.Session()
        self.base_url = f'https://api.vk.com/method/'
        self.version = '5.131'
        self.params = {
            'client_id': self.app_id, 'access_token': self.access_token,
            'v': self.version
        }

    def validate_response(self, response):
        if error := response.get('error'):
            if error.get('error_code') == 5:
                raise TokenException
            if error.get('error_code') == 6:
                raise TooManyRequests
            raise APIException(f'Error {response}')
        if not isinstance(response, dict) or 'response' not in response.keys():
            raise APIException(f'Unexpected type of response: {response}')
        return response

    def get_object(self, url: str, params: dict):
        # We should use Retrying module here probably
        response = self.session.get(url=url, params=params).json()
        counter = 1
        while response.get('error') and response['error'].get('error_code') == 6:
            sleep(counter)
            print(f'Too many request, sleeping {counter} secs')
            response = self.session.get(url=url, params=params).json()
            counter += 1
        if error := response.get('error'):
            raise APIException(f'Error fetching API: {error}')
        return response

    def get_group(self, group_id: str = ''):
        url = self.base_url + 'groups.getById'
        params = self.params | {
            'fields': 'description,is_closed,contacts,members_count,links',
            'group_ids': group_id
        }
        response = self.session.get(url, params=params).json()
        if error := response.get('error'):
            if error.get('error_code') == 5:
                raise TokenException('Invalid access token')
            raise APIException(f'Error {response}')
        if not isinstance(response, dict) or 'response' not in response.keys() or not isinstance(response['response'], list):
            raise APIException(f'Unexpected type of response: {response}')
        response = response['response'][0]
        return Group(
            id=response['id'], name=response['name'], screen_name=response['screen_name'], is_closed=response['is_closed'],
            description=response['description'], api=self
        )
