from django.db import models

class Category(models.Model):
    '''Model representing a deck category'''
    name = models.CharField(max_length=200, help_text='Enter a category name(e.g. Science Fiction)')
    
    def __str__(self):
        return self.name

class Deck(models.Model):
    '''Model representing a deck'''
    DECK_STATE = (
        ('o', 'Open'),
        ('f', 'Followers Only'),
        ('x', 'Private'),
    )
    
    name = models.CharField(max_length=200, help_text='Enter Deck name')
    description = models.TextField(blank=True, default='', help_text='Enter Deck Description')
    categories = models.ManyToManyField(Category, related_name='decks', blank=True, help_text='Select a categroy for this deck')
    status = models.CharField(max_length=1, choices=DECK_STATE, blank=True, default='x', help_text='Deck privacy')
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    
    class Meta: 
        ordering = ['last_modified']
    
    def __str__(self):
        return self.name

class Card(models.Model):
    '''Model representing a card'''
    front_text = models.CharField(max_length=200)
    back_text = models.CharField(max_length=200)
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.front_text}|{self.back_text}'
    