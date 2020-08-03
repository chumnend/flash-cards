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
    ),
    description = forms.CharField(
        label="Deck Description",
        max_length=2000,
        widget=forms.Textarea(),
    ),
    categories = forms.CharField(
        label="Categories",
        max_length=200,
        required=False,
        help_text="Seperate categories using spaces",
    )
    
    class Meta:
        model = Deck
        fields = ['name', 'description', 'categories']
