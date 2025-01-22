from rest_framework import generics, permissions
from rest_framework.exceptions import NotFound
from .models import Profile
from .serializers import ProfileSerializer
from art_drf.permissions import IsOwnerOrReadOnly


class ProfileList(generics.ListAPIView):
    """
    List all profiles.
    No create view (POST method), as profile creation is handled by Django signals.
    """
    serializer_class = ProfileSerializer

    def get_queryset(self):
        """
        Retrieve all profiles with an optional filter by username.
        """
        queryset = Profile.objects.all()
        username = self.request.query_params.get('username', None)
        if username:
            queryset = queryset.filter(owner__username=username)
        return queryset


class ProfileDetail(generics.RetrieveUpdateAPIView):
    """
    Retrieve or update a profile.
    Only the owner of the profile can update it.
    """
    serializer_class = ProfileSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        """
        Always call `all()` to avoid queryset caching issues.
        """
        return Profile.objects.all()

    def get_object(self):
        """
        Override get_object to provide custom error handling.
        """
        queryset = self.get_queryset()
        pk = self.kwargs.get('pk')
        try:
            return queryset.get(pk=pk)
        except Profile.DoesNotExist:
            raise NotFound(detail="Profile not found.")
