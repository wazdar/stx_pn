from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=254)

    def __str__(self):
        return str(self.name)


class Category(models.Model):
    name = models.CharField(max_length=254)

    def __str__(self):
        return str(self.name)


class Book(models.Model):
    authors = models.ManyToManyField(Author)
    categories = models.ManyToManyField(Category)

    title = models.CharField(max_length=254)
    published_date = models.CharField(max_length=10, null=True)
    average_rating = models.FloatField(default=0)
    ratings_count = models.IntegerField(default=0)
    thumbnail = models.URLField(null=True)

    def __str__(self):
        return str(self.title)
