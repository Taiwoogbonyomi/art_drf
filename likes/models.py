from django.db import models
from django.contrib.auth.models import User
from posts.models import ArtPost


class Like(models.Model):
    """
    Like model, related to 'owner' and 'post'.
    'owner' is a User instance and 'post' is a Post instance.
    'unique_like' ensures a user can't like the same post twice.
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(
        ArtPost, related_name='likes', on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['owner', 'post'], name='unique_like'
            )
        ]
        verbose_name = "Like"
        verbose_name_plural = "Likes"

    def __str__(self):
        return f'{self.owner.username} liked {self.post.title[:30]}'

    @classmethod
    def toggle_like(cls, user, post):
        """
        Toggles the like status for a given user and post.
        If the user has already liked the post, the like is removed.
        If not, a new like is created.
        """
        like, created = cls.objects.get_or_create(owner=user, post=post)
        if not created:
            like.delete()
            return False  # Like removed
        return True  # Like added
