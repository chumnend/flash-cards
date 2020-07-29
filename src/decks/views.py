from django.shortcuts import render, get_object_or_404
from decks.models import Category, Deck, Card

def home(request):
    decks = Deck.objects.filter(publish_status="o")[:4]
    context = {
        "decks": decks,
    }
    
    return render(request, 'decks/home.html', context)

def explore(request):
    decks = Deck.objects.filter(publish_status="o")
    categories = Category.objects.all()
    context = {
        "decks": decks,
        "categories": categories,
    }
    
    return render(request, 'decks/explore.html', context)

def deck(request, pk):
    deck = get_object_or_404(Deck, pk=pk)
    cards = Card.objects.filter(deck=deck)
    context = {
        "deck": deck,
        "cards": cards,
        "num_cards": len(cards),
    }

    return render(request, 'decks/deck.html', context)
