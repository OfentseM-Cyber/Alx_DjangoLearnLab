"""
Custom filters for the API application.

This module defines filter sets for implementing advanced
filtering, searching, and ordering capabilities.
"""

import django_filters
from .models import Book


class BookFilter(django_filters.FilterSet):
    """
    Filter set for Book model providing advanced filtering capabilities.
    
    Allows filtering by:
    - title (case-insensitive contains)
    - author name (case-insensitive contains) 
    - publication_year (exact match)
    - publication_year range (gte, lte)
    """
    
    title = django_filters.CharFilter(lookup_expr='icontains')
    author__name = django_filters.CharFilter(lookup_expr='icontains')
    publication_year = django_filters.NumberFilter()
    publication_year__gte = django_filters.NumberFilter(field_name='publication_year', lookup_expr='gte')
    publication_year__lte = django_filters.NumberFilter(field_name='publication_year', lookup_expr='lte')
    
    class Meta:
        model = Book
        fields = ['title', 'author__name', 'publication_year']
