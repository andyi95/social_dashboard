from pydantic import BaseModel
from datetime import date


class WordStats(BaseModel):
    word: str
    count: int
    post_id: int
    date: date