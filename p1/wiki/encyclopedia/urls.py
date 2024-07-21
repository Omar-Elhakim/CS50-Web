from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:entry>", views.entry, name="entry"),
    path("random/", views.Random, name="random"),
    path("newEntry/", views.newEntry, name="newEntry"),
    path("newEntry/submitedData/", views.submit, name="submit"),
    path("search/", views.search, name="search"),
]
