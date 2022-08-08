from sqlalchemy import func, select, and_, or_
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.sql import ClauseElement
from nltk.corpus import stopwords
import pymorphy2 as py
import re
from app.db.base import Post, PostWord
from app.db.session import Session

session = Session()
morph = py.MorphAnalyzer()


class PostParser:
    def __init__(self, post: Post):
        self.post = post

    def parse(self):
        content = self.post.text
        words = {}
        for word in content.split():
            stripped = re.sub(r'[^\w\s]', '', word).lower()
            parsed = morph.parse(stripped)[0].normal_form
            if parsed in stopwords.words('russian') or len(parsed) > 255:
                continue
            words[parsed] = 1 if parsed not in words.keys() else words[parsed] + 1
        if q := session.query(PostWord).filter(and_(PostWord.word.in_(words.keys()), PostWord.post_id == self.post.id)).all():
            for instance in q:
                instance: PostWord
                instance.count = words[instance.word]
            session.commit()
            return
        instances = []
        for word, count in words.items():
            instances.append(
                PostWord(word=word, post_id=self.post.id, count=count, date=self.post.date.date())
            )
        session.add_all(instances)
        session.commit()

if __name__ == '__main__':
    subquery = ~session.query(PostWord).filter(PostWord.post_id == Post.id).exists()
    posts = session.query(Post).filter(Post.text != '', subquery).all()
    i = 0
    for post in posts:
        if i % 10:
            print(f'parsing post {post}')
        PostParser(post).parse()
        i += 1
