from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError
from commentslikes.models import CommentLike
from commentslikes.serializers import CommentLikeSerializer


class CommentLikeList(generics.ListCreateAPIView):
    """
    List all likes on comments or create a like if logged in.
    Prevents duplicate likes.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = CommentLikeSerializer

    def get_queryset(self):
        """
        Optionally filter likes by the current user and comment.
        If the user is not authenticated, return an empty queryset.
        """
        user = self.request.user
        queryset = CommentLike.objects.all()
        comment_id = self.request.query_params.get("comment")

        if comment_id:
            queryset = queryset.filter(comment_id=comment_id)

        if user.is_authenticated:
            return queryset
        return CommentLike.objects.none()

    def perform_create(self, serializer):
        """
        Prevent duplicate likes for the same comment by the same user.
        """
        comment = serializer.validated_data.get("comment")
        existing_like = CommentLike.objects.filter(
            owner=self.request.user, comment=comment
        ).first()

        if existing_like:
            raise ValidationError("You have already liked this comment.")

        serializer.save(owner=self.request.user)
