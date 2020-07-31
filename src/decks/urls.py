from django.urls import path
from decks import views

urlpatterns = [
    path("", views.home, name="home"),
    path("explore/", views.explore, name="explore"),
    path("decks/new/", views.new_deck, name="new_deck"),
    path("decks/<int:pk>/", views.deck, name="deck"),
]
