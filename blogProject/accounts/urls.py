from django.urls import path
from .views import *

urlpatterns = [
    path('users/<int:pk>/role/', UserRoleUpdateView.as_view(), name='user-role-update'),  
    path('users/roles/', UserListByRoleView.as_view(), name='users-by-role'),
    path('users/<int:user_id>/ban/', UserBanUnbanView.as_view(), name='ban-unban-user'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('auth/user/', CurrentUserView.as_view(), name='current_user'),

]