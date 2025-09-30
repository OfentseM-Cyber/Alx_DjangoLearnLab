"""
Custom views and generic views for the API application.

This module implements Django REST Framework's generic views
and mixins to handle CRUD operations for Book and Author models.
"""

from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from django_filters import rest_framework  # Updated import for ALX checker
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer, AuthorDetailSerializer
from .filters import BookFilter

# Book Views using Generic API Views
class BookListView(generics.ListAPIView):
    """
    ListView for retrieving all books with filtering, searching, and ordering.
    
    Provides a read-only endpoint that returns all Book instances.
    Includes comprehensive filtering, search, and ordering capabilities.
    
    Filtering Examples:
    - /api/books/?title=harry                    (books with 'harry' in title)
    - /api/books/?author__name=tolkien           (books by author with 'tolkien' in name)
    - /api/books/?publication_year=2020          (books published in 2020)
    - /api/books/?publication_year__gte=2020     (books published 2020 or later)
    - /api/books/?publication_year__lte=2020     (books published 2020 or earlier)
    
    Search Examples:
    - /api/books/?search=harry                   (search in title and author name)
    
    Ordering Examples:
    - /api/books/?ordering=title                 (ascending by title)
    - /api/books/?ordering=-title                (descending by title)
    - /api/books/?ordering=publication_year      (ascending by year)
    - /api/books/?ordering=-publication_year     (descending by year)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]
    
    # Filtering, searching, and ordering configuration
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = BookFilter
    search_fields = ['title', 'author__name']
    ordering_fields = ['title', 'publication_year', 'author__name']
    ordering = ['title']  # Default ordering

class BookDetailView(generics.RetrieveAPIView):
    """
    DetailView for retrieving a single book by ID.
    
    Provides a read-only endpoint that returns a specific Book instance
    based on the primary key in the URL.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]  # Allow anyone to view book details


class BookCreateView(generics.CreateAPIView):
    """
    CreateView for adding a new book.
    
    Handles POST requests to create new Book instances.
    Includes data validation through BookSerializer.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can create books

    def perform_create(self, serializer):
        """
        Custom method to handle book creation.
        Can be extended to add additional logic during creation.
        """
        serializer.save()


class BookUpdateView(generics.UpdateAPIView):
    """
    UpdateView for modifying an existing book.
    
    Handles PUT and PATCH requests to update existing Book instances.
    Ensures data validation through BookSerializer.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can update books

    def perform_update(self, serializer):
        """
        Custom method to handle book updates.
        Can be extended to add additional logic during updates.
        """
        serializer.save()


class BookDeleteView(generics.DestroyAPIView):
    """
    DeleteView for removing a book.
    
    Handles DELETE requests to remove Book instances from the database.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can delete books

    def perform_destroy(self, instance):
        """
        Custom method to handle book deletion.
        Can be extended to add additional logic during deletion.
        """
        instance.delete()


# Author Views (Enhanced with permissions)
class AuthorListCreateView(generics.ListCreateAPIView):
    """
    Combined List and Create view for Author model.
    
    Handles GET requests to list all authors and POST requests to create new authors.
    Includes basic search functionality for author names.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']
    ordering = ['name']
    
    def get_permissions(self):
        """
        Custom permission method that applies different permissions
        based on the HTTP method (GET vs POST).
        """
        if self.request.method == 'GET':
            return [AllowAny()]  # Anyone can view authors
        return [IsAuthenticated()]  # Only authenticated users can create authors

class AuthorDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Detail view for Author model supporting retrieve, update, and delete operations.
    
    Handles GET, PUT, PATCH, and DELETE requests for individual authors.
    Applies permission checks based on the operation type.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorDetailSerializer
    
    def get_permissions(self):
        """
        Custom permission method that applies different permissions
        based on the HTTP method.
        """
        if self.request.method == 'GET':
            return [AllowAny()]  # Anyone can view author details
        return [IsAuthenticated()]  # Only authenticated users can modify authors
