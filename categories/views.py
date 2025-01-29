from rest_framework import generics
from categories.models import Category
from categories.serializers import CategorySerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

class CategoryList(generics.ListAPIView):
    """
    List all categories.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'description']

class CategoryDetail(generics.RetrieveAPIView):
    """
    Retrieve a single category by its ID.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
