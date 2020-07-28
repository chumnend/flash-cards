from django.contrib import admin
from decks.models import Category, Deck, Card

class DeckAdmin(admin.ModelAdmin):
    pass

class CardAdmin(admin.ModelAdmin):
    pass

class CategoryAdmin(admin.ModelAdmin):
    pass

admin.site.register(Deck, DeckAdmin)
admin.site.register(Card, CardAdmin)
admin.site.register(Category, CategoryAdmin)
