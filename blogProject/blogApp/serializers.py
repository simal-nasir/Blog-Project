from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model

User = get_user_model()

class ProfileSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='user.name', read_only=True)

    class Meta:
        model = Profile
        fields = ['id', 'name', 'bio', 'profile_picture']


class BlogPostSerializer(serializers.ModelSerializer):
    category = serializers.CharField()
    image = serializers.ImageField(required=False, allow_null=True)
    tags = serializers.CharField(required=False)

    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'content', 'author', 'category', 'image', 'tags']
        read_only_fields = ['author']

    def create(self, validated_data):

        category_name = validated_data.pop('category')
        category, created = Category.objects.get_or_create(name=category_name)

        tags_string = validated_data.pop('tags', '')
        tag_names = tags_string.split()

        blog_post = BlogPost.objects.create(category=category, **validated_data)

        for tag_name in tag_names:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            blog_post.tags.add(tag)

        blog_post.save()
        return blog_post

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']