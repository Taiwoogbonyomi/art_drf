from django.apps import AppConfig
from django.db.utils import OperationalError, ProgrammingError
from django.core.exceptions import ImproperlyConfigured


class CategoriesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'categories'

    def ready(self):
        """
        Auto-populate predefined categories when the app starts.
        """
        try:
            from categories.models import Category

            # Ensure the database is ready before making queries
            if not Category._meta.db_table:
                return

            CATEGORIES = [
                {
                    "name": "Portrait",
                    "description": "Art focused on human or animal figures",
                },
                {
                    "name": "Landscape",
                    "description": "Art featuring natural scenery"
                },
                {
                    "name": "Abstract",
                    "description": "Non-representational and conceptual art"
                },
                {
                    "name": "Still Life",
                    "description": "Art depicting inanimate objects"
                },
            ]

            for category_data in CATEGORIES:
                Category.objects.get_or_create(
                    name=category_data["name"],
                    defaults=category_data)

        except (OperationalError, ProgrammingError, ImproperlyConfigured):
            # Prevents issues if the database or migrations are not ready
            pass
