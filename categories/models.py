from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    CATEGORY_CHOICES = [
        ('portrait', 'Portrait'),
        ('landscape', 'Landscape'),
    ]
    """
    Category model to group art posts into categories like Portrait, Landscape, etc.
    """
    name = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        unique=True
    )
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name
