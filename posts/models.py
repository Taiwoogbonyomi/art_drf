from django.db import models
from django.contrib.auth.models import User
from categories.models import Category
from cloudinary.models import CloudinaryField


class ArtPost(models.Model):
    """
    Post model, related to 'owner', i.e., a User instance.
    Uses Cloudinary for image uploads.
    """

    class ImageFilterChoices(models.TextChoices):
        OIL_PAINTING = "oil_painting", "Oil Painting"
        ACRYLIC = "acrylic", "Acrylic"
        WATERCOLOR = "watercolor", "Watercolor"
        IMPRESSIONIST = "impressionist", "Impressionist"
        ABSTRACT_ART = "abstract_art", "Abstract Art"
        PENCIL_SKETCH = "pencil_sketch", "Pencil Sketch"
        CUBISM = "cubism", "Cubism"
        POP_ART = "pop_art", "Pop Art"
        SURREALISM = "surrealism", "Surrealism"
        EXPRESSIONISM = "expressionism", "Expressionism"
        INK_WASH = "ink_wash", "Ink Wash"

    owner = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True, default="No content provided.")
    image = CloudinaryField(
        'image',
        default='../default_post_tx8nvq',
        blank=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="art_posts",
        db_index=True,
    )
    image_filter = models.CharField(
        max_length=32,
        choices=ImageFilterChoices.choices,
        default=ImageFilterChoices.OIL_PAINTING,
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    def __str__(self):
        return f'{self.id} {self.title[:30]}...'
