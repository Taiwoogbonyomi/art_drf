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
        Returns the profile image URL if available, otherwise None.
        Prevents AttributeError if the profile is missing.
        """
        profile = getattr(obj, 'profile', None)
        if profile and profile.image:
            return profile.image.url
        return None  
