from django.contrib import admin
from django.urls import path

from main.views import GoogleApiCall

urlpatterns = [
    path("admin/", admin.site.urls),
    path("db", GoogleApiCall.as_view(), name="google-api-call"),
]
