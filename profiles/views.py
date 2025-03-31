from django.db.models import Count
from rest_framework import generics,  filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import get_object_or_404
from .models import Profile
from .serializers import ProfileSerializer
from art_drf.permissions import IsOwnerOrReadOnly


class ProfileList(generics.ListAPIView):
    """
    List all profiles.
    No create view (POST method),
    as profile creation is handled by Django signals.
    """
    serializer_class = ProfileSerializer
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend
    ]
    filterset_fields = [
        'owner__following__followed__profile',
        'owner__followed__owner__profile'
    ]
    search_fields = [
        'owner__username',
        'name'
    ]
    ordering_fields = [
        'posts_count',
        'followers_count',
        'following_count',
        'owner__following__created_at',
        'owner__followed__created_at',
    ]

    def get_queryset(self):
        """
        Retrieve all profiles with an optional filter by username,
        and include post/follower/following counts.
        """
        queryset = Profile.objects.annotate(
            posts_count=Count('owner__artpost', distinct=True),
            followers_count=Count('owner__followed', distinct=True),
            following_count=Count('owner__following', distinct=True)
        ).order_by('-created_at')

        username = self.request.query_params.get('username')
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
        Retrieve profiles with related counts for optimized performance.
        """
        return Profile.objects.annotate(
            posts_count=Count('owner__artpost', distinct=True),
            followers_count=Count('owner__followed', distinct=True),
            following_count=Count('owner__following', distinct=True)
        )

    def get_object(self):
        """
        Use DRF's get_object_or_404 for cleaner error handling.
        """
        return get_object_or_404(self.get_queryset(), pk=self.kwargs.get('pk'))
