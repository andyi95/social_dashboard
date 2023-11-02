from rest_framework import serializers
from apps.dashboard.models import PostWord, Post, Group


class WordStatSerializer(serializers.Serializer):
    word = serializers.CharField(max_length=255)
    count = serializers.IntegerField()
    post_id = serializers.IntegerField()
    date = serializers.DateField()


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    group = GroupSerializer()
    class Meta:
        model = Post
        fields = '__all__'




class DetailStatSerializer(serializers.Serializer):
    date = serializers.DateField()
    post_count = serializers.IntegerField()
