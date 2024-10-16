from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView,DestroyAPIView
from rest_framework.response import Response
from rest_framework import permissions, status
from django.http import HttpResponse
from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework import generics
from django.contrib.auth import get_user_model
import csv
import openpyxl
from openpyxl import Workbook
from blogApp.models import Category
from blogApp.serializers import CategorySerializer
from .serializers import AdminUserSerializer
from blogApp.models import *
from blogApp.serializers import *
from accounts.models import UserAccount


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


class ExportCSVView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        # Create the HttpResponse object with the CSV header.
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="blog_posts_report.csv"'

        # Create a CSV writer
        writer = csv.writer(response)
        writer.writerow(['Title', 'Author', 'Category', 'Created At', 'Likes', 'Comments Count'])

        # Query the data you want to include in the report
        posts = BlogPost.objects.all()

        for post in posts:
            writer.writerow([post.title, post.author.name, post.category, post.created_at, post.likes.count(), post.comments.count()])

        return response


class ExportExcelView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "Blog Posts Report"

        # Add headers
        sheet.append(['Title', 'Author', 'Category', 'Created At', 'Likes', 'Comments Count'])

        # Fetch all blog posts
        posts = BlogPost.objects.all()

        for post in posts:
            # Convert category and author to simple strings, and count likes and comments
            category_name = post.category.name if post.category else 'No Category'
            author_name = post.author.name
            created_at = post.created_at.strftime('%Y-%m-%d %H:%M:%S')  # Convert datetime to string

            # Append the data to the sheet
            sheet.append([post.title, author_name, category_name, created_at, post.likes.count(), post.comments.count()])

        # Prepare response as Excel file
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=blog_posts_report.xlsx'

        # Save the workbook to the response
        workbook.save(response)

        return response