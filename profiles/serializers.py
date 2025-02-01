from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Profile
from followers.models import Follower

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for creating new users.
    """
    password = serializers.CharField(write_only=True, min_length=8, required=True)
    password2 = serializers.CharField(write_only=True, min_length=8, required=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "password2"]
        extra_kwargs = {"email": {"required": True}}

    def validate_email(self, value):
        """Ensure email is unique."""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def validate(self, data):
        """Ensure passwords match."""
        if data["password"] != data["password2"]:
            raise serializers.ValidationError({"password": "Passwords must match."})
        return data

    def create(self, validated_data):
        """Create a new user with a hashed password."""
        validated_data.pop("password2")  # Remove password2 before saving
        return User.objects.create_user(**validated_data)
    

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
        return bool(request and request.user == obj.owner)

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
