import pandas as pd
from tortoise.expressions import F, Subquery

from app.models import Post, PostWord, User
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi import APIRouter, Path, Depends, Request, HTTPException
from app.core.config import settings
from app.schemas import TimeSeries, UserAuth, WordStats, UserSignUp, UserRead
from tortoise.functions import Max, Count, Sum
from typing import List
from datetime import date, datetime
from pypika import Table, functions as fn
from tortoise import connections

router = APIRouter()


@router.get('/words', response_model=List[WordStats])
async def get_words(date__gt: str = None, date__lt: str = None, limit: int = None):
    """Get top """
    limit  = 100 if not limit else limit
    qs = PostWord.annotate(post_id=Max('post_id'), count=Sum('count'), date=Max('date')).group_by(
        'word').order_by(
        '-count').limit(limit)
    if date__gt:
        date__gt = datetime.strptime(date__gt, '%Y-%m-%dT%H:%M:%S.%fZ')
        qs = qs.filter(
            date__gt=date__gt
        )
    if date__lt:
        date__lt = datetime.strptime(date__lt, '%Y-%m-%dT%H:%M:%S.%fZ')
        qs = qs.filter(
            date__lt=date__lt
        )
    return await qs.all()


@router.get('/posts/{word}', response_model=List[TimeSeries])
async def get_word(word: str = Path(title='A single word for time series')):
    """
    https://github.com/tortoise/tortoise-orm/issues/683 check
    select count(p.id), date(p.date), a.post_count from postword
left join post p on p.id = postword.post_id
left join (
    select count(post.id) as post_count, date(post.date) as post_date from post group by date(post.date)
) as a on a.post_date = date(p.date)
where postword.word = 'прогноз'
group by date(p.date), a.post_count order by date(p.date);

    :param word:
    :return:
    """
    # subq = Post.annotate(date=fn.Date('date'), all_posts=Count('id')).group_by('date')
    pw = Table('postword')
    all_posts_count = await Post.filter(words__word=word).all().count()
    qs = PostWord.filter(word=word).annotate(posts_count=Sum('count'), date=fn.Date(
        pw.date)).group_by('date').order_by('-date')
    qs = qs.annotate(ratio=F('posts_count') / all_posts_count)
    data = await qs.all().values('date', 'posts_count')
    for item in data:
        item.update({
            'ratio': float(item['posts_count'] / all_posts_count)
        })
    return data
    conn = connections.get('default')
    data = await conn.execute_query(
        f'''
        select count(p.id), date(p.date), a.post_count from postword
left join post p on p.id = postword.post_id
left join (
    select count(post.id) as post_count, date(post.date) as post_date from post group by date(post.date)
) as a on a.post_date = date(p.date)
where postword.word = '{word}'
group by date(p.date), a.post_count order by date(p.date) asc;
'''
    )
    # qs = PostWord.filter(word=word).all().select_related('post')
    # all_posts_count = await Post.filter(words__word=word).all().count()
    # pw = Table('postword')
    # qs = await qs.annotate(
    #     count=Sum('count'), date=fn.Date(pw.date)
    # ).group_by('date', 'post').annotate(
    #     ratio=F('count') / all_posts_count
    # ).limit(100)
    return data


    # subq = session.query(
    #     sa.func.count(Post.id).distinct().label('all_posts'),
    #     sa.func.date(Post.date).label('date')
    # ).group_by(Post.date).subquery()
    # qs = session.query(
    #     sa.func.sum(PostWord.count).distinct().label('count'),
    #     subq.c.all_posts,
    #     sa.cast(sa.func.sum(PostWord.count).__div__(subq.c.all_posts), sa.Float).label('ratio'),
    #     sa.func.date(Post.date).label('date')
    # ).join(Post).join(subq, sa.func.date(Post.date) == subq.c.date).group_by(
    #     sa.func.date(Post.date), subq.c.all_posts
    # ).filter(PostWord.word == word)
    # return qs.limit(100).all()

user_router = APIRouter()


@user_router.post('auth/token/')
async def login(data: UserAuth, Authorize: AuthJWT = Depends()):
    user = await User.filter(username=data.username).first()
    # user = session.query(User).filter(User.username==data.username).scalar()
    if not user or not user.check_password(data.password):
        raise HTTPException(
            status_code=401, detail='Bad username or password'
        )
    access_token = Authorize.create_access_token(subject=user.username)
    return {'access_token': access_token}


@user_router.post('', response_model=UserRead)
async def signup(data: UserSignUp):
    if await User.filter(username=data.username).exists() or len(data.username) < 4:

    # if session.query(User).filter(User.username==data.username).scalar() or len(data.username) < 4:
        raise HTTPException(
            status_code=401, detail='Username is used'
        )
    user = User(**data.dict())
    user.set_password(data.password)
    await user.save()
    return user

# @user_router.get('', response_model=UserRead)
# def me():
