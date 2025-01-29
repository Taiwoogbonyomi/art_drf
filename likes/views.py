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
        Optionally, filter likes by the current user and post.
        If the user is not authenticated, return an empty queryset.
        """
        user = self.request.user
        if user.is_authenticated:
            queryset = Like.objects.filter(owner=user)
            post_id = self.request.query_params.get('post')  
            if post_id:
                try:
                    post_id = int(post_id)
                    queryset = queryset.filter(post_id=post_id)
                except ValueError:
                    raise ValidationError("Invalid 'post' value.")
            return queryset
        else:    
            return Like.objects.none()
   
    def perform_create(self, serializer):
        """
        Prevent duplicate likes for the same post by the same user.
        """
        if not self.request.user.is_authenticated:
            raise ValidationError("You must be logged in to like a post.")

        post = serializer.validated_data.get('post')  
        if Like.objects.filter(owner=self.request.user, post=post).exists():
            raise ValidationError("You have already liked this post.")

        serializer.save(owner=self.request.user)  

class LikeDetail(generics.RetrieveDestroyAPIView):
    """
    Retrieve a like or delete it by ID if you own it.
    """
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = LikeSerializer
    queryset = Like.objects.all()

    def perform_destroy(self, instance):
        """
        Ensure only the owner can delete their like.
        """
        if instance.owner != self.request.user:
            raise ValidationError("You can only delete your own likes.")
        instance.delete()
