from django_filters import rest_framework as filters
from rest_framework import viewsets

from main.models import Book
from main.serializers import BookSerializer


class BookFilter(filters.FilterSet):
    published_date = filters.CharFilter(lookup_expr="icontains")
    author = filters.CharFilter(method="filter_author")

    class Meta:
        model = Book
        fields = ["published_date", "author"]

    def filter_author(self, queryset, name, value):
        """
        Filtering by author or authors.
        :param queryset:
        :param name:
        :param value:
        :return:
        """
        author_list = self.request.GET.getlist("author")

        for author in author_list:
            queryset = queryset.filter(authors__name=author)
        return queryset


class BooksView(viewsets.ReadOnlyModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    filterset_class = BookFilter

    def get_queryset(self):

        if self.request.GET.get("sort", False):
            sort = self.request.GET.get("sort")
            if sort in ["published_date", "-published_date"]:
                return Book.objects.all().order_by(sort)

        return Book.objects.all()
