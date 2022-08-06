
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from typing import Any
from sqlalchemy.orm import declarative_base
AlchemyBase = declarative_base()

# class Base(AlchemyBase):
#     __abstract__ = True
#
#     @declared_attr
#     def __tablename__(cls):
#         return cls.__name__.lower()


@as_declarative()
class Base:
    id: Any
    __name__: str
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

from app.models.user import User
from app.models.social import Post, PostWord, Account, Group, Comment
