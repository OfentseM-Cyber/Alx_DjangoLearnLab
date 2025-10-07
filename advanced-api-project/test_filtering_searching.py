"""
Test script for filtering, searching, and ordering functionality.
"""

import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'advanced_api_project.settings')
django.setup()

from rest_framework.test import APIClient
from api.models import Author, Book

def test_filtering_searching_ordering():
    """Test filtering, searching, and ordering capabilities."""
    print("Testing filtering, searching, and ordering...")
    
    # Create test data
    author1 = Author.objects.create(name="J.K. Rowling")
    author2 = Author.objects.create(name="J.R.R. Tolkien")
    
    Book.objects.create(title="Harry Potter and the Philosopher's Stone", publication_year=1997, author=author1)
    Book.objects.create(title="Harry Potter and the Chamber of Secrets", publication_year=1998, author=author1)
    Book.objects.create(title="The Hobbit", publication_year=1937, author=author2)
    Book.objects.create(title="The Lord of the Rings", publication_year=1954, author=author2)
    Book.objects.create(title="Fantastic Beasts", publication_year=2001, author=author1)
    
    client = APIClient()
    
    # Test basic listing
    print("\n1. Testing basic book list...")
    response = client.get('/api/books/')
    print(f"Total books: {len(response.data)}")
    
    # Test filtering by title
    print("\n2. Testing title filtering...")
    response = client.get('/api/books/?title=harry')
    print(f"Books with 'harry' in title: {len(response.data)}")
    
    # Test filtering by author
    print("\n3. Testing author filtering...")
    response = client.get('/api/books/?author__name=tolkien')
    print(f"Books by Tolkien: {len(response.data)}")
    
    # Test filtering by publication year
    print("\n4. Testing year filtering...")
    response = client.get('/api/books/?publication_year=1997')
    print(f"Books published in 1997: {len(response.data)}")
    
    # Test year range filtering
    print("\n5. Testing year range filtering...")
    response = client.get('/api/books/?publication_year__gte=1990&publication_year__lte=2000')
    print(f"Books published between 1990-2000: {len(response.data)}")
    
    # Test search functionality
    print("\n6. Testing search functionality...")
    response = client.get('/api/books/?search=potter')
    print(f"Books found with search 'potter': {len(response.data)}")
    
    # Test ordering
    print("\n7. Testing ordering...")
    response = client.get('/api/books/?ordering=title')
    titles_asc = [book['title'] for book in response.data]
    print(f"First book (ascending): {titles_asc[0] if titles_asc else 'None'}")
    
    response = client.get('/api/books/?ordering=-title')
    titles_desc = [book['title'] for book in response.data]
    print(f"First book (descending): {titles_desc[0] if titles_desc else 'None'}")
    
    # Test author search
    print("\n8. Testing author search...")
    response = client.get('/api/authors/?search=rowling')
    print(f"Authors found with search 'rowling': {len(response.data)}")
    
    print("\nFiltering, searching, and ordering test completed!")

if __name__ == "__main__":
    test_filtering_searching_ordering()
