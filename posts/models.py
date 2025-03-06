from django.db import models
from django.contrib.auth.models import User
from categories.models import Category


class ArtPost(models.Model):
    """
    Post model, related to 'owner', i.e. a User instance.
    """
    image_filter_choices = [
        ('oil_painting', 'Oil Painting'),
        ('acrylic', 'Acrylic'),
        ('watercolor', 'Watercolor'),
        ('impressionist', 'Impressionist'),
        ('abstract_art', 'Abstract Art'),
        ('pencil_sketch', 'Pencil Sketch'),
        ('cubism', 'Cubism'),
        ('pop_art', 'Pop Art'),
        ('surrealism', 'Surrealism'),
        ('expressionism', 'Expressionism'),
        ('ink_wash', 'Ink Wash')
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True, default="No content provided.")
    image = models.ImageField(
        upload_to='images/',
        default='../default_post_tx8nvq',
        blank=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="art_posts"
    )
    image_filter = models.CharField(
        max_length=32,
        choices=image_filter_choices,
        default='oil_painting'
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    def __str__(self):
        return f'{self.id} {self.title[:30]}...'
