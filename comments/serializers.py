from django.contrib.humanize.templatetags.humanize import naturaltime
from rest_framework import serializers
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Comment model
    Adds extra fields when returning a list of Comment instances
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        """Checks if the requesting user is the owner of the comment."""
        request = self.context.get("request")
        return request.user.is_authenticated and obj.owner == request.user if request else False

    def get_created_at(self, obj):
        """Returns a human-readable timestamp (e.g., '5 minutes ago')."""
        return {
            "humanized": naturaltime(obj.created_at),
            "iso_format": obj.created_at.isoformat(),
        }

    def get_updated_at(self, obj):
        """Returns a human-readable timestamp (e.g., '5 minutes ago')."""
        return {
            "humanized": naturaltime(obj.updated_at),
            "iso_format": obj.updated_at.isoformat(),
        }

    def get_profile_image(self, obj):
        if hasattr(obj.owner, 'profile') and obj.owner.profile.image:
            return obj.owner.profile.image.url
        return None

    def validate_content(self, value):
        """Ensures comment content is not empty or too long."""
        if not value.strip():
            raise serializers.ValidationError(
                "Comment content cannot be empty."
            )
        if len(value) > 1000:
            raise serializers.ValidationError(
                "Comment content exceeds 1000 characters."
            )
        return value

    class Meta:
        model = Comment
        fields = [
            'id', 'owner', 'is_owner', 'profile_id', 'profile_image',
            'post', 'created_at', 'updated_at', 'content'
        ]
        read_only_fields = ['owner', 'created_at', 'updated_at']


class CommentDetailSerializer(CommentSerializer):
    """
    Serializer for the Comment model used in Detail view.
    The 'post' field is read-only to prevent modification during updates,
    ensuring it remains associated with the correct post.
    """
    post = serializers.ReadOnlyField(source='post.id')

    class Meta(CommentSerializer.Meta):
        pass
