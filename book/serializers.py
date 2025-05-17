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
        