from rest_framework import serializers
from .models import *


class BookSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    category = serializers.StringRelatedField()    
    class Meta:
        model = Book
        fields = '__all__'
        read_only_fields = ['available_copies']


class BookPostSerializer(serializers.ModelSerializer):       
    class Meta:
        model = Book
        fields = '__all__'
        

class AuthorSerializer(serializers.ModelSerializer):       
    class Meta:
        model = Author
        fields = '__all__'
        

class CategorySerializer(serializers.ModelSerializer):       
    class Meta:
        model = Category
        fields = '__all__'


class BorrowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrow
        fields = ['id', 'user', 'book', 'borrow_date', 'due_date', 'return_date']
        read_only_fields = ['borrow_date', 'due_date', 'return_date', 'user']

class BorrowcreateSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source='book.title', read_only=True)

    class Meta:
        model = Borrow
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.read_only = True

class BorrowReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrow
        fields = []