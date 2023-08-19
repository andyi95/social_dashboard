from datetime import date

import nltk
import unicodedata
import os
import sys


import pymorphy3
from nltk.corpus import stopwords
from django.db.models import Q, F, Count
import re
morph = pymorphy3.MorphAnalyzer()

class PostParser:
    def __init__(self, post: 'Post'):
        self.post = post
        self.stopwords = stopwords.words('russian')
        self.stopwords.extend(
            ['новый', 'далее', 'стать', 'подробный']
        )

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

    # @staticmethod
    # def replace_numbers(words):
    #     """Replace all interger occurrences in list of tokenized words with textual representation"""
    #     p = inflect.engine()
    #     new_words = []
    #     for word in words:
    #         if word.isdigit():
    #             new_word = p.number_to_words(word)
    #             new_words.append(new_word)
    #         else:
    #             new_words.append(word)
    #     return new_words

    def parse(self):
        content = re.sub(r"http\S+", ' ', self.post.text)
        content = nltk.wordpunct_tokenize(content)
        content = self.to_lowercase(content)
        content = self.remove_punctuation(content)
        content = self.remove_stopwords(content)
        words = {}
        for word in content:
            parsed = morph.parse(word)[0].normal_form
            if parsed == '' or parsed in self.stopwords:
                continue
            words[parsed] = 1 if parsed not in words.keys() else words[parsed] + 1
        instances = []
        for word, count in words.items():
            instances.append(
                PostWord(word=word, post=self.post, count=count, date=self.post.date.date())
            )

        return instances



if __name__ == '__main__':
    sys.path.extend(['C:\\dev\\social_dashboard_django', 'C:\\dev\\social_dashboard_django\\backend',
                     'C:\\Program Files\\JetBrains\\PyCharm 2022.3.2\\plugins\\python\\helpers\\pycharm',
                     'C:\\Program Files\\JetBrains\\PyCharm 2022.3.2\\plugins\\python\\helpers\\pydev'])

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
    import django
    if 'setup' in dir(django):
        django.setup()
    from dashboard.models import Post, PostWord

    PostWord.objects.filter(post__date__gt=date(2023, 5, 1)).all().delete()
    # qs = Post.objects.filter(Q(words__isnull=True) & ~Q(text='')).order_by('id').all()[:1000]
    instances = []
    qs = Post.objects.filter(text__iregex=r'\w*[a-zA-Z]\w*').order_by('-id').all()
    j = 0
    for i, post in enumerate(qs):
        if post.words.exists():
            continue
        parser = PostParser(post)
        instances.extend(parser.parse())
        if len(instances) > 1000:
            print('creating 1000 words. Last one is ' + str(instances[-1]))
            PostWord.objects.bulk_create(instances)


