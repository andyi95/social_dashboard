from datetime import date
from typing import Literal

import nltk
import unicodedata
import os
import sys


import pymorphy3
from django.db.models import Sum
from langdetect import detect
from nltk.corpus import stopwords
from nltk import word_tokenize, pos_tag, wordpunct_tokenize
import re
from nltk.stem.snowball import SnowballStemmer
morph = pymorphy3.MorphAnalyzer()



class PostParser:
    def __init__(self, post: 'Post'):
        self.post = post
        self.stopwords = stopwords.words('russian')
        self.stopwords.extend(
            [
                'новый', 'далее', 'стать', 'подробный', 'это', 'ру', 'ленту', '2023', 'the', 'of', 'and', 'in', 'to',
                'lentaru'
            ]
        )
        self.stoptags_ru = ['NPRO', 'PREP', 'CONJ', 'PRCL', 'INTJ', 'NUMR', 'ROMN', 'UNKN']
        self.stoptags_en = ['CC', 'DT', 'EX', 'IN', 'LS', 'MD', 'PDT', 'POS', 'PRP', 'PRP$', 'TO', 'UH', 'WDT', 'WP',
                            'WP$', 'WRB', 'CD']

    def detect_lang(self, text):
        if re.search(r'[а-яА-Я]', text):
            return 'ru'
        if re.search(r'[a-zA-Z]', text):
            return 'en'
        return None

    @staticmethod
    def remove_URL(sample):
        """Remove URLs from a sample string"""
        return re.sub(r"http\S+", "", sample)

    @staticmethod
    def remove_non_ascii(words):
        """Remove non-ASCII characters from list of tokenized words"""
        new_words = []
        for word in words:
            new_word = unicodedata.normalize('NFKD', word).encode('ascii', 'ignore').decode('utf-8', 'ignore')
            new_words.append(new_word)
        return new_words

    def remove_stopwords(self, words: list):
        res = []
        for word in words:
            if word not in self.stopwords:
                res.append(word)
        return res

    @staticmethod
    def to_lowercase(words):
        """Convert all characters to lowercase from list of tokenized words"""
        new_words = []
        for word in words:
            new_word = word.lower()
            new_words.append(new_word)
        return new_words

    @staticmethod
    def remove_punctuation(words):
        """Remove punctuation from list of tokenized words"""
        new_words = []
        for word in words:
            new_word = re.sub(r'[^\w\s]', '', word)
            if new_word != '':
                new_words.append(new_word)
        return new_words

    def stem_words(self, words, lang: Literal['en', 'ru'] = 'ru'):
        if lang == 'ru':
            stemmed = [morph.parse(word)[0].normal_form for word in words]
        else:
            stemmed = [SnowballStemmer('english').stem(word) for word in words]
        return stemmed

    def parse(self, as_post_word=True):
        content = re.sub(r"http\S+", ' ', self.post.text)
        content = wordpunct_tokenize(content)
        content = self.to_lowercase(content)
        content = self.remove_punctuation(content)
        content = self.remove_stopwords(content)
        words = {}
        for word in content:
            if self.detect_lang(word) not in ('ru', 'en'):
                continue
            if self.detect_lang(word) == 'en':
                tagged = nltk.pos_tag([word])[0][1]
                if tagged in self.stoptags_en:
                    continue
                lemma = SnowballStemmer('english').stem(word)
            else:
                parsed = morph.parse(word)[0]
                lemma = parsed.normal_form
                if lemma == '' or lemma in self.stopwords or parsed.tag.POS in self.stoptags_ru:
                    continue
            words[lemma] = 1 if lemma not in words.keys() else words[lemma] + 1
        instances = []
        if not as_post_word:
            return content
        for word, count in words.items():
            instances.append(
                PostWord(word=word, post=self.post, count=count, date=self.post.date.date())
            )
        return instances

    def remove_stoptags(self):
        words_to_delete = []
        for instance in PostWord.objects.values('word').annotate(
                cnt=Sum('count')
        ).order_by('-cnt').all():
            if self.detect_lang(instance['word']) not in ('ru', 'en'):
                words_to_delete.append(instance['word'])
                continue
            if self.detect_lang(instance['word']) == 'en':
                tagged = nltk.pos_tag([instance['word']])
                if tagged in self.stoptags_en:
                    words_to_delete.append(instance['word'])
            if self.detect_lang(instance['word']) == 'ru':
                parsed = morph.parse(instance['word'])[0]
                if str(parsed.tag.POS) in self.stoptags_ru:
                    words_to_delete.append(instance['word'])
            if len(words_to_delete) > 1000:
                print(f'deleting {len(words_to_delete)} words. Last 100 is ' + ', '.join(words_to_delete[:100]))
                PostWord.objects.filter(word__in=words_to_delete).all().delete()
                words_to_delete = []
        a = 1
        PostWord.objects.filter(word__in=words_to_delete).all().delete()


if __name__ == '__main__':
    sys.path.extend(['C:\\dev\\social_dashboard_django', 'C:\\dev\\social_dashboard_django\\backend',
                     'C:\\Program Files\\JetBrains\\PyCharm 2022.3.2\\plugins\\python\\helpers\\pycharm',
                     'C:\\Program Files\\JetBrains\\PyCharm 2022.3.2\\plugins\\python\\helpers\\pydev', '/app'])

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
    import django
    if 'setup' in dir(django):
        django.setup()
    from apps.dashboard.models import Post, PostWord, Tag
    from django.conf import settings
    from django.db.models.functions import Length
    from openai import OpenAI
    api = OpenAI(api_key=settings.OPENAI_KEY)
    instances = []
    qs = Post.objects.filter(text__iregex=r'\w*[a-zA-Z]\w*', words__isnull=True).order_by('-id').all()
    promt = (f'classify the following text to one of the following tags. '
             f'The response should contain only one word - the tag. Here the list of tags: ')
    for tag in Tag.objects.all():
        promt += f' {tag.name}({tag.description}),'
    qs = Post.objects.annotate(t_len=Length('text')).filter(t_len__gte=100).order_by('-id').all()[:100]
    results = []
    for post in qs:
        content = promt + '\n. The post text is: ' + post.text
        res = api.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=[{'role': 'user', 'content': content}]
        )
        results.append(res)
        tag, created = Tag.objects.get_or_create(name=res.choices[0].message.content)
        post.tags.add(tag)

    print('wait')
    promt += '. The post text is: ' + post.text
    res = api.chat.completions.create(model='gpt-3.5-turbo', messages=[{'role': 'user', 'content': promt}])

    for i, post in enumerate(qs):
        parser = PostParser(post)
        instances.extend(parser.parse())
        if len(instances) > 1000:
            print('creating 1000 words. Last one is ' + str(instances[-1]))
            PostWord.objects.bulk_create(instances)
            instances = []
# def test_f():
#     Post.objects.filter(date__gte=date(2023, 1, 1)).count()
#     from sklearn.feature_extraction.text import TfidfVectorizer
#     from sklearn.naive_bayes import MultinomialNB
#     from sklearn.pipeline import make_pipeline
#     from sklearn.model_selection import train_test_split
#     from sklearn.metrics import classification_report
#
#     def preprocess_text(text):
#         """
#         Preprocess a given text by removing special characters, URLs, emojis, and performing tokenization,
#         stopwords removal, and lemmatization.
#         """
#         # Remove URLs
#         text = re.sub(r'https?://\S+|www\.\S+', '', text)
#
#         # Remove special characters, numbers, and punctuation (retain alphabetical characters and whitespace)
#         text = re.sub(r'[^a-zA-Z\s]', '', text)
#
#         # Remove tabs, new lines, and extra spaces
#         text = re.sub(r'\s+', ' ', text).strip()
#
#         # Lowercase
#         text = text.lower()
#
#         # Tokenize text
#         tokens = word_tokenize(text)
#
#         # Remove stopwords
#         stop_words = set(stopwords.words('english'))
#         tokens = [word for word in tokens if word not in stop_words]
#
#         # Lemmatization
#         lemmatizer = WordNetLemmatizer()
#         tokens = [lemmatizer.lemmatize(word) for word in tokens]
#
#         # Re-join tokens into a string
#         preprocessed_text = ' '.join(tokens)
#
#         return preprocessed_text
#
#     from openai import OpenAI
#     from django.conf import settings
#
#     settings.OPENAI_KEY
#     client = OpenAI(api_key=settings.OPENAI_KEY)
#     from django.db.models.functions import Length
#     from django.db.models import Max, Min, Avg
#     from django.db.models import Max, Min, Avg, Count
#
#     qs = Post.objects.annotate(t_len=Length('text')).values('t_len').filter(t_len__gte=100).annotate(
#         cnt=Count('id')).values('t_len', 'cnt')
#     qs = Post.objects.annotate(t_len=Length('text')).values('t_len').annotate(cnt=Count('id')).filter(t_len__gte=100,
#                                                                                                       cnt__gte=10).values(
#         't_len', 'cnt')
#     list(qs.order_by('-t_len')[:20])
#     Post.objects.filter(postword__isnull=True).count()
#     Post.objects.filter(words__isnull=True).count()
#     p = Post.objects.last()
#     from apps.user.models import User
#
#     User.objects.all()
#     User.objects.last()
#     for tag in Tag.objects.all():
#         promt += f' {[tag.name]}({tag.description},'
#
#     promt = f'classif the following text to one of the following tags: '
#     for tag in Tag.objects.all():
#         promt += f' {tag.name}({tag.description}),'
#
#     post = Post.objects.last()
#     promt += '. The post text is: ' + post.text
#     Post.objects.filter(words__isnull=True).count()
#     p = Post.objects.last()
#     from apps.user.models import User
#
#     User.objects.all()
#     User.objects.last()
#     for tag in Tag.objects.all():
#         promt += f' {[tag.name]}({tag.description},'
#     promt = f'classif the following text to one of the following tags: '
#     for tag in Tag.objects.all():
#         promt += f' {tag.name}({tag.description}),'
#     post = Post.objects.last()
#     promt += '. The post text is: ' + post.text
#     promt
#     promt = 'Determine the post topic from the following list'
#     for tag in Tag.objects.all():
#         promt += f' {tag.name}({tag.description}),'
#     post = Post.objects.last()
#     promt += '. The post text is: ' + post.text