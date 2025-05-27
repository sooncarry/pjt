from django.db.models import F, Count
from django.utils import timezone
from datetime import timedelta
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer


class PostListCreateView(generics.ListCreateAPIView):
    """
    GET /api/community/?filter=hot&period=week&limit=10
    GET /api/community/?filter=popular&minCount=100
    기본: 최신순 전체 글 반환
    """
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        qs = Post.objects.all()
        filter_type = self.request.query_params.get('filter')

        if filter_type == 'hot':
            # 기간 계산 (기본 1주일)
            period = self.request.query_params.get('period', 'week')
            cutoff = (timezone.now() - timedelta(days=30)) if period == 'month' \
                     else (timezone.now() - timedelta(weeks=1))
            qs = qs.filter(created_at__gte=cutoff)

            # 조회수 + 좋아요수 + 댓글수 합산하여 정렬
            qs = (
                qs
                .annotate(
                    likes_count=Count('likes', distinct=True),
                    comments_count=Count('comments', distinct=True)
                )
                .annotate(
                    total_count=F('view_count') + F('likes_count') + F('comments_count')
                )
                .order_by('-total_count')
            )

            # 상위 N건만 (기본 10)
            try:
                limit = int(self.request.query_params.get('limit', 10))
            except (TypeError, ValueError):
                limit = 10
            return qs[:limit]

        elif filter_type == 'popular':
            # 최소 기준치 이상인 모든 글 (기본 합산 100 이상)
            try:
                min_cnt = int(self.request.query_params.get('minCount', 100))
            except (TypeError, ValueError):
                min_cnt = 100

            qs = (
                qs
                .annotate(
                    likes_count=Count('likes', distinct=True),
                    comments_count=Count('comments', distinct=True)
                )
                .annotate(
                    total_count=F('view_count') + F('likes_count') + F('comments_count')
                )
                .filter(total_count__gte=min_cnt)
                .order_by('-total_count')
            )
            return qs

        # 기본: 작성일 내림차순
        return qs.order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def retrieve(self, request, *args, **kwargs):
        post = self.get_object()
        # 조회수 1 증가
        Post.objects.filter(pk=post.pk).update(view_count=F('view_count') + 1)
        post.refresh_from_db()
        return super().retrieve(request, *args, **kwargs)


@api_view(['POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def toggle_like(request, pk):
    """
    POST /api/community/<pk>/like/
    인증된 사용자에 한해 좋아요 토글
    """
    if request.user.is_anonymous:
        return Response({'detail': '로그인이 필요합니다.'}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response({'detail': '게시글이 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

    if post.likes.filter(pk=request.user.pk).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return Response({'likes_count': post.likes.count()}, status=status.HTTP_200_OK)


class CommentCreateView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
