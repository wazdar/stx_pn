from django.urls import reverse
from rest_framework import status

from .tests_setup import TestSetUp
from main.models import Book


class TestBooksView(TestSetUp):
    def test_books_list_get(self):
        response = self.client.get(self.book_url)
        response_data = response.json()["results"][0]

        books = Book.objects.all()
        serializer = self.serializer(books, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.raw_data[0]["title"], response_data["title"])
        self.assertEqual(response.json()["results"], serializer.data)

    def test_get_one_book(self):
        response = self.client.get(
            reverse("book-detail", kwargs={"pk": self.books[0].pk})
        )
        book = Book.objects.get(pk=self.books[0].pk)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.serializer(book).data)

    def test_get_one_book_error(self):
        response = self.client.get(reverse("book-detail", kwargs={"pk": 666}))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_book_list_sort_by_date(self):
        response = self.client.get(
            reverse("book-list"), data={"sort": "-published_date"}
        )
        response_data = response.json()["results"]

        books_sorted = Book.objects.order_by("-published_date")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data, self.serializer(books_sorted, many=True).data)

    def test_book_filter_by_date(self):
        response = self.client.get(
            reverse("book-list"), data={"published_date": "2001"}
        )
        response_data = response.json()

        books = Book.objects.filter(published_date__icontains="2001")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data["count"], len(books))
        self.assertEqual(len(response_data["results"]), len(books))

    def test_book_filter_by_one_author(self):
        response = self.client.get(
            reverse("book-list"), data={"author": self.books[0].authors.first()}
        )
        response_data = response.json()

        books = Book.objects.filter(authors__name=self.books[0].authors.first())

        self.assertEqual(response_data["count"], len(books))
        self.assertEqual(len(response_data["results"]), len(books))

    def test_book_filter_by_list_of_authors(self):
        authors = ["First Author", "Second Author"]
        response = self.client.get(reverse("book-list"), data={"author": authors})
        response_data = response.json()

        books = Book.objects.filter(authors__name=authors[0]).filter(
            authors__name=authors[1]
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data["count"], len(books))
        self.assertEqual(len(response_data["results"]), len(books))

        self.assertEqual(
            response_data["results"], self.serializer(books, many=True).data
        )
