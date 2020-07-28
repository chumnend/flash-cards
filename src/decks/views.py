from django.shortcuts import render
from decks.models import Deck, Card

def home(request):
    decks = Deck.objects.all()
    context = {
        "decks": decks,
    }
    
    return render(request, 'decks/home.html', context)
