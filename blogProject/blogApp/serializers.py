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
    category = serializers.CharField()  # Expecting category name
    image = serializers.ImageField(required=False, allow_null=True)
    tags = serializers.CharField(required=False)  # Expecting tags as a string
    status = serializers.CharField(default='draft')  # Adding status to handle drafts

    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'content', 'author', 'category', 'image', 'tags', 'status']
        read_only_fields = ['author']

    def create(self, validated_data):
        # Handle category
        category_name = validated_data.pop('category')
        category, created = Category.objects.get_or_create(name=category_name)

        # Handle tags
        tags_string = validated_data.pop('tags', '')  # Get tags string if provided
        tag_names = tags_string.split()  # Split the string into a list of tag names

        # Create the blog post with the draft/published status
        blog_post = BlogPost.objects.create(category=category, **validated_data)

        # Associate tags with the blog post
        for tag_name in tag_names:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            blog_post.tags.add(tag)

        blog_post.save()
        return blog_post

    def update(self, instance, validated_data):
        # Handle category update
        category_name = validated_data.pop('category', None)
        if category_name:
            category, created = Category.objects.get_or_create(name=category_name)
            instance.category = category

        # Handle tags update
        tags_string = validated_data.pop('tags', '')
        if tags_string:
            tag_names = tags_string.split()
            instance.tags.clear()  # Clear existing tags before adding new ones
            for tag_name in tag_names:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                instance.tags.add(tag)

        # Update other fields, including the status (draft/published)
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.image = validated_data.get('image', instance.image)
        instance.status = validated_data.get('status', instance.status)

        instance.save()
        return instance

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content', 'post', 'author', 'parent', 'created_at']
        read_only_fields = ['post', 'author', 'created_at']

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['id', 'user', 'category', 'tag', 'author']
        read_only_fields = ['user']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)