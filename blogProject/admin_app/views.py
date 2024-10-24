from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView,View
from rest_framework.generics import ListAPIView,DestroyAPIView
from rest_framework.response import Response
from django.db.models import Count
from rest_framework import permissions, status
from django.http import HttpResponse,JsonResponse
from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework import generics
from django.contrib.auth import get_user_model
from datetime import timedelta
import csv
import openpyxl
from openpyxl import Workbook
from blogApp.models import Category
from blogApp.serializers import CategorySerializer
from .serializers import *
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

class BlogPostScheduleCreateView(APIView):
    permission_classes = [permissions.IsAdminUser]  # Only superusers can schedule posts

    def post(self, request, *args, **kwargs):
        serializer = BlogPostSerializer(data=request.data)
        if serializer.is_valid():
            # Automatically set the status to 'draft' before the post is published
            serializer.save(author=request.user, status='draft')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PublishScheduledPostsView(View):
    def get(self, request):
        now = timezone.now()
        posts_to_publish = BlogPost.objects.filter(publish_at__lte=now, status='draft')

        for post in posts_to_publish:
            post.status = 'published'
            post.save()

        return JsonResponse({'message': 'Posts published', 'count': posts_to_publish.count()})

class DraftListView(generics.ListAPIView):
    queryset = BlogPost.objects.filter(status='draft')
    serializer_class = DraftSerializer
    permission_classes = [permissions.IsAdminUser]

class DraftDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BlogPost.objects.filter(status='draft')
    serializer_class = DraftSerializer
    permission_classes = [permissions.IsAdminUser]

class AdminDashboardView(APIView):
    permission_classes = [permissions.IsAdminUser]  # Only superusers or admins can access this

    def get(self, request):
        # Calculate the date range for the last 7 days
        one_week_ago = timezone.now() - timedelta(days=7)

        # Metrics for users registered in the last 7 days
        new_users_count = UserAccount.objects.filter(created_at__gte=one_week_ago).count()

        # Get the latest 5 blog posts
        latest_posts = BlogPost.objects.order_by('-created_at')[:5]

        # Get the most commented posts
        most_commented_posts = BlogPost.objects.annotate(comment_count=Count('comments')).order_by('-comment_count')[:5]

        # Collecting the key metrics
        dashboard_data = {
            'new_users_count': new_users_count,
            'latest_posts': [
                {'title': post.title, 'author': post.author.name, 'created_at': post.created_at}
                for post in latest_posts
            ],
            'most_commented_posts': [
                {'title': post.title, 'comments_count': post.comment_count}
                for post in most_commented_posts
            ],
        }

        return Response(dashboard_data)

class PendingPostsListView(generics.ListAPIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = PendingPostSerializer

    def get_queryset(self):
        return BlogPost.objects.filter(status='pending').order_by('-created_at')

class ApprovePostView(APIView):
    permission_classes = [permissions.IsAdminUser]  # Only admin can approve/reject

    def patch(self, request, pk):
        try:
            post = BlogPost.objects.get(pk=pk)
        except BlogPost.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

        status = request.data.get('status')
        if status in ['approved', 'rejected']:
            post.status = status
            post.save()
            return Response({'message': f'Post {status} successfully'}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)