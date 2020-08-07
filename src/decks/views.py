from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import DeleteView
from decks.forms import SearchDeckForm, DeckForm, CardForm
from decks.models import Category, Deck, Card

def home(request):
    if request.user.is_authenticated:
        owner_decks = Deck.objects.filter(owner=request.user)
        
        f_list = []
        for f in request.user.following.all():
            f_list.append(f.followed.pk)
        
        feed_decks = Deck.objects.filter(
            Q(owner__in=f_list, publish_status="f") |
            Q(owner__in=f_list, publish_status="o") |
            Q(owner=request.user) 
        )
        
        deck_paginator = Paginator(feed_decks, 4)
        page_number = request.GET.get('page')
        deck_page_obj = deck_paginator.get_page(page_number)
        
        context = {
            "owner_decks": owner_decks,
            "decks": deck_page_obj,
        }
        return render(request, 'decks/dashboard.html', context)
    else:
        decks = Deck.objects.filter(publish_status="o")[:4]
        context = {
            "decks": decks,
        }
        return render(request, 'decks/home.html', context)

def explore(request):
    if request.user.is_authenticated:
        f_list = []
        for f in request.user.following.all():
            f_list.append(f.followed.pk)
            
        decks = Deck.objects.filter(
            Q(owner__in=f_list, publish_status="f") |
            Q(publish_status="o") 
        )
    else:
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
        form = DeckForm(request.POST)
        if form.is_valid():
            name=form.cleaned_data['name']
            description=form.cleaned_data['description']
            categories = form.cleaned_data['categories']
            publish_status = form.cleaned_data['publish_status']
            
            deck = Deck.objects.create(
                name=name,
                description=description,
                owner = request.user,
                publish_status = publish_status,
            )
            
            if categories:
                for category in categories:
                    deck.categories.add(category)
            
            return redirect('home')
    
    form = DeckForm()
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
    
    return render(request, 'decks/manage_deck.html', context)

@login_required
def edit_deck(request, pk):
    deck = get_object_or_404(Deck, pk=pk)
    if deck.owner.username != request.user.username:
        return redirect('home')
        
    if request.POST:
        form = DeckForm(request.POST, instance=deck)
        if form.is_valid():
            form.save()
            return redirect('manage_deck', pk=pk)
    
    form = DeckForm(instance=deck)
    context = {
        'deck': deck,
        'form': form,
    }
    
    return render(request, 'decks/edit_deck.html', context)

@method_decorator(login_required, name="dispatch")
class DeleteDeck(DeleteView):
    model = Deck
    pk_url_kwarg= 'pk'
    template_name= 'decks/delete_deck.html'
    success_url = reverse_lazy('decks')

@login_required
def new_card(request, pk):
    deck = get_object_or_404(Deck, pk=pk)
    if deck.owner.username != request.user.username:
        return redirect('home')
    
    if request.POST:
        form = CardForm(request.POST)
        if form.is_valid():
            front_text=form.cleaned_data['front_text']
            back_text=form.cleaned_data['back_text']

            Card.objects.create(
                front_text=front_text,
                back_text=back_text,
                deck=deck,
            )
            
            return redirect('manage_deck', pk=pk)
            
    form = CardForm()
    context = {
        "form": form,
    }
    
    return render(request, 'decks/new_card.html', context)

@login_required
def edit_card(request, deck_pk, card_pk):
    deck = get_object_or_404(Deck, pk=deck_pk)
    card = get_object_or_404(Card, pk=card_pk)
    if deck.owner.username != request.user.username:
        return redirect('home')
        
    if request.POST:
        form = CardForm(request.POST, instance=card)
        if form.is_valid():
            form.save()
            return redirect('manage_deck', pk=deck_pk)
    
    form = CardForm(instance=card)
    context = {
        'deck': deck,
        'card': card,
        'form': form,
    }
    
    return render(request, 'decks/edit_card.html', context)

@method_decorator(login_required, name="dispatch")
class DeleteCard(DeleteView):
    model = Card
    pk_url_kwarg= 'card_pk'
    template_name= 'decks/delete_card.html'

    def get_success_url(self, **kwargs):
        return reverse_lazy('manage_deck', kwargs={'pk': self.kwargs['deck_pk']})
