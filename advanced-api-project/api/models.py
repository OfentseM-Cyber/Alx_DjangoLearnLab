from django.db import models

# Create your models here.
"""
Data models for the API application.

This module defines the Author and Book models which represent
the core data structure of our library management system.
"""

from django.db import models


class Author(models.Model):
    """
    Author model representing a book author.
    
    Attributes:
        name (CharField): The name of the author (max 100 characters)
    """
    name = models.CharField(max_length=100)
    
    def __str__(self):
        """String representation of the Author model."""
        return self.name
    
    class Meta:
        """Meta options for the Author model."""
        verbose_name = "Author"
        verbose_name_plural = "Authors"


class Book(models.Model):
    """
    Book model representing a published book.
    
    Attributes:
        title (CharField): The title of the book (max 200 characters)
        publication_year (IntegerField): The year the book was published
        author (ForeignKey): Reference to the Author model, establishing
                            a one-to-many relationship (one author can have many books)
    """
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    author = models.ForeignKey(
        Author, 
        on_delete=models.CASCADE,  # If author is deleted, their books are also deleted
        related_name='books'  # Enables reverse relation: author.books.all()
    )
    
    def __str__(self):
        """String representation of the Book model."""
        return f"{self.title} by {self.author.name}"
    
    class Meta:
        """Meta options for the Book model."""
        verbose_name = "Book"
        verbose_name_plural = "Books"
        ordering = ['-publication_year', 'title']  # Default ordering by year (descending)
