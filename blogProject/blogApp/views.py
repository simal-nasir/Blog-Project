from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.generics import ListAPIView, CreateAPIView,DestroyAPIView,UpdateAPIView,RetrieveAPIView
from rest_framework.views import APIView
from django.db.models import Count
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
import re
from .models import *
from accounts.models import UserAccount
from .serializers import *

class ProfileRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.profile

class BlogPostCreateView(CreateAPIView):
    serializer_class = BlogPostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        content = serializer.validated_data.get('content')
        tags = re.findall(r'#(\w+)', content)

        tag_objects = []
        for tag_name in tags:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            tag_objects.append(tag)

        category_id = self.request.data.get('category')
        category = Category.objects.get(id=category_id)

        blog_post = serializer.save(author=self.request.user, category=category)

        blog_post.tags.set(tag_objects)

class BlogPostByCategoryView(ListAPIView):
    serializer_class = BlogPostSerializer

    def get_queryset(self):
        category_name = self.kwargs['category']
        return BlogPost.objects.filter(category__name=category_name)

# View blog posts by author
class BlogPostByAuthorView(ListAPIView):
    serializer_class = BlogPostSerializer

    def get_queryset(self):
        author_id = self.kwargs['author_id']
        return BlogPost.objects.filter(author__id=author_id)

# View blog posts by tag
class BlogPostByTagView(ListAPIView):
    serializer_class = BlogPostSerializer

    def get_queryset(self):
        tag_name = self.kwargs['tag']
        return BlogPost.objects.filter(tags__name=tag_name)

class TagListView(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class BlogPostSearchView(ListAPIView):
    serializer_class = BlogPostSerializer

    def get_queryset(self):
        query = self.request.query_params.get('q', None)
        if query:
            return BlogPost.objects.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(tags__name__icontains=query) |
                Q(category__name__icontains=query)
            ).distinct()
        return BlogPost.objects.all()

class CommentListView(generics.ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Comment.objects.filter(post__id=post_id, parent=None).order_by('-created_at')  # Only top-level comments

class CommentCreateView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        post_id = self.kwargs['post_id']
        post = BlogPost.objects.get(id=post_id)
        comment = serializer.save(author=self.request.user, post=post)
        ActivityLog.objects.create(user=self.request.user, post=post, action='commented')
        

class ToggleLikeView(APIView):
    def post(self, request, post_id):
        try:
            post = BlogPost.objects.get(id=post_id)
            user = request.user

            if user in post.likes.all():
                post.likes.remove(user) 
            else:
                post.likes.add(user)     
                post.dislikes.remove(user) 

            return Response({'status': 'success', 'likes': post.likes.count(), 'dislikes': post.dislikes.count()}, status=status.HTTP_200_OK)
        except BlogPost.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)


class ToggleDislikeView(APIView):
    def post(self, request, post_id):
        try:
            post = BlogPost.objects.get(id=post_id)
            user = request.user

            if user in post.dislikes.all():
                post.dislikes.remove(user)
            else:
                post.dislikes.add(user)
                post.likes.remove(user)
            return Response({'status': 'success', 'likes': post.likes.count(), 'dislikes': post.dislikes.count()}, status=status.HTTP_200_OK)
        except BlogPost.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

class BookmarkPostView(APIView):
    def post(self, request, post_id):
        try:
            post = BlogPost.objects.get(id=post_id)
            user = request.user

            bookmark, created = Bookmark.objects.get_or_create(user=user, post=post)

            if created:
                return Response({'status': 'success', 'message': 'Post bookmarked.'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'status': 'warning', 'message': 'Post already bookmarked.'}, status=status.HTTP_400_BAD_REQUEST)
        except BlogPost.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

class RemoveBookmarkView(APIView):
    def delete(self, request, post_id):
        try:
            post = BlogPost.objects.get(id=post_id)
            user = request.user

            bookmark = Bookmark.objects.get(user=user, post=post)
            bookmark.delete()

            return Response({'status': 'success', 'message': 'Bookmark removed.'}, status=status.HTTP_204_NO_CONTENT)
        except BlogPost.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
        except Bookmark.DoesNotExist:
            return Response({'error': 'Bookmark not found'}, status=status.HTTP_404_NOT_FOUND)

class UserBookmarksView(ListAPIView):
    serializer_class = BlogPostSerializer

    def get_queryset(self):
        user = self.request.user
        return BlogPost.objects.filter(bookmark__user=user)

class SubscriptionCreateView(generics.CreateAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

class SubscriptionListView(generics.ListAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user)

class BlogPostUpdateView(UpdateAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        blog_post = super().get_object()
        if blog_post.author != self.request.user:
            raise PermissionDenied("You are not allowed to edit this post.")
        return blog_post

class BlogPostDeleteView(DestroyAPIView):
    queryset = BlogPost.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        blog_post = super().get_object()
        if blog_post.author != self.request.user:
            raise PermissionDenied("You are not allowed to delete this post.")
        return blog_post

class BlogPostListView(APIView):
    def get(self, request):
        published_or_no_status_posts = BlogPost.objects.filter(
            status='published'
        ).union(BlogPost.objects.filter(status__isnull=True))

        serializer = BlogPostSerializer(published_or_no_status_posts, many=True)
        return Response(serializer.data)

class BlogPostDetailView(RetrieveAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer

    def get_object(self):
        post_id = self.kwargs.get('id')
        post = get_object_or_404(BlogPost, id=post_id)
        return post

class UserBlogPostListView(ListAPIView):
    serializer_class = BlogPostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return BlogPost.objects.filter(author=self.request.user)

class CommentFlagView(APIView):
    def post(self, request, comment_id):
        try:
            comment = Comment.objects.get(id=comment_id)
            comment.is_flagged = True
            comment.save()
            return Response({"detail": "Comment flagged successfully."}, status=status.HTTP_200_OK)
        except Comment.DoesNotExist:
            return Response({"detail": "Comment not found."}, status=status.HTTP_404_NOT_FOUND)

class CommentModerateView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        flagged_comments = Comment.objects.filter(is_flagged=True)
        serializer = CommentSerializer(flagged_comments, many=True)
        return Response(serializer.data)

    def put(self, request, comment_id):
        try:
            comment = Comment.objects.get(id=comment_id)
            action = request.data.get('action')  # 'approve' or 'reject'

            if action == 'approve':
                comment.is_flagged = False
                comment.save()
                return Response({"detail": "Comment approved."}, status=status.HTTP_200_OK)
            elif action == 'reject':
                comment.delete()
                return Response({"detail": "Comment deleted."}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"detail": "Invalid action."}, status=status.HTTP_400_BAD_REQUEST)
        except Comment.DoesNotExist:
            return Response({"detail": "Comment not found."}, status=status.HTTP_404_NOT_FOUND)

class FlaggedCommentListView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        flagged_comments = Comment.objects.filter(is_flagged=True)
        serializer = CommentSerializer(flagged_comments, many=True)
        return Response(serializer.data)

class AnalyticsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        total_users = UserAccount.objects.count()
        total_comments = Comment.objects.count()
        most_popular_posts = BlogPost.objects.annotate(comment_count=Count('comments')).order_by('-comment_count')[:5]  # Top 5 posts by comments

        # Preparing response data
        analytics_data = {
            'total_users': total_users,
            'total_comments': total_comments,
            'most_popular_posts': [
                {
                    'title': post.title,
                    'comment_count': post.comment_count,
                } for post in most_popular_posts
            ],
        }

        return Response(analytics_data, status=200)

class UserActivityReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        activity_logs = ActivityLog.objects.filter(user=user).order_by('-timestamp')
        
        activity_data = {}
        for log in activity_logs:
            if log.post.title not in activity_data:
                activity_data[log.post.title] = {
                    'views': 0,
                    'likes': 0,
                    'comments': 0,
                }
            if log.action == 'viewed':
                activity_data[log.post.title]['views'] += 1
            elif log.action == 'liked':
                activity_data[log.post.title]['likes'] += 1
            elif log.action == 'commented':
                activity_data[log.post.title]['comments'] += 1

        return Response(activity_data, status=200)