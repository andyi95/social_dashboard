"""
Your project sounds interesting! Let's address your concerns step by step.

1. **Finding Words That Appear in All Posts from a Particular Group:**

   One way to identify these words is by making use of Django's ORM querying capabilities:

   ```python
   from django.db.models import Count

   group_id = <some_group_id>
   total_posts_in_group = Post.objects.filter(group_id=group_id).count()

   # Filtering words that appear in all posts
   frequently_appearing_words = PostWord.objects.filter(post__group_id=group_id) \
       .values('word') \
       .annotate(post_count=Count('post', distinct=True)) \
       .filter(post_count=total_posts_in_group)
   ```

   This will give you the words that appear in all posts of a particular group. If these words are not meaningful to your analysis, you can consider removing them just like stop words.

2. **Ideas for More In-depth Analysis:**

   - **Topic Modeling**: Use Latent Dirichlet Allocation (LDA) to identify the main topics present in the posts. Libraries like `gensim` are great for this. This can give you an idea of what subjects are frequently discussed in the posts.

   - **Sentiment Analysis**: By making use of libraries like TextBlob or NLTK's Vader, you can get a sentiment score for each post, allowing you to understand if the post has a positive, negative, or neutral sentiment.

   - **Word Embeddings**: Using models like Word2Vec, you can convert words into vectors and find similar words or even find semantic relations between words.

   - **Trending Topics**: Identify trending words/topics over time. This can be done by plotting word frequency against time.

   - **Clustering**: Use `scikit-learn` to cluster posts based on their content. This can help in grouping similar posts together.

   - **Predictive Models**: If you have some labeled data or can generate some, you could build models to predict certain post characteristics, like predicting if a post will get a high number of likes based on its content.

   - **Time Series Analysis**: Since you're storing `date` for each word, you can perform time series analysis to identify trends, seasonality, etc., in word usage.

3. **Other Suggestions**:

   - **Improved Text Cleaning**: Apart from removing stop words, consider handling things like emojis, URLs, mentions, and hashtags which might be frequent in social media posts.

   - **Named Entity Recognition (NER)**: Using libraries like `spaCy`, you can extract entities like person names, organizations, locations, etc., from the posts. This can give you insights into which entities are being talked about the most.

   - **TF-IDF Analysis**: Instead of just counting word frequency, consider using Term Frequency-Inverse Document Frequency (TF-IDF) to find out which words are important in a post relative to all posts.

   - **Expand Stop Words**: Based on the frequently appearing words and the context of your data (e.g., if you're scraping a specific platform or in a specific niche), you might want to expand your list of stop words.

Remember, the kind of analysis you can perform largely depends on the nature of your data and what insights you're aiming to extract. Always ensure you have the right to scrape and analyze the data, respecting user privacy and platform terms of service.

"""


from django.db import models


class Account(models.Model):
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    deactivated = models.BooleanField(blank=True, null=True)
    is_closed = models.BooleanField(blank=True, null=True)
    about = models.CharField(max_length=255, blank=True, null=True)
    activities = models.TextField(blank=True, null=True)
    bdate = models.DateTimeField(blank=True, null=True)
    last_seen = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'account'


class Group(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    screen_name = models.CharField(max_length=255, blank=True, null=True)
    is_closed = models.BooleanField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    contact_id = models.IntegerField(blank=True, null=True)
    group_id = models.IntegerField(blank=True, null=True)
    social_media_type = models.CharField(max_length=255, blank=True, null=True, verbose_name='тип соц. сети')

    class Meta:
        managed = False
        db_table = 'group'


class Post(models.Model):
    post_id = models.IntegerField(blank=True, null=True)
    group = models.ForeignKey(Group, models.DO_NOTHING, blank=True, null=True, related_name='posts')
    date = models.DateTimeField(blank=True, null=True, verbose_name='Publication timestamp in MSC tz')
    marked_as_ads = models.BooleanField(blank=True, null=True)
    post_type = models.CharField(max_length=32, blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    likes_count = models.IntegerField(blank=True, null=True)
    repost_count = models.IntegerField(blank=True, null=True)
    views_count = models.IntegerField(blank=True, null=True)
    comment_count = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'post'

    def __str__(self):
        return f'Пост от {self.date.date()} текст {self.text[:20]}'


class PostStats(models.Model):
    likes_count = models.IntegerField()
    repost_count = models.IntegerField()
    views_count = models.IntegerField()
    comment_count = models.IntegerField()
    post = models.ForeignKey(Post, models.DO_NOTHING, related_name='stats')

    class Meta:
        managed = False
        db_table = 'poststats'


class PostWord(models.Model):
    word = models.CharField(max_length=255, blank=True, null=True)
    post = models.ForeignKey(Post, models.DO_NOTHING, blank=True, null=True, related_name='words')
    date = models.DateField(blank=True, null=True, verbose_name='Publication date of original post in MSC tz')
    count = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'postword'

    def __str__(self):
        return self.word


class Comment(models.Model):
    from_field = models.ForeignKey(Account, models.DO_NOTHING, db_column='from_id', blank=True, null=True,
                                   verbose_name='ID of comment author')
    post = models.ForeignKey('Post', models.DO_NOTHING, blank=True, null=True)
    owner = models.ForeignKey('Group', models.DO_NOTHING, blank=True, null=True, verbose_name='ID of group feed with '
                                                                                             'the '
                                                                                     'comment')
    date = models.DateTimeField(blank=True, null=True, verbose_name='Publication timestamp in MSC tz')
    text = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'comment'
