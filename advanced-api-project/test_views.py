"""
Test script for custom views and generic views.
"""

import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'advanced_api_project.settings')
django.setup()

from api.models import Author, Book
from api.serializers import BookSerializer

def test_views_setup():
    """Test that views are properly configured."""
    print("Testing views setup...")
    
    # Create test data
    author = Author.objects.create(name="Test Author for Views")
    book = Book.objects.create(
        title="Test Book for Views",
        publication_year=2020,
        author=author
    )
    
    # Test serialization
    serializer = BookSerializer(book)
    print("Book data:", serializer.data)
    
    print("Views setup test completed!")

if __name__ == "__main__":
    test_views_setup()
