from django.shortcuts import get_object_or_404
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from .models import Post
from .serializers import PostSerializer
from art_drf.permissions import IsOwnerOrReadOnly



class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]
    

    def get(self, request):
        posts = Post.objects.all()
        title_filter = request.query_params.get('title', None)
        if title_filter:
            posts = posts.filter(title__icontains=title_filter)
        posts = posts.order_by('-created_at')
        serializer = PostSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        serializer = PostSerializer(
            data=request.data, context={'request': request}
        )
        if serializer.is_valid():
            try:
                serializer.save(owner=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PostDetail(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.select_related('owner').all()
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_object(self, pk):
        post = get_object_or_404(
            Post.objects.select_related('owner'), 
            pk=pk
        )
        self.check_object_permissions(self.request, post)
        return post

    def get(self, request, pk):
        post = self.get_object(pk)
        serializer = PostSerializer(
            post, context={'request': request}
        )
        return Response(serializer.data)

    def put(self, request, pk):
        post = self.get_object(pk)
        serializer = PostSerializer(
            post, 
            data=request.data, 
            context={'request': request}
        )
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data)
            except Exception as e:
                return Response(
                    {"error": str(e)}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        return Response(
            serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST
        )


    
    def delete(self, request, pk):
        post = self.get_object(pk)
        post.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )

