from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("software/", views.SoftwareListView.as_view(), name="software-list",),
    path("developer/<slug:pk>", views.DeveloperView.as_view(), name="developer", ),
    path("developers/", views.DeveloperListView.as_view(), name="developer-list", ),
    path("software/cat-<int:category>/", views.SoftwareListView.as_view(), name="software-list-category"),
    path("search/", views.SearchView.as_view(), name="search"),
    path("stats/", views.stats, name="stats"),
]
