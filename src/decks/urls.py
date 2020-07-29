from django.urls import path
from decks import views

urlpatterns = [
    path("", views.home, name="home"),
    path("explore/", views.explore, name="explore"),
    path("decks/<int:pk>/", views.deck, name="deck"),
]
