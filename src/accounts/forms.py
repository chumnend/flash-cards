from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    email = forms.CharField(
        max_length=254, 
        required=True, 
        widget=forms.EmailInput()
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class UserForm(forms.Form):
    email = forms.CharField(
        label="email"
    )
    about_me = forms.CharField(
        label="about me", 
        widget=forms.Textarea()
    )
    
    class Meta:
        fields=('email', 'about_me')
    