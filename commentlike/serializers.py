from rest_framework import serializers
from commentlike.models import CommentLike


class CommentLikeSerializer(serializers.ModelSerializer):
    """
    Serializer for CommentLike model.
    Handles like creation with unique constraint validation.
    """
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = CommentLike
        fields = ["id", "owner", "comment", "created_at"]

    def create(self, validated_data):
        """
        Handle unique constraint gracefully by catching IntegrityError.
        Prevents users from liking the same comment multiple times.
        """
        from django.db import IntegrityError

        try:
            return CommentLike.objects.create(**validated_data)
        except IntegrityError:
            raise serializers.ValidationError(
                {"detail": "You have already liked this comment."}
            )
