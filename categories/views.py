from rest_framework import generics
from .models import Category
from .serializers import CategorySerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

class CategoryList(generics.ListAPIView):
    """
    List all categories.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'description']  

    def get_queryset(self):
        """
        Optionally, filter categories by name or description.
        """
        queryset = super().get_queryset()
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(name__icontains=search) | queryset.filter(description__icontains=search)

        return queryset

class CategoryDetail(generics.RetrieveAPIView):
    """
    Retrieve a single category by its ID.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer