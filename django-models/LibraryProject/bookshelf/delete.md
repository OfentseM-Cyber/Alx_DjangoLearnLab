```python
from bookshelf.models import Book
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()
print("Book deleted successfully")
print("All books:", Book.objects.all())
```
Expected output:
```
Book deleted successfully
All books: <QuerySet []>
```
