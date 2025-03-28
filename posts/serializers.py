from rest_framework import serializers
from posts.models import ArtPost
from likes.models import Like


class ArtPostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    like_id = serializers.SerializerMethodField()
    likes_count = serializers.ReadOnlyField()
    comments_count = serializers.ReadOnlyField()
    category_name = serializers.CharField(
        source='category.name',
        read_only=True
    )

    def validate_image(self, value):
        if value.size > 2 * 1024 * 1024:
            raise serializers.ValidationError('Image size larger than 2MB!')
        if value.image.height > 4096:
            raise serializers.ValidationError(
                'Image height larger than 4096px!'
            )
        if value.image.width > 4096:
            raise serializers.ValidationError(
                'Image width larger than 4096px!'
            )
        return value

    def to_representation(self, instance):
        """Add human-readable image filter display."""
        data = super().to_representation(instance)
        data['image_filter_display'] = instance.get_image_filter_display()
        return data

    def get_is_owner(self, obj):
        """Check if the authenticated user owns the post."""
        request = self.context.get('request')
        return request.user == obj.owner if request else False

    def get_like_id(self, obj):
        """
        Returns the ID of the Like instance if the requesting user
        has liked the post, otherwise returns None.
        """
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            like = Like.objects.filter(owner=request.user, post=obj).first()
            return like.id if like else None
        return None

    class Meta:
        model = ArtPost
        fields = [
            'id', 'owner', 'is_owner', 'profile_id',
            'profile_image', 'created_at', 'updated_at',
            'title', 'content', 'category', 'category_name',
            'image', 'image_filter', 'like_id', 'likes_count',
            'comments_count',
        ]
