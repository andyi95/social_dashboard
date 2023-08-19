from rest_framework import serializers
from dashboard.models import PostWord, Post


class WordStatSerializer(serializers.Serializer):
    word = serializers.CharField(max_length=255)
    count = serializers.IntegerField()
    post_id = serializers.IntegerField()
    date = serializers.DateField()


class DetailStatSerializer(serializers.Serializer):
    date = serializers.DateField()
    post_count = serializers.IntegerField()
