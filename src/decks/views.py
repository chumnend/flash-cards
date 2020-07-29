from django.shortcuts import render, redirect, get_object_or_404
from decks.models import Category, Deck, Card
from decks.forms import SearchDeckForm

def home(request):
    decks = Deck.objects.filter(publish_status="o")[:4]
    context = {
        "decks": decks,
    }
    
    return render(request, 'decks/home.html', context)

def explore(request):
    decks = Deck.objects.filter(publish_status='o')
    if request.method == 'POST':
        form = SearchDeckForm(request.POST)
        if form.is_valid():
            decks = decks.filter(name__icontains=form.cleaned_data['name'])
            if form.cleaned_data['category']:
                decks = decks.filter(categories__name__contains=form.cleaned_data['category'])

    categories = Category.objects.all()
    form = SearchDeckForm()
    context = {
        "decks": decks,
        "categories": categories,
        "form": form,
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
