from django.shortcuts import render
from decks.models import Deck, Card

def decks_index(request):
    decks = Deck.objects.all()
    context = { 'decks': decks }
    
    return render(request, 'decks_index.html', context)

def decks_category(request, category):
    decks = Deck.objects.filter(categories__name__contains=category)
    context = { 'decks': decks }
    
    return render(request, 'decks_index.html', context)

def decks_detail(request, pk):
    deck = Deck.objects.get(pk=pk)
    cards = Card.objects.filter(deck=deck)
    context = { 
        'deck': deck,
        'cards': cards,
        'num_cards': len(cards),
    }
    
    return render(request, 'decks_detail.html', context)
    