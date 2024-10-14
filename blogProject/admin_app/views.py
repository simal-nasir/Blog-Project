from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView,DestroyAPIView
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework import generics
from django.contrib.auth import get_user_model
from blogApp.models import Category
from blogApp.serializers import CategorySerializer
from .serializers import AdminUserSerializer
from blogApp.models import BlogPost
from blogApp.serializers import BlogPostSerializer


class CategoryCreateView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoryDeleteView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def delete(self, request, category_id):
        try:
            category = Category.objects.get(id=category_id)
            category.delete() 
            return Response({"message": "Category deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Category.DoesNotExist:
            return Response({"error": "Category not found."}, status=status.HTTP_404_NOT_FOUND)

class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

User = get_user_model()

class AdminUserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = AdminUserSerializer
    permission_classes = [IsAdminUser]

User = get_user_model()

class AdminUserDeleteView(DestroyAPIView):
    queryset = User.objects.all()
    lookup_field = 'id'
    permission_classes = [IsAdminUser]

    def perform_destroy(self, instance):
        if instance.is_superuser:
            raise ValidationError({"error": "You cannot delete another superuser."})
        super().perform_destroy(instance)


class BlogPostEditView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def patch(self, request, post_id):
        try:
            post = BlogPost.objects.get(id=post_id)
        except BlogPost.DoesNotExist:
            return Response({"error": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = BlogPostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BlogPostDeleteView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def delete(self, request, post_id):
        try:
            post = BlogPost.objects.get(id=post_id)
            post.delete()
            return Response({"message": "Post deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except BlogPost.DoesNotExist:
            return Response({"error": "Post not found."}, status=status.HTTP_404_NOT_FOUND)