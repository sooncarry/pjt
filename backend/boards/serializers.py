# backend/community/serializers.py
from rest_framework import serializers
from .models import Post, Comment

class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')
    replies         = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('author',)

    def get_replies(self, obj):
        children = obj.replies.all()
        return CommentSerializer(children, many=True).data


class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')
    created_at      = serializers.DateTimeField(format='%Y-%m-%d', read_only=True)
    updated_at      = serializers.DateTimeField(format='%Y-%m-%d', read_only=True)
    view_count      = serializers.IntegerField(read_only=True)
    likes_count     = serializers.SerializerMethodField()
    likes           = serializers.SlugRelatedField(
                        many=True,
                        read_only=True,
                        slug_field='username'   # 좋아요 누른 유저명 리스트
                     )
    comments        = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'content',
            'category',
            'author_username',
            'created_at',
            'updated_at',
            'view_count',
            'likes_count',
            'likes',
            'comments',
        ]
        read_only_fields = (
            'author',
            'created_at',
            'updated_at',
            'view_count',
        )

    def get_likes_count(self, obj):
        return obj.likes.count()
