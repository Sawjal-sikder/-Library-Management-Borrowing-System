from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from django.utils import timezone
from django.db import transaction
from datetime import timedelta
from .serializers import *
from .models import *
from django.contrib.auth import get_user_model

User = get_user_model()

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


class BorrowCreateView(generics.CreateAPIView):
    serializer_class = BorrowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user
        book_id = request.data.get("book_id")

        if not book_id:
            return Response({"error": "book_id is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response({"error": "Book not found."}, status=status.HTTP_404_NOT_FOUND)

        active_borrows = Borrow.objects.filter(user=user, return_date__isnull=True).count()
        if active_borrows >= 3:
            return Response({"error": "Borrowing limit exceeded. You can borrow up to 3 books at a time."},
                            status=status.HTTP_400_BAD_REQUEST)

        if book.available_copies <= 0:
            return Response({"error": f"'{book.title}' is not available right now."},
                            status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            book.available_copies -= 1
            book.save()

            borrow_date = timezone.now().date()
            due_date = borrow_date + timedelta(days=14)

            borrow = Borrow.objects.create(
                user=user,
                book=book,
                borrow_date=borrow_date,
                due_date=due_date
            )

        borrow_data = self.get_serializer(borrow).data
        return Response(
            {
                "message": f"You have successfully borrowed '{book.title}'. Return by {due_date}.",
                "borrow": borrow_data
            },
            status=status.HTTP_201_CREATED
        )
    
class BorrowListView(generics.ListAPIView):
    serializer_class = BorrowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Borrow.objects.filter(user=user, return_date__isnull=True)


class ReturnBookView(generics.UpdateAPIView):
    queryset = Borrow.objects.all()
    serializer_class = BorrowReturnSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['post']  

    def post(self, request, *args, **kwargs):
        borrow_id = request.data.get('borrow_id')
        user = request.user

        if not borrow_id:
            return Response({"error": "borrow_id is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            borrow = Borrow.objects.select_related('book', 'user').get(id=borrow_id, user=user)
        except Borrow.DoesNotExist:
            return Response({"error": "Borrow record not found."}, status=status.HTTP_404_NOT_FOUND)

        if borrow.return_date is not None:
            return Response({"error": "This book has already been returned."}, status=status.HTTP_400_BAD_REQUEST)

        today = timezone.now().date()

        with transaction.atomic():
            borrow.return_date = today
            borrow.save()

            book = borrow.book
            book.available_copies += 1
            book.save()

            days_late = (today - borrow.due_date).days
            if days_late > 0:
                user.penalty_points = (user.penalty_points or 0) + days_late
                user.save()

        return Response({
            "message": f"Book '{book.title}' returned successfully.",
            "days_late": max(days_late, 0),
            "penalty_points_added": days_late if days_late > 0 else 0,
            "total_penalty_points": user.penalty_points
        }, status=status.HTTP_200_OK)
    
class UserPenaltyPointsView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAdminUser]
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        penalty_points = getattr(user, 'penalty_points', 0) or 0
        return Response({
            "user_id": user.id,
            "penalty_points": penalty_points
        }, status=status.HTTP_200_OK)