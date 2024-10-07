from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from blogApp.models import Category
from blogApp.serializers import CategorySerializer

class CategoryCreateView(APIView):
    permission_classes = [IsAdminUser]  # Only allow superuser to access this view

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer