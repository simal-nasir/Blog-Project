from rest_framework import serializers
from .models import Profile
from django.contrib.auth import get_user_model

User = get_user_model()

class ProfileSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='user.name', read_only=True)  # Include the user's name

    class Meta:
        model = Profile
        fields = ['id', 'name', 'bio', 'profile_picture']  # Add 'name' to the fields