from django.db import models
from django.contrib.auth.models import User
from comments.models import Comment


class CommentLike(models.Model):
    """
    Model to track likes on comments.
    Ensures a user can only like a comment once.
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(
        Comment, related_name="likes", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['owner', 'comment'], name='unique_comment_like'
            )
        ]

    def __str__(self):
        return f"{self.owner.username} liked '{self.comment.content[:30]}...'"
