from django.urls import reverse
from rest_framework.test import APITestCase

from main.models import Author
from main.models import Book
from main.models import Category
from main.serializers import BookSerializer

BOOKS = [
    {
        "title": "First book",
        "authors": ["First Author", "Second Author"],
        "categories": ["First Category", "Second Category"],
        "published_date": "2001-01-01",
        "average_rating": 2,
        "ratings_count": 1,
        "thumbnail": "http//www.google.pl",
    },
    {
        "title": "Second book",
        "authors": ["Third Author", "Second Author"],
        "categories": ["Third Category", "Second Category"],
        "published_date": "2002-01-01",
        "average_rating": 3,
        "ratings_count": 2,
        "thumbnail": "http//www.google.pl",
    },
    {
        "title": "Third book",
        "authors": ["Fourth Author", "Third Author"],
        "categories": ["Fourth Category", "Second Category"],
        "published_date": "2003-01-01",
        "average_rating": 4,
        "ratings_count": 3,
        "thumbnail": "http//www.google.pl",
    },
    {
        "title": "Four book",
        "authors": ["First Author", "Third Author"],
        "categories": ["Fourth Category", "Second Category"],
        "published_date": "2001-01-01",
        "average_rating": 4,
        "ratings_count": 3,
        "thumbnail": "http//www.google.pl",
    },
]


class TestSetUp(APITestCase):
    def setUp(self):
        self.book_url = reverse("book-list")
        self.db_url = reverse("google-api-call")
        self.raw_data = BOOKS
        self.serializer = BookSerializer

        for book in self.raw_data:
            b = Book.objects.create(
                title=book["title"],
                average_rating=book["average_rating"],
                ratings_count=book["ratings_count"],
                published_date=book["published_date"],
                thumbnail=book["thumbnail"],
            )
            for auth in book["authors"]:
                author, created = Author.objects.get_or_create(name=auth)
                b.authors.add(author)

            for category in book["categories"]:
                c, created = Category.objects.get_or_create(name=category)
                b.categories.add(c)

            b.save()

        self.books = Book.objects.all()
        return super(TestSetUp, self).setUp()

    def tearDown(self):
        return super().tearDown()
