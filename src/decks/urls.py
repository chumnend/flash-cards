from django.urls import path
from . import views

urlpatterns = [
    path("", views.decks_index, name="decks_index"),
    path("<int:pk>/", views.decks_detail, name="decks_detail"),
    path("<category>/", views.decks_category, name="decks_category"),
]
