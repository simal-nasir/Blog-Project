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
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)