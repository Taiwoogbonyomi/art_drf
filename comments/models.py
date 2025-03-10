from django.db import models
from django.contrib.auth import get_user_model
from posts.models import ArtPost

User = get_user_model()


class Comment(models.Model):
    """
    Comment model, related to User and Post
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    post = models.ForeignKey(
        ArtPost, on_delete=models.CASCADE,
        db_index=True, related_name="comments"
    )
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True,
        related_name="replies"
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.TextField(max_length=1000)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

    def __str__(self):
        return f'Comment by {self.owner.username} on {
            getattr(self.post, "title", "Unknown Post")
            [:20]}: {self.content[:30]}...'

    @property
    def is_reply(self):
        """Checks if this comment is a reply to another comment."""
        return self.parent is not None
