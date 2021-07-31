from rest_framework import viewsets

from main.models import Book


class BooksView(viewsets.ModelViewSet):
    queryset = Book.objects.all()
