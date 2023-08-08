
from nltk.corpus import stopwords
import pymorphy3 as py
import re
from app.models import Post, Group, PostWord
from app.core.config import DB_URL
from tortoise import Tortoise
from tortoise.expressions import Q
from tortoise.functions import Max, Min
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

import asyncio
morph = py.MorphAnalyzer()
class TopicProcessor:
    def __init__(self, texts = None):
        self.texts = texts
        self.stopwords = stopwords.words('russian')
        self.stopwords.extend(
            ['новый', 'далее', 'стать', 'подробный']
        )

    def preprocess_text(self, text):
        tokens = word_tokenize(text.lower())
        tokens = [token for token in tokens if token.isalpha() and token not in self.stopwords]
        return " ".join(tokens)


class PostParser:
    def __init__(self, post: Post):
        self.post = post
        self.stopwords = stopwords.words('russian')
        self.stopwords.extend(
            ['новый', 'далее', 'стать', 'подробный']
        )

    async def parse(self):
        content = self.post.text
        words = {}
        for word in content.split():
            stripped = re.sub(r'[^\w\s]', '', word).lower()
            parsed = morph.parse(stripped)[0].normal_form
            if parsed == '' or parsed in stopwords.words('russian') or len(parsed) > 255:
                continue
            words[parsed] = 1 if parsed not in words.keys() else words[parsed] + 1
        if posts := await PostWord.filter(word__in=words.keys(), post=self.post).all():
            for instance in posts:
                instance.count = words[instance.word]
                await instance.save()
            return
        instances = []
        for word, count in words.items():
            instances.append(
                PostWord(word=word, post_id=self.post.id, count=count, date=self.post.date.date())
            )
        return instances


async def run():
    await Tortoise.init(
        db_url=DB_URL,
        modules={'models': ['app.models']}
    )
    # posts = await Post.filter(~Q(text = '')).order_by('date').limit(5)
    # proc = TopicProcessor()
    # preprocessed_texts  = [proc.preprocess_text(post.text) for post in posts]
    # tfidf_vectorizer = TfidfVectorizer(max_features=1000)  # You can adjust the max_features as needed
    # tfidf_matrix = tfidf_vectorizer.fit_transform(preprocessed_texts)
    # num_topics = 1  # You can adjust the number of topics based on your requirements
    # lda_model = LatentDirichletAllocation(n_components=num_topics, random_state=42)
    # lda_matrix = lda_model.fit_transform(tfidf_matrix)
    # main_topics = [topic.argmax() for topic in lda_matrix]
    # a = 1


async def process_posts():
    # posts = await Post.filter(~Q(text = '') & Q(id__gte=q_max[0].post_id)).order_by('id').all()
    while True:
        posts = await Post.filter(Q(words__isnull=True) & ~Q(text = '')).order_by('id').limit(10000).all()
        if not posts:
            print('The end')
            return
        instances = []
        for i, post in enumerate(posts):
            q = await PostWord.filter(post=post).exists()
            if q:
                continue
            instances.extend(
                await PostParser(post).parse()
            )
            if len(instances) >= 1000:
                print(f'Creating {len(instances)} posts. Last post {instances[-1]}')
                await PostWord.bulk_create(instances)
                instances = []


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run())
    try:
        loop.run_until_complete(process_posts())
    except KeyboardInterrupt:
        print('Interrupting')
        pass
