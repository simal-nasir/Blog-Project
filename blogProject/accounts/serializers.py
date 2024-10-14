from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import UserAccount

User = get_user_model()

class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'name', 'password')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ['id', 'email', 'name', 'role', 'is_active']
        read_only_fields = ['email', 'is_active']

    def update(self, instance, validated_data):

        if 'role' in validated_data and not self.context['request'].user.is_superuser:
            raise serializers.ValidationError("Only superusers can assign roles.")

        if 'role' in validated_data:
            instance.role = validated_data['role']

        instance.save()
        return instance

class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ['id', 'email', 'name', 'role', 'is_active', 'is_staff']  # Include the fields you want to serialize