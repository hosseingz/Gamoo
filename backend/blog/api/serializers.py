from rest_framework import serializers
from blog.models import Post

class PostListSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'slug',
            'author',
            'cover_image',
            'reading_time',
            'created_at'
        ]

    def get_author(self, obj) -> str:
        full_name = obj.author.get_full_name()
        if full_name:
            return full_name
        return obj.author.username

class PostDetailSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'slug',
            'author',
            'cover_image',
            'reading_time',
            'created_at',
            'content',
            'updated_at'
        ]

    def get_author(self, obj) -> str:
        full_name = obj.author.get_full_name()
        if full_name:
            return full_name
        return obj.author.username
