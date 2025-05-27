from rest_framework import serializers
from .models import Post, Comment

class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('author',)

    def get_replies(self, obj):
        children = obj.replies.all()
        return CommentSerializer(children, many=True).data


class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')
    likes_count = serializers.SerializerMethodField()
    likes = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='username'  # ✅ 좋아요 누른 사람들의 username 목록
    )
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ('author',)

    def get_likes_count(self, obj):
        return obj.likes.count()
