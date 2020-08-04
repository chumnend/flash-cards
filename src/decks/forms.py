from django import forms
from decks.models import Deck, Card, Category

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


class DeckForm(forms.ModelForm):
    name = forms.CharField(
        label="Deck Name",
        max_length=20,
    ),
    description = forms.CharField(
        label="Deck Description",
        max_length=2000,
        widget=forms.Textarea(),
    ),
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(), 
        label="Category",
        required=False,
    )
    PUBLISH_STATUS = ( ("x", "Private"), ("f", "Followers Only"), ("o", "Everyone"), )
    publish_status = forms.ChoiceField(
        choices=PUBLISH_STATUS,
        label="Visibility",
        required=False,
    )
    
    class Meta:
        model = Deck
        fields = ['name', 'description', 'categories', 'publish_status']

class CardForm(forms.ModelForm):
    front_text = forms.CharField(
        label="Front Card Text",
        max_length=30,
        widget=forms.Textarea(),
    )
    back_text = forms.CharField(
        label="Back Card Text",
        max_length=30,
        widget=forms.Textarea(),
    )
    
    class Meta:
        model = Card
        fields = ['front_text', 'back_text']
