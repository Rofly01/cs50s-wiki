from unicodedata import name
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("create", views.create, name="create"),
    path("<str:entry>", views.entry_page, name="entry"),
    path("<str:page>/edit", views.edit, name="edit"),
    path("ext/rdm", views.random, name="random")
]
