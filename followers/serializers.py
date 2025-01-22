from django.db import IntegrityError
from rest_framework import serializers
from .models import Follower

class FollowerSerializer(serializers.ModelSerializer):
    """
    Serializer for the Follower model
    Create method handles the unique constraint on 'owner' and 'followed'
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    followed_name = serializers.ReadOnlyField(source='followed.username')

    class Meta:
        model = Follower
        fields = ['id', 'owner', 'created_at', 'followed', 'followed_name']

    def validate_followed(self, value):
        """
        Ensure a user cannot follow themselves.
        """
        if self.context['request'].user == value:
            raise serializers.ValidationError("You cannot follow yourself.")
        return value

    def create(self, validated_data):
        """
        Custom create method to handle unique constraint errors gracefully.
        """
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError(
                {'detail': 'You are already following this user.'}
            )
