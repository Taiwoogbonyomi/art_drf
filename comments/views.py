from rest_framework import generics, permissions
from art_drf.permissions import IsOwnerOrReadOnly
from .models import Comment
from .serializers import CommentSerializer, CommentDetailSerializer

class CommentList(generics.ListCreateAPIView):
    """
    Retrieve a list of comments or create a new comment if authenticated.

    - GET: Returns a list of comments.
    - POST: Creates a new comment associated with the logged-in user.
    """
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Comment.objects.select_related('owner', 'post').order_by('-created_at')
    

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve a comment, or update/delete it if you are the owner.

    - GET: Retrieve a specific comment by ID.
    - PUT/PATCH: Update the comment if the owner.
    - DELETE: Delete the comment if the owner.
    """
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = CommentDetailSerializer
    queryset = Comment.objects.select_related('owner', 'post').order_by('-created_at')

