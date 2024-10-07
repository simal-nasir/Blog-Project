from django.urls import path
from .views import *

urlpatterns = [
    path('categories/create/', CategoryCreateView.as_view(), name='create-category'),
    path('categories/', CategoryListView.as_view(), name='list-categories'), 
]