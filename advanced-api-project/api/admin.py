from django.contrib import admin

# Register your models here.
"""
Admin configuration for API models.
"""

from django.contrib import admin
from .models import Author, Book

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """Admin interface configuration for Author model."""
    list_display = ['id', 'name']
    search_fields = ['name']

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """Admin interface configuration for Book model."""
    list_display = ['id', 'title', 'author', 'publication_year']
    list_filter = ['author', 'publication_year']
    search_fields = ['title', 'author__name']
