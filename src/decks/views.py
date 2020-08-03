from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from decks.models import Category, Deck, Card
from decks.forms import SearchDeckForm, NewDeckForm

def home(request):
    if request.user.is_authenticated:
        owner_decks = Deck.objects.filter(owner=request.user)
        feed_decks = Deck.objects.filter(publish_status="o")[:6] # TO REPLACE WITH FOLLOWED USER DECKS
        context = {
            "owner_decks": owner_decks,
            "decks": feed_decks,
        }
        return render(request, 'decks/dashboard.html', context)
    else:
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

    deck_paginator = Paginator(decks, 10)
    page_number = request.GET.get('page')
    deck_page_obj = deck_paginator.get_page(page_number)
    
    num_decks = len(decks)
    categories = Category.objects.all()
    form = SearchDeckForm()
    context = {
        "decks": deck_page_obj,
        "num_decks": num_decks,
        "categories": categories,
        "form": form,
    }
    
    return render(request, 'decks/explore.html', context)

@login_required
def decks(request):
    if request.POST:
        pass
    
    decks = Deck.objects.filter(owner=request.user)
    deck_paginator = Paginator(decks, 10)
    page_number = request.GET.get('page')
    deck_page_obj = deck_paginator.get_page(page_number)
    
    context = {
        "decks": deck_page_obj,
    }
    
    return render(request, 'decks/decks.html', context)

@login_required
def new_deck(request):
    if request.POST:
        form = NewDeckForm(request.POST)
        if form.is_valid():
            name=form.cleaned_data['name']
            description=form.cleaned_data['description']
            categories = form.cleaned_data['categories'].split()
            
            deck = Deck.objects.create(
                name=name,
                description=description,
                owner = request.user,
            )
            
            if categories:
                for category in categories:
                    obj, created = Category.objects.get_or_create(name=category)
                    deck.categories.add(obj)
            
            return redirect('home')
    
    form = NewDeckForm()
    context = {
        "form": form,
    }
    
    return render(request, 'decks/new_deck.html', context)

def deck(request, pk):
    deck = get_object_or_404(Deck, pk=pk)
    cards = Card.objects.filter(deck=deck)
    num_cards = len(cards)
    context = {
        "deck": deck,
        "cards": cards,
        "num_cards": num_cards,
    }

    return render(request, 'decks/deck.html', context)

@login_required
def manage_deck(request, pk):
    deck = get_object_or_404(Deck, pk=pk)
    if deck.owner.username != request.user.username:
        return redirect('home')
    
    cards = Card.objects.filter(deck=deck)
    num_cards = len(cards)
    context = {
        "deck": deck,
        "cards": cards,
        "num_cards": num_cards,
    }
    
    return render(request, 'decks/deck_manage.html', context)
