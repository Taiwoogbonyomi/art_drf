from django.db.models import Count
from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from art_drf.permissions import IsOwnerOrReadOnly
from .models import ArtPost
from .serializers import PostSerializer


class PostList(generics.ListCreateAPIView):
    """
    List posts or create a post if logged in.
    The perform_create method associates the post with the logged-in user.
    """
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    filterset_fields = [
        'owner__followed__owner__profile',
        'likes__owner__profile',
        'owner__profile',
    ]
    search_fields = [
        'title', 
        'owner__username'
    ]
    ordering_fields = [
        'likes_count',
        'comments_count',
        'likes__created_at',
        'created_at',
        'updated_at',
    ]
   
    def get_queryset(self):
        """
        Get all posts with annotated like and comment counts.
        """
        return ArtPost.objects.annotate(
            likes_count=Count('likes', distinct=True),
            comments_count=Count('comment', distinct=True)
        ).order_by('-created_at')

    def perform_create(self, serializer):
        """
        Associate the logged-in user with the new post.
        """
        serializer.save(owner=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve a post and edit or delete it if you own it.
    """
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        """
        Get a single post with annotated like and comment counts.
        """
        return Post.objects.annotate(
            likes_count=Count('likes', distinct=True),
            comments_count=Count('comment', distinct=True)
        ).order_by('-created_at')
