
from app.db.session import Session
from sqlalchemy import desc, select, func
from sqlalchemy.exc import IntegrityError, NoResultFound
from app.db.base import Post, Group, PostWord
session = Session()
from fastapi import APIRouter

from app.schemas import WordStats

from typing import List
from datetime import date, datetime

router = APIRouter()

@router.get('/words', response_model=List[WordStats])
def get_words(date__gt: date = None, date__lt: date = None, limit: int = None):
    qs = session.query(
        PostWord.word, func.max(PostWord.post_id).label('post_id'), func.sum(PostWord.count).label('count'),
        func.max(PostWord.date).label('date')
    ).group_by(PostWord.word).order_by(desc(func.sum(PostWord.count)))
    qs = qs.join(PostWord.post)
    if date__gt:
        qs = qs.filter(
            Post.date.__gt__(datetime(date__gt.year, date__gt.month, date__gt.day))
        )
    if date__lt:
        qs = qs.filter(
            Post.date.__lt__(datetime(date__lt.year, date__lt.month, date.day))
        )
    if limit:
        qs = qs[:limit]
    return qs
