from django import forms
from decks.models import Deck, Category

class SearchDeckForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs = {
                'placeholder': 'Enter Search Name',
            }
        ), 
        label="Name", 
        max_length=20, 
        required=False,
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(), 
        label="Category",
        empty_label="All",
        required=False,
    )

    class Meta:
        model = Deck
        fields = ['name', 'category']
