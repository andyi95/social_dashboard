from pydantic import BaseModel
from datetime import date, datetime


class ORMModel(BaseModel):
    class Config:
        orm_mode = True


class WordStats(BaseModel):
    word: str
    count: int
    post_id: int
    date: date


class TimeSeries(BaseModel):
    date: date
    posts_count: int
    ratio: float


class UserAuth(BaseModel):
    username: str
    password: str



class UserSignUp(BaseModel):
    username: str
    email: str
    password: str
    first_name: str
    last_name: str


class UserRead(ORMModel):
    username: str
    first_name: str
    last_name: str
    email: str