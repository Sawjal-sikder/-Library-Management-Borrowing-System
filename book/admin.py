from django.contrib import admin
from .models import *

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'author', 'category', 'available_copies')
    
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name',)
   
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
   
@admin.register(Borrow)
class BorrowAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'borrow_date', 'due_date', 'return_date')
    