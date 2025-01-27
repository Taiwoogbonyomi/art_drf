from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError
from art_drf.permissions import IsOwnerOrReadOnly
from likes.models import Like
from likes.serializers import LikeSerializer

class LikeList(generics.ListCreateAPIView):
    """
    List likes or create a like if logged in.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = LikeSerializer

    def get_queryset(self):
        """
        Optionally, filter likes by the current user and art_post.
        If the user is not authenticated, return an empty queryset.
        """
        user = self.request.user
        if user.is_authenticated:
            queryset = Like.objects.filter(owner=user)
            
            # Optional filtering by art_post
            art_post = self.request.query_params.get('art_post')
            if art_post:
                try:
                    art_post = int(art_post)
                    queryset = queryset.filter(art_post_id=art_post)
                except ValueError:
                    raise ValidationError("Invalid 'art_post' value.")
            return queryset
        else:
            # Return an empty queryset if the user is not authenticated
            return Like.objects.none()

    def perform_create(self, serializer):
        """
        Prevent duplicate likes for the same ArtPost by the same user.
        """
        if not self.request.user.is_authenticated:
            raise ValidationError("You must be logged in to like a post.")
        
        art_post = serializer.validated_data.get('art_post')
        if Like.objects.filter(owner=self.request.user, art_post=art_post).exists():
            raise ValidationError("You have already liked this post.")
        
        serializer.save(owner=self.request.user)

class LikeDetail(generics.RetrieveDestroyAPIView):
    """
    Retrieve a like or delete it by id if you own it.
    """
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = LikeSerializer
    queryset = Like.objects.all()
