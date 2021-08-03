from django.contrib import admin
from django.urls import include
from django.urls import path
from rest_framework import routers

from main.views import BooksView
from main.views import GoogleApiCall

router = routers.SimpleRouter()
router.register(r"books", BooksView)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("db", GoogleApiCall.as_view(), name="google-api-call"),
    path("", include(router.urls)),
]
