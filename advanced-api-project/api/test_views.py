"""
Unit tests for Django REST Framework API endpoints.
"""

from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Author, Book


class BookAPITestCase(TestCase):
    
    def setUp(self):
        self.client = APIClient()
        
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        
        self.author1 = Author.objects.create(name='J.K. Rowling')
        self.author2 = Author.objects.create(name='J.R.R. Tolkien')
        
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
    
    def test_list_books_authenticated(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get('/api/books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_book_authenticated(self):
        self.client.login(username='testuser', password='testpassword123')
        data = {
            'title': 'New Test Book',
            'publication_year': 2023,
            'author': self.author1.id
        }
        response = self.client.post('/api/books/create/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_update_book_authenticated(self):
        self.client.login(username='testuser', password='testpassword123')
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
    
    def test_delete_book_authenticated(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.delete(f'/api/books/delete/{self.book1.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_filter_books_by_title(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get('/api/books/?title=harry')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_search_books(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get('/api/books/?search=potter')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_order_books_by_title(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get('/api/books/?ordering=title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class AuthorAPITestCase(TestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword123'
        )
        self.author = Author.objects.create(name='Test Author')
    
    def test_create_author_authenticated(self):
        self.client.login(username='testuser', password='testpassword123')
        data = {'name': 'New Test Author'}
        response = self.client.post('/api/authors/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ValidationTestCase(TestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword123'
        )
        self.author = Author.objects.create(name='Test Author')
    
    def test_create_book_with_future_publication_year(self):
        self.client.login(username='testuser', password='testpassword123')
        from datetime import datetime
        future_year = datetime.now().year + 1
        data = {
            'title': 'Future Book',
            'publication_year': future_year,
            'author': self.author.id
        }
        response = self.client.post('/api/books/create/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_multiple_login_attempts(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get('/api/books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.client.logout()
        
        self.client.login(username='testuser', password='testpassword123')
        data = {'name': 'Another Author'}
        response = self.client.post('/api/authors/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
