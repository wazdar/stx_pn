import responses
from rest_framework import status

from .test_dumydata import google_call
from .tests_setup import BOOKS
from .tests_setup import TestSetUp
from main.models import Book


class TestDbView(TestSetUp):
    def test_db_post_without_q_parm(self):
        post_data = {}
        response = self.client.post(self.db_url, data=post_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()["error"], "q is required")

    def test_db_post_with_empty_q(self):
        post_data = {"q": ""}
        response = self.client.post(self.db_url, data=post_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()["error"], "q is required")

    def test_db_get(self):
        response = self.client.get(self.db_url)

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    @responses.activate
    def test_db_post_with_q(self):
        post_data = {"q": "war"}

        responses.add(
            responses.GET,
            "https://www.googleapis.com/books/v1/volumes?q=war&startIndex=0&maxResults=40",
            json=google_call,
            status=200,
        )

        response = self.client.post(self.db_url, data=post_data)
        books = Book.objects.all()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(google_call["items"]) + len(BOOKS), len(books))
