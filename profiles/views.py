from django.contrib.auth.models import User
from django.db.models import Count
from rest_framework import generics, permissions, filters, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Profile
from .serializers import ProfileSerializer, UserSerializer
from art_drf.permissions import IsOwnerOrReadOnly


class RegisterUserAPIView(APIView):
    """
    API view for user registration.
    Allows new users to sign up by providing a username and password.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = NewUserSerializer(data=request.data)
        
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            # Create a new user and hash the password automatically
            user = User.objects.create_user(username=username, password=password)

            return Response(
                {"message": "User registered successfully!", "user_id": user.id},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileList(generics.ListAPIView):
    """
    List all profiles.
    No create view (POST method), as profile creation is handled by Django signals.
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
