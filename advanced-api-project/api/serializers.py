"""
Custom serializers for the API application.

This module defines serializers that handle complex data structures
and nested relationships between Author and Book models.
"""

from rest_framework import serializers
from .models import Author, Book
from datetime import datetime


class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model.
    
    This serializer handles all fields of the Book model and includes
    custom validation for the publication_year field to ensure it's not in the future.
    """
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']
        read_only_fields = ['id']
    
    def validate_publication_year(self, value):
        """
        Custom validation for publication_year field.
        
        Args:
            value (int): The publication year to validate
            
        Returns:
            int: The validated publication year
            
        Raises:
            serializers.ValidationError: If the publication year is in the future
        """
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError(
                f"Publication year cannot be in the future. Current year is {current_year}."
            )
        return value


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Author model with nested book relationships.
    
    This serializer includes the author's name and dynamically serializes
    all related books using the BookSerializer. The nested relationship
    allows for comprehensive author data including their published works.
    """
    
    # Nested serializer for related books
    # Using BookSerializer to handle the one-to-many relationship
    # read_only=True ensures nested books are only included in output, not input
    books = BookSerializer(many=True, read_only=True)
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'books']
        read_only_fields = ['id']


class AuthorDetailSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for Author model with additional nested book information.
    
    This demonstrates an alternative approach to handling nested relationships
    where we might want different levels of detail in different contexts.
    """
    
    books = BookSerializer(many=True, read_only=True)
    books_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'books', 'books_count']
        read_only_fields = ['id']
    
    def get_books_count(self, obj):
        """Method to get the count of books by this author."""
        return obj.books.count()
