"""
Unit tests for Django REST Framework API endpoints.

This module contains comprehensive tests for Book and Author
API endpoints, including CRUD operations, filtering, searching,
ordering, and permission testing.
"""

from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Author, Book


class BookAPITestCase(TestCase):
    """
    Test case for Book API endpoints.
    
    Tests CRUD operations, filtering, searching, ordering,
    and permission enforcement for Book endpoints.
    """
    
    def setUp(self):
        """
        Set up test data and client for each test method.
        """
        self.client = APIClient()
        
        # Create test users
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        
        self.admin_user = User.objects.create_user(
            username='adminuser',
            email='admin@example.com',
            password='adminpassword123',
            is_staff=True
        )
        
        # Create test authors
        self.author1 = Author.objects.create(name='J.K. Rowling')
        self.author2 = Author.objects.create(name='J.R.R. Tolkien')
        
        # Create test books
        self.book1 = Book.objects.create(
            title='Harry Potter and the Philosopher\'s Stone',
            publication_year=1997,
            author=self.author1
        )
        self.book2 = Book.objects.create(
            title='Harry Potter and the Chamber of Secrets',
            publication_year=1998,
            author=self.author1
        )
        self.book3 = Book.objects.create(
            title='The Hobbit',
            publication_year=1937,
            author=self.author2
        )
        self.book4 = Book.objects.create(
            title='The Lord of the Rings',
            publication_year=1954,
            author=self.author2
        )
    
    def test_list_books_authenticated(self):
        """
        Test that authenticated users can list all books.
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/books/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)
    
    def test_list_books_unauthenticated(self):
        """
        Test that unauthenticated users can list all books.
        """
        response = self.client.get('/api/books/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)
    
    def test_get_book_detail(self):
        """
        Test retrieving a single book by ID.
        """
        response = self.client.get(f'/api/books/{self.book1.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book1.title)
        self.assertEqual(response.data['publication_year'], self.book1.publication_year)
    
    def test_create_book_authenticated(self):
        """
        Test that authenticated users can create books.
        """
        self.client.force_authenticate(user=self.user)
        
        data = {
            'title': 'New Test Book',
            'publication_year': 2023,
            'author': self.author1.id
        }
        
        response = self.client.post('/api/books/create/', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 5)
        self.assertEqual(response.data['title'], 'New Test Book')
    
    def test_create_book_unauthenticated(self):
        """
        Test that unauthenticated users cannot create books.
        """
        data = {
            'title': 'New Test Book',
            'publication_year': 2023,
            'author': self.author1.id
        }
        
        response = self.client.post('/api/books/create/', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Book.objects.count(), 4)
    
    def test_update_book_authenticated(self):
        """
        Test that authenticated users can update books.
        """
        self.client.force_authenticate(user=self.user)
        
        data = {
            'title': 'Updated Book Title',
            'publication_year': 2024,
            'author': self.author1.id
        }
        
        response = self.client.put(
            f'/api/books/update/{self.book1.id}/',
            data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Refresh from database and verify changes
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Updated Book Title')
        self.assertEqual(self.book1.publication_year, 2024)
    
    def test_update_book_unauthenticated(self):
        """
        Test that unauthenticated users cannot update books.
        """
        data = {
            'title': 'Updated Book Title',
            'publication_year': 2024,
            'author': self.author1.id
        }
        
        response = self.client.put(
            f'/api/books/update/{self.book1.id}/',
            data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_delete_book_authenticated(self):
        """
        Test that authenticated users can delete books.
        """
        self.client.force_authenticate(user=self.user)
        
        response = self.client.delete(f'/api/books/delete/{self.book1.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 3)
        self.assertFalse(Book.objects.filter(id=self.book1.id).exists())
    
    def test_delete_book_unauthenticated(self):
        """
        Test that unauthenticated users cannot delete books.
        """
        response = self.client.delete(f'/api/books/delete/{self.book1.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Book.objects.count(), 4)
    
    def test_filter_books_by_title(self):
        """
        Test filtering books by title.
        """
        response = self.client.get('/api/books/?title=harry')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        
        # Verify all returned books contain 'harry' in title (case-insensitive)
        titles = [book['title'].lower() for book in response.data]
        self.assertTrue(all('harry' in title for title in titles))
    
    def test_filter_books_by_author(self):
        """
        Test filtering books by author name.
        """
        response = self.client.get('/api/books/?author__name=tolkien')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_filter_books_by_publication_year(self):
        """
        Test filtering books by publication year.
        """
        response = self.client.get('/api/books/?publication_year=1997')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], self.book1.title)
    
    def test_filter_books_by_year_range(self):
        """
        Test filtering books by publication year range.
        """
        response = self.client.get('/api/books/?publication_year__gte=1990&publication_year__lte=2000')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_search_books(self):
        """
        Test searching books across title and author fields.
        """
        response = self.client.get('/api/books/?search=potter')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_order_books_by_title_ascending(self):
        """
        Test ordering books by title in ascending order.
        """
        response = self.client.get('/api/books/?ordering=title')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book['title'] for book in response.data]
        
        # Check if titles are in ascending order
        self.assertEqual(titles, sorted(titles))
    
    def test_order_books_by_title_descending(self):
        """
        Test ordering books by title in descending order.
        """
        response = self.client.get('/api/books/?ordering=-title')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book['title'] for book in response.data]
        
        # Check if titles are in descending order
        self.assertEqual(titles, sorted(titles, reverse=True))
    
    def test_order_books_by_publication_year(self):
        """
        Test ordering books by publication year.
        """
        response = self.client.get('/api/books/?ordering=publication_year')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book['publication_year'] for book in response.data]
        
        # Check if years are in ascending order
        self.assertEqual(years, sorted(years))


class AuthorAPITestCase(TestCase):
    """
    Test case for Author API endpoints.
    """
    
    def setUp(self):
        """
        Set up test data for author tests.
        """
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword123'
        )
        
        self.author = Author.objects.create(name='Test Author')
    
