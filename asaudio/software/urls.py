from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("software/", views.SoftwareListView.as_view(), name="software-list",),
    path("software/cat-<int:category>/", views.SoftwareListView.as_view(), name="software-list-category"),
    path("search/", views.SearchView.as_view(), name="search")
]
