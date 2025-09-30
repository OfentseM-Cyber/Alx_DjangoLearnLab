from django.shortcuts import render

# Create your views here.
"""
API views for handling Author and Book models.
"""

from rest_framework import generics
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer, AuthorDetailSerializer


class AuthorListCreateView(generics.ListCreateAPIView):
    """API view for listing and creating authors."""
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class AuthorDetailView(generics.RetrieveUpdateDestroyAPIView):
    """API view for retrieving, updating, and deleting individual authors."""
    queryset = Author.objects.all()
    serializer_class = AuthorDetailSerializer


class BookListCreateView(generics.ListCreateAPIView):
    """API view for listing and creating books."""
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    """API view for retrieving, updating, and deleting individual books."""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
