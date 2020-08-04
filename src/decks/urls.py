from django.urls import path
from decks import views

urlpatterns = [
    path("", views.home, name="home"),
    path("explore/", views.explore, name="explore"),
    path("decks/", views.decks, name="decks"),
    path("decks/new/", views.new_deck, name="new_deck"),
    path("decks/<int:pk>/", views.deck, name="deck"),
    path("decks/<int:pk>/manage/", views.manage_deck, name="manage_deck"),
    path("decks/<int:pk>/edit/", views.edit_deck, name="edit_deck"),
    path("decks/<int:pk>/delete/", views.delete_deck, name="delete_deck"),
    path("decks/<int:pk>/card/new/", views.new_card, name="new_card"),
    path("decks/<int:deck_pk>/card/<int:card_pk>/", views.edit_card, name="edit_card"),
    path("decks/<int:deck_pk>/card/<int:card_pk>/", views.delete_card, name="delete_card"),
]
