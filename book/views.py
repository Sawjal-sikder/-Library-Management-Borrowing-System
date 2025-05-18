from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status, permissions
from rest_framework.response import Response
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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        book = serializer.save()
        book_data = self.get_serializer(book).data
        return Response(
            {
                "message": f"'{book.title}' has been successfully created.",
                "book": book_data
            },
            status=status.HTTP_201_CREATED
        )


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

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        book_title = instance.title  # or whatever your book title field is
        self.perform_destroy(instance)
        return Response(
            {"message": f"'{book_title}' has been successfully deleted."},
            status=status.HTTP_200_OK
        )


class AuthorListView(generics.ListAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAdminUser]

class AuthorCreateView(generics.CreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAdminUser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        author = serializer.save()
        author_data = self.get_serializer(author).data
        return Response(
            {
                "message": f"'{author.name}' has been successfully created.",
                "author": author_data
            },
            status=status.HTTP_201_CREATED
        )


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]

class CategoryCreateView(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        category = serializer.save()
        category_data = self.get_serializer(category).data
        return Response(
            {
                "message": f"'{category.name}' has been successfully created.",
                "category": category_data
            },
            status=status.HTTP_201_CREATED
        )
