from django.urls import path
from commentslikes import views

urlpatterns = [
    path('commentslikes/', views.CommentsLikesList.as_view()),
    path('commentslikes/<int:pk>/', views.CommentsLikesDetail.as_view()),
]
