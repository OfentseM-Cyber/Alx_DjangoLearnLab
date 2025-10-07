# Django Blog Project - ALX Learning Lab

A simple Django blog application with Post model, admin interface, and basic templates.

## Features
- Post model with title, content, author, and published date
- Django admin interface for managing posts
- Basic templates for home page
- Static files setup

## Project Structure# Django Blog Project

django_blog/
├── manage.py
├── django_blog/ # Project settings
│ ├── settings.py
│ ├── urls.py
│ └── ...
├── blog/ # Blog app
│ ├── models.py
│ ├── views.py
│ ├── templates/
│ └── static/
├── requirements.txt
├── db.sqlite3
└── README.md


## Setup
1. Clone the repository
2. Install requirements: `pip install -r requirements.txt`
3. Run migrations: `python manage.py migrate`
4. Create superuser: `python manage.py createsuperuser`
5. Run server: `python manage.py runserver`

## URLs
- Home: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/
