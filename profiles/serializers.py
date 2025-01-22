from rest_framework import serializers
from .models import Profile
from followers.models import Follower


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the Profile model.
    Includes additional fields for ownership and following status.
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    following_id = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = [
            'id', 'owner', 'created_at', 'updated_at', 'name',
            'content', 'image', 'is_owner', 'following_id',
        ]

    def get_is_owner(self, obj):
        """
        Checks if the requesting user is the owner of the profile.
        """
        request = self.context.get('request', None)
        return request and request.user == obj.owner

    def get_following_id(self, obj):
        """
        Returns the ID of the Follower instance if the requesting user
        is following the profile owner, otherwise returns None.
        """
        request = self.context.get('request', None)
        if request and request.user.is_authenticated:
            following = Follower.objects.filter(
                owner=request.user, followed=obj.owner
            ).first()
            return following.id if following else None
        return None
