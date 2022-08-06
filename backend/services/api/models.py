from dataclasses import dataclass


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
    api = None
