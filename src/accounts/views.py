from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from accounts.forms import RegisterForm, UserForm
from accounts.models import UserDetails, Followers

def register(request):
    if request.POST:
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserDetails.objects.create(user=user)
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
        
    context = {
        "form": form,    
    }
    
    return render(request, 'accounts/register.html', context)

def profile(request, pk):
    current_user = get_object_or_404(User, pk=pk)
    current_user_details = get_object_or_404(UserDetails, user=current_user)
    following = current_user.following.all()
    followers = current_user.followers.all()
    
    if request.user.is_authenticated:
        if request.user == current_user:
            return redirect('settings')
            
        is_following = len(followers.filter(follower=request.user)) > 0
        if is_following:
            decks = current_user.decks.all().exclude(publish_status='x')
        else:
            decks = current_user.decks.filter(publish_status='o')
    else: 
        decks = decks = current_user.decks.filter(publish_status='o')
        is_following = False
    
    deck_paginator = Paginator(decks, 10)
    page_number = request.GET.get('page')
    deck_page_obj = deck_paginator.get_page(page_number)
    
    context = {
        "current_user": current_user,
        "username": current_user.username,
        "about_me": current_user_details.about_me,
        "gravatar": current_user_details.gravatar(),
        "following_count": len(following),
        "follower_count": len(followers),
        "decks": deck_page_obj,
        "is_following": is_following,
    }
    
    return render(request, 'accounts/profile.html', context)
    
@login_required
def settings(request):
    user_details = get_object_or_404(UserDetails, user=request.user)
    following = request.user.following.all()
    followers = request.user.followers.all()

    if request.POST:
        form = UserForm(request.POST)
        if form.is_valid():
            request.user.email = form.cleaned_data['email']
            request.user.save()
            user_details.about_me = form.cleaned_data['about_me']
            user_details.save()
            return redirect('settings')
    
    form = UserForm(initial={
        'email': request.user.email, 
        'about_me': user_details.about_me}
    )
    
    context = {
        "username": request.user.username,
        "about_me": user_details.about_me,
        "gravatar": user_details.gravatar(),
        "following": following,
        "followers": followers,
        "following_count": len(following),
        "follower_count": len(followers),
        "form": form,
    }
    
    return render(request, 'accounts/settings.html', context)

@login_required
def follow(request, pk):
    current_user = get_object_or_404(User, pk=pk)
    Followers.objects.create(
        follower=request.user,
        followed=current_user,
    )
    
    return redirect('profile', pk=current_user.pk)

@login_required
def unfollow(request, pk):
    current_user = get_object_or_404(User, pk=pk)
    Followers.objects.filter(
        follower=request.user,
        followed=current_user,
    ).delete()

    return redirect('profile', pk=current_user.pk)
