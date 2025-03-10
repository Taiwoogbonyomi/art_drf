from rest_framework import generics
from categories.models import Category
from categories.serializers import CategorySerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend


class CategoryList(generics.ListCreateAPIView):
    """
    List all categories or create a new one if authenticated.
    """
    queryset = Category.objects.all().order_by("name")
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [
        filters.SearchFilter,
        DjangoFilterBackend,
        filters.OrderingFilter,
    ]
    search_fields = ["name", "description"]
    ordering_fields = ["name", "created_at"]


class CategoryDetail(generics.RetrieveAPIView):
    """
    Retrieve a single category by its ID.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
