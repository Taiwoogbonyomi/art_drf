from django.urls import path
from .views import CategoryList
from .views import CategoryDetail


urlpatterns = [
    path('categories/', CategoryList.as_view()),
    path('categories/<int:pk>/', CategoryDetail.as_view()),

]
