from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Post
from .serializers import PostSerializer
from art_drf.permissions import IsOwnerOrReadOnly


class PostList(generics.ListCreateAPIView):
    """
    Retrieve a list of posts or create a new post if authenticated.
    
    - GET: Returns all posts, optionally filtered by title.
    - POST: Creates a new post associated with the logged-in user.
    """
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """
        Optionally filter posts by title (case insensitive).
        """
        queryset = super().get_queryset()
        title_filter = self.request.query_params.get('title', None)
        if title_filter:
            queryset = queryset.filter(title__icontains=title_filter)
        return queryset

    def perform_create(self, serializer):
        """
        Associates the logged-in user with the new post.
        """
        try:
            serializer.save(owner=self.request.user)
        except Exception as e:
            raise Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a post if the user is the owner.

    - GET: Retrieve a specific post.
    - PUT/PATCH: Update a post if the owner.
    - DELETE: Remove a post if the owner.
    """
    queryset = Post.objects.select_related('owner')
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_object(self):
        """
        Get the post object or return a 404 error.
        Ensures proper permission checks.
        """
        post = get_object_or_404(self.get_queryset(), pk=self.kwargs.get('pk'))
        self.check_object_permissions(self.request, post)
        return post
