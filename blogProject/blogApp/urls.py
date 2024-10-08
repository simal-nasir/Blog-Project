from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('profile/', ProfileRetrieveUpdateView.as_view(), name='profile'),
    path('posts/create/', BlogPostCreateView.as_view(), name='create-post'), 
    path('posts/category/<str:category>/', BlogPostByCategoryView.as_view(), name='posts-by-category'),
    path('posts/author/<int:author_id>/', BlogPostByAuthorView.as_view(), name='posts-by-author'),
    path('posts/tag/<str:tag>/', BlogPostByTagView.as_view(), name='posts-by-tag'),
    path('tags/', TagListView.as_view(), name='tag-list'),
    path('posts/search/', BlogPostSearchView.as_view(), name='posts-search'),
    path('posts/<int:post_id>/comments/', CommentListView.as_view(), name='post-comments'),
    path('posts/<int:post_id>/comments/create/', CommentCreateView.as_view(), name='create-comment'),
    path('posts/<int:post_id>/like/', ToggleLikeView.as_view(), name='like-post'),
    path('posts/<int:post_id>/dislike/', ToggleDislikeView.as_view(), name='dislike-post'),
    path('posts/<int:post_id>/bookmark/', BookmarkPostView.as_view(), name='bookmark-post'),
    path('posts/<int:post_id>/remove-bookmark/', RemoveBookmarkView.as_view(), name='remove-bookmark'),
    path('user/bookmarks/', UserBookmarksView.as_view(), name='user-bookmarks'),
    path('subscriptions/', SubscriptionListView.as_view(), name='subscription-list'),
    path('subscriptions/create/', SubscriptionCreateView.as_view(), name='subscription-create'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)