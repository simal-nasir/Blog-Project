from django.shortcuts import render
from rest_framework import generics, permissions
from accounts.models import UserAccount
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from blogApp.models import Profile
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import UserAccount
from accounts.serializers import UserAccountSerializer

class UserRoleUpdateView(APIView):
    permission_classes = [IsAdminUser]
    def put(self, request, pk):
        try:
            user = UserAccount.objects.get(pk=pk)

            profile, created = Profile.objects.get_or_create(user=user)

            role = request.data.get('role')
            if role in ['author', 'editor', 'moderator']:
                profile.role = role
                profile.save()

                return Response({'message': f'Role {role} assigned to {user.email}'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid role specified'}, status=status.HTTP_400_BAD_REQUEST)

        except UserAccount.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


class UserListByRoleView(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        role = self.request.query_params.get('role', None)
        if role:
            return UserAccount.objects.filter(role=role)
        return UserAccount.objects.all()



class UserBanUnbanView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def patch(self, request, user_id):
        try:
            user = UserAccount.objects.get(id=user_id)
        except UserAccount.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        # Get the action from the request data
        action = request.data.get("action")  # Expecting 'ban' or 'unban'

        if action == "ban":
            user.is_banned = True
            user.save()
            return Response({"message": f"User {user.email} has been banned."}, status=status.HTTP_200_OK)

        elif action == "unban":
            user.is_banned = False
            user.save()
            return Response({"message": f"User {user.email} has been unbanned."}, status=status.HTTP_200_OK)

        return Response({"error": "Invalid action."}, status=status.HTTP_400_BAD_REQUEST)
    
class UserListView(generics.ListAPIView):
    queryset = UserAccount.objects.all()
    serializer_class = UserAccountSerializer
    permission_classes = [IsAuthenticated] 

class CurrentUserView(APIView):
    
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user  
        user_data = {
            "id": user.id,
            "email": user.email,
            "name": user.name,
        }
        return Response(user_data, status=status.HTTP_200_OK)