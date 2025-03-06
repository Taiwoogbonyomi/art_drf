from rest_framework import serializers
from .models import Profile
from followers.models import Follower


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the Profile model.
    Includes additional fields for ownership and following status.
    """
    owner = serializers.ReadOnlyField(source="owner.username")
    is_owner = serializers.SerializerMethodField()
    following_id = serializers.SerializerMethodField()
    posts_count = serializers.ReadOnlyField()
    followers_count = serializers.ReadOnlyField()
    following_count = serializers.ReadOnlyField()

    class Meta:
        model = Profile
        fields = [
            "id",
            "owner",
            "created_at",
            "updated_at",
            "name",
            "content",
            "image",
            "is_owner",
            "following_id",
            "posts_count",
            "followers_count",
            "following_count",
        ]

    def get_is_owner(self, obj):
        """Checks if the requesting user is the owner of the profile."""
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return obj.owner == request.user
        return False

    def get_following_id(self, obj):
        """
        Returns the ID of the Follower instance if the requesting user
        is following the profile owner, otherwise returns None.
        """
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            following = Follower.objects.filter(owner=request.user, followed=obj.owner)
            return following.first().id if following.exists() else None
        return None
