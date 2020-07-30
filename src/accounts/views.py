from django.contrib.auth import login
from django.shortcuts import render, redirect
from accounts.forms import RegisterForm

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
