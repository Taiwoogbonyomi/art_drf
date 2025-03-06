from django.db import models
from django.contrib.auth.models import User
from posts.models import ArtPost


class Comment(models.Model):
    """
    Comment model, related to User and Post
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    post = models.ForeignKey(ArtPost, on_delete=models.CASCADE, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.TextField(max_length=1000)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        constraints = [
            models.UniqueConstraint(
                fields=['owner', 'post'], name='unique_user_comment')
        ]

    def __str__(self):
        return f'Comment by {self.owner.username} on {self.post.title[:20]}: {self.content[:30]}...'
