from rest_framework import generics, permissions
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
        Optionally, filter likes by the current user.
        """
        user = self.request.user
        return Like.objects.filter(owner=user)

    def perform_create(self, serializer):
        """
        Override to assign the logged-in user as the owner of the like.
        """
        serializer.save(owner=self.request.user)

class LikeDetail(generics.RetrieveDestroyAPIView):
    """
    Retrieve a like or delete it by id if you own it.
    """
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = LikeSerializer
    queryset = Like.objects.all()
