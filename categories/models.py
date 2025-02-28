from django.db import models


class Category(models.Model):
    """
    Category model to group art posts into categories like
    Portrait, Landscape, etc.
    """
    category_filter_choices = [
        ('portrait', 'Portrait'),
        ('landscape', 'Landscape'),
        ('abstract', 'Abstract'),
        ('still_life', 'Still Life'),
    ]

    name = models.CharField(
        max_length=50,
        choices=category_filter_choices,
        unique=True,
        default="Landscape"
    )
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.get_name_display()
