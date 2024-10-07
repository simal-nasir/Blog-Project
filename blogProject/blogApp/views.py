from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView, CreateAPIView
from django.views.decorators.csrf import csrf_exempt
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
        category_name = self.kwargs['category']  # Expecting category name
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
        tag_name = self.kwargs['tag']  # Expecting tag name
        return BlogPost.objects.filter(tags__name=tag_name)

class TagListView(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer