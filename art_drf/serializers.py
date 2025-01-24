from dj_rest_auth.serializers import UserDetailsSerializer
from rest_framework import serializers


class CurrentUserSerializer(UserDetailsSerializer):
    profile_id = serializers.ReadOnlyField(source='profile.id')
    profile_image = serializers.SerializerMethodField()

    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + (
            'profile_id', 'profile_image'
        )

    def get_profile_image(self, obj):
        """
        Safely retrieve the profile image URL or return a default value.
        """
        if hasattr(obj, 'profile') and obj.profile.image:
            return obj.profile.image.url
        return None  # Or provide a default image URL
