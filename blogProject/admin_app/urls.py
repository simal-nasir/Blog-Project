from django.urls import path
from .views import *

urlpatterns = [
    path('categories/create/', CategoryCreateView.as_view(), name='create-category'),
    path('categories/', CategoryListView.as_view(), name='list-categories'),
    path('categories/<int:category_id>/delete/', CategoryDeleteView.as_view(), name='category-delete'),  # Add this line
    path('users/', AdminUserListView.as_view(), name='admin-user-list'),
    path('users/<int:id>/delete/', AdminUserDeleteView.as_view(), name='delete-admin-user'),
    path('post/<int:post_id>/edit/', BlogPostEditView.as_view(), name='blogpost-edit'),
    path('post/<int:post_id>/delete/', BlogPostDeleteView.as_view(), name='blogpost-delete'),
    path('export/csv/', ExportCSVView.as_view(), name='export_csv'),
    path('export/excel/', ExportExcelView.as_view(), name='export_excel'),
    path('posts/scheduled/create/', BlogPostScheduleCreateView.as_view(), name='scheduled-post-create'),
    path('publish-scheduled-posts/', PublishScheduledPostsView.as_view(), name='publish-scheduled-posts'),
    path('drafts/', DraftListView.as_view(), name='draft-list'),
    path('drafts/<int:pk>/', DraftDetailView.as_view(), name='draft-detail'),
    path('dashboard/', AdminDashboardView.as_view(), name='admin-dashboard'),
    path('pending-posts/', PendingPostsListView.as_view(), name='pending-posts'),
    path('posts/<int:pk>/approve/', ApprovePostView.as_view(), name='approve-post'),
]