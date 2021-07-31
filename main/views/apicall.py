from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from main.models import Author
from main.models import Book
from main.models import Category
from stx_pn.utility import ApiRequest


class GoogleApiCall(APIView):
    def post(self, request):
        """
        Importing data from google API.
        :param request:
        :return:
        """
        if request.data.get("q", None):
            data_from_api = ApiRequest(q=request.data.get("q")).get_data()

            new_books = 0
            new_authors = 0
            new_category = 0

            for data in data_from_api:
                book, book_created = Book.objects.update_or_create(
                    title=data["title"],
                    published_date=data["publication_date"],
                    average_rating=data["average_rating"],
                    ratings_count=data["ratings_count"],
                    thumbnail=data["thumbnail"],
                )
                new_books += 1 if book_created else 0

                if data["authors"] is not None:
                    for author in data["authors"]:
                        author, author_created = Author.objects.get_or_create(
                            name=author
                        )
                        book.authors.add(author)
                        new_authors += 1 if author_created else 0

                if data["categories"] is not None:
                    for category in data["categories"]:
                        category, category_created = Category.objects.get_or_create(
                            name=category
                        )
                        book.categories.add(category)
                        new_category += 1 if category_created else 0

            return Response(
                {
                    "new_books": new_books,
                    "new_category": new_category,
                    "new_authors": new_authors,
                },
                status=status.HTTP_201_CREATED,
            )

        return Response({"error": "q is required"}, status=status.HTTP_400_BAD_REQUEST)
