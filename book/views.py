from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions
from .serializers import *
from .models import *

class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['author', 'category']

class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'id'


class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookPostSerializer
    permission_classes = [permissions.IsAdminUser]


class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookPostSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = 'id'


class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookPostSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = 'id'


class AuthorListView(generics.ListAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAdminUser]

class AuthorCreateView(generics.CreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAdminUser]


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]

class CategoryCreateView(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]

