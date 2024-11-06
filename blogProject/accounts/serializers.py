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
        fields = ['id', 'email', 'name', 'role', 'is_active','is_superuser']
        read_only_fields = ['email', 'is_active']

    def update(self, instance, validated_data):

        if 'role' in validated_data and not self.context['request'].user.is_superuser:
            raise serializers.ValidationError("Only superusers can assign roles.")

        if 'role' in validated_data:
            instance.role = validated_data['role']

        instance.save()
        return instance

from rest_framework import serializers
from .models import UserAccount

class UserAccountSerializer(serializers.ModelSerializer):
    is_superuser = serializers.BooleanField(source='is_superuser', read_only=True)

    class Meta:
        model = UserAccount
        fields = ['id', 'email', 'name', 'role', 'is_superuser', 'is_active', 'is_staff', 'is_banned', 'created_at']

from djoser.serializers import UserSerializer as BaseUserSerializer

class CustomUserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = BaseUserSerializer.Meta.fields + ('is_superuser',)