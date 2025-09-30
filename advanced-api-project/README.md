# Advanced API Project

A Django REST Framework project with custom serializers handling complex data structures and nested relationships.

## Project Structure
## Custom Views and Generic Views

This project implements Django REST Framework's generic views for efficient CRUD operations:

### Book Views

- **BookListView** (`GET /api/books/`) - List all books (public access)
- **BookDetailView** (`GET /api/books/<id>/`) - Get specific book details (public access)
- **BookCreateView** (`POST /api/books/create/`) - Create new book (authenticated users only)
- **BookUpdateView** (`PUT/PATCH /api/books/<id>/update/`) - Update book (authenticated users only)
- **BookDeleteView** (`DELETE /api/books/<id>/delete/`) - Delete book (authenticated users only)

### Author Views

- **AuthorListCreateView** (`GET/POST /api/authors/`) - List all authors or create new author
- **AuthorDetailView** (`GET/PUT/PATCH/DELETE /api/authors/<id>/`) - Detailed author operations

### Permissions

- Read operations (GET) are available to all users
- Write operations (POST, PUT, PATCH, DELETE) require authentication
- Custom permission methods apply different rules based on HTTP methods

### Testing

Use tools like Postman or curl to test endpoints:
```bash
# Get all books
curl http://127.0.0.1:8000/api/books/

# Create a book (requires authentication)
curl -X POST http://127.0.0.1:8000/api/books/create/ \
  -H "Content-Type: application/json" \
  -d '{"title":"New Book", "publication_year": 2023, "author": 1}'
