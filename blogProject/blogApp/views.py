from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView, CreateAPIView,DestroyAPIView,UpdateAPIView,RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
import re
from .models import *
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
        serializer.save(author=self.request.user, post=post)

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
            return Response({'status': 'success', 'likes': post.likes.count()}, status=status.HTTP_200_OK)
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

            return Response({'status': 'success', 'dislikes': post.dislikes.count()}, status=status.HTTP_200_OK)
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