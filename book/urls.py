from django.urls import path
from .views import *

urlpatterns = [
    path('books/', BookListView.as_view(), name='book_list'),
    path('books/create/', BookCreateView.as_view(), name='book_create'),
    path('books/<int:id>/', BookDetailView.as_view(), name='book_detail'),
    path('books/update/<int:id>/', BookUpdateView.as_view(), name='book_update'),
    path('books/delete/<int:id>/', BookDeleteView.as_view(), name='book_delete'),

    path('authors/', AuthorListView.as_view(), name='author_list'),
    path('authors/create/', AuthorCreateView.as_view(), name='author_create'),

    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('categories/create/', CategoryCreateView.as_view(), name='category_create'),
]
