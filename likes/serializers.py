from rest_framework import serializers
from likes.models import Like
from django.db import IntegrityError


class LikeSerializer(serializers.ModelSerializer):
    """
    Serializer for the Like model.
    The create method handles the unique constraint on 'owner' and 'post'.
    """
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Like
        fields = ['id', 'created_at', 'owner', 'post']

    def create(self, validated_data):
        """
        Handle unique constraint gracefully by catching integrity errors.
        """
        try:
            return Like.objects.create(**validated_data)
        except IntegrityError:
            raise serializers.ValidationError(
                {'detail': 'You have already liked this post.'}
            )
