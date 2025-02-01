from django.urls import path
from .views import RegisterUserAPIView, ProfileList, ProfileDetail 

urlpatterns = [
    path('register/', RegisterUserAPIView.as_view(),),
    path('profiles/', ProfileList.as_view()),
    path('profiles/<int:pk>/', ProfileDetail.as_view()),
]