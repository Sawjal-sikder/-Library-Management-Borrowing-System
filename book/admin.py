from django.contrib import admin
from .models import *

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'available_copies')
    search_fields = ('title', 'author__name', 'category__name')
    list_filter = ('category',)
    ordering = ('title',)
    list_per_page = 10
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)
@admin.register(Borrow)
class BorrowAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'borrow_date', 'due_date', 'return_date')
    search_fields = ('user__email', 'book__title')
    list_filter = ('borrow_date', 'due_date', 'return_date')
    ordering = ('-borrow_date',)