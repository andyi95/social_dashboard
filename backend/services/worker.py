from services.api import VkAPI
from app.db.session import Session
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import Session, joinedload
from app.models.social import Post, PostWord, Group, Comment, Account
session = Session()

#
# class PostRetriever:
#     def get_posts(self, owner_id, req_limit=4800):
