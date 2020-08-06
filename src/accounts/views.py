from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from accounts.forms import RegisterForm
from accounts.models import Followers

def register(request):
    if request.POST:
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
        
    context = {
        "form": form,    
    }
    
    return render(request, 'accounts/register.html', context)

def profile(request, pk):
    user_profile = get_object_or_404(User, pk=pk)
    following_count = len(user_profile.following.all())
    follower_count = len(user_profile.followers.all())
    
    if request.user.is_authenticated:
        is_user = request.user == user_profile
        is_following = user_profile.followers.filter(follower=request.user)
        
        if is_user:
            decks = user_profile.decks.all()
        elif not is_user and is_following:
            decks = user_profile.decks.all().exclude(publish_status='x')
        else:
            decks = user_profile.decks.filter(publish_status='o')
    else: 
        decks = decks = user_profile.decks.filter(publish_status='o')
        is_user = False
        is_following = False
    
    deck_paginator = Paginator(decks, 10)
    page_number = request.GET.get('page')
    deck_page_obj = deck_paginator.get_page(page_number)
    
    context = {
        "user_profile": user_profile,
        "following_count": following_count,
        "follower_count": follower_count,
        "is_user": is_user,
        "is_following": is_following,
        "decks": deck_page_obj,
    }
    
    return render(request, 'accounts/profile.html', context)

@login_required
def follow(request, pk):
    user_profile = get_object_or_404(User, pk=pk)
    Followers.objects.create(
        follower=request.user,
        followed=user_profile,
    )
    
    return redirect('profile', pk=user_profile.pk)

@login_required
def unfollow(request, pk):
    user_profile = get_object_or_404(User, pk=pk)
    Followers.objects.filter(
        follower=request.user,
        followed=user_profile,
    ).delete()

    return redirect('profile', pk=user_profile.pk)
