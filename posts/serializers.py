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
        """Validate image size and dimensions."""
        max_size = 2 * 1024 * 1024  # 2MB
        max_dimension = 4096

        if value.size > max_size:
            raise serializers.ValidationError(
                'Image size must be less than 2MB!')
        width = getattr(value, 'width', None)
        height = getattr(value, 'height', None)

        if width > max_dimension or height > max_dimension:
            raise serializers.ValidationError(
                f"Image dimensions must be at most {max_dimension}px."
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
