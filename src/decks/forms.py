from django import forms
from decks.models import Deck, Category

class SearchDeckForm(forms.ModelForm):
    name = forms.CharField(
        label="Name", 
        max_length=20, 
        required=False,
        widget=forms.TextInput(
            attrs= {'placeholder': 'Search by deck name'}
        )
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(), 
        label="Category",
        empty_label=" ",
        required=False,
    )

    class Meta:
        model = Deck
        fields = ['name', 'category']


class NewDeckForm(forms.ModelForm):
    name = forms.CharField(
        label="Deck Name",
        max_length=20,
        widget=forms.TextInput()
    ),
    description = forms.CharField(
        label="Deck Description",
        max_length=2000,
        widget=forms.Textarea(),
    ),
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(), 
        label="Category",
        empty_label="All",
        required=False,
    )
    
    class Meta:
        model = Deck
        fields = ['name', 'description', 'category']
