import pandas as pd

from app.db.session import Session
import sqlalchemy as sa
from sqlalchemy.exc import IntegrityError, NoResultFound
from app.db.base import Post, Group, PostWord

from fastapi import APIRouter, Path, Query

from app.schemas import WordStats

from typing import List
from datetime import date, datetime

session = Session()
router = APIRouter()

@router.get('/posts', response_model=List[WordStats])
def get_words(date__gt: str = None, date__lt: str = None, limit: int = None):
    """Get top """
    qs = session.query(
        PostWord.word, sa.func.max(PostWord.post_id).label('post_id'), sa.func.sum(PostWord.count).label('count'),
        sa.func.max(PostWord.date).label('date')
    ).group_by(PostWord.word).order_by(sa.desc(sa.func.sum(PostWord.count)))
    qs = qs.join(PostWord.post)
    if date__gt:
        date__gt = datetime.strptime(date__gt, '%Y-%m-%dT%H:%M:%S.%fZ')
        qs = qs.filter(
            Post.date.__gt__(datetime(date__gt.year, date__gt.month, date__gt.day))
        )
    if date__lt:
        date__lt = datetime.strptime(date__lt, '%Y-%m-%dT%H:%M:%S.%fZ')
        qs = qs.filter(
            Post.date.__lt__(datetime(date__lt.year, date__lt.month, date__lt.day))
        )
    if limit:
        qs = qs[:limit]
    return qs[:100]


@router.get('/words/{word}')
def get_word(word: str = Path(title='A single word for time series')):
    subq = session.query(sa.func.count(Post.id).label('all_posts_count'), sa.func.date(Post.date).label('dated')).subquery()
    qs = session.query(
        sa.func.date(Post.date),
        sa.cast(sa.func.count(Post.id).__div__(subq.c.all_posts_count), sa.Float)
    ).filter(Post.text.like(f'%{word}%')).join(
        subq, sa.func.date(Post.date)==subq.c.dated
    ).group_by(sa.func.date(Post.date), subq.c.date, subq.c.all_posts_count)
    # qs = session.query(sa.cast(Post.date, sa.Date).label('date'), sa.func.count(Post)).filter(Post.text.like(f'%{word}%')).group_by(cast(Post.date, Date))
    # qs = session.query(PostWord.date, PostWord.word, sa.func.count(PostWord).label('count')).filter(PostWord.word.like(word)).group_by(PostWord.date)
    df = pd.DataFrame.from_dict([row._asdict() for row in qs.all()])
