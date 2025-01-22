from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Follower(models.Model):
    """
    Follower model, related to 'owner' and 'followed'.
    'owner' is a User that is following a User.
    'followed' is a User that is followed by 'owner'.
    The related_name attribute allows Django to differentiate
    between 'owner' and 'followed' since both are User model instances.
    UniqueConstraint ensures a user can't follow the same user twice.
    """
    owner = models.ForeignKey(
        User, related_name='following', on_delete=models.CASCADE
    )
    followed = models.ForeignKey(
        User, related_name='followed', on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['owner', 'followed'], name='unique_follower_pair'
            )
        ]

    def __str__(self):
        return f'{self.owner.username} follows {self.followed.username}'

    def clean(self):
        """
        Prevent users from following themselves.
        """
        if self.owner == self.followed:
            raise ValidationError("You cannot follow yourself.")
