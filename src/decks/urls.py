from django.urls import path
from decks import views

urlpatterns = [
    path("", views.home, name="home")
]
