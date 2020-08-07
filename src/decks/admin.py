from django.contrib import admin
from .models import Category, Deck, Card

class CategoryAdmin(admin.ModelAdmin):
    pass

class DeckAdmin(admin.ModelAdmin):
    pass

class CardAdmin(admin.ModelAdmin):
    pass

admin.site.register(Category, CategoryAdmin)
admin.site.register(Deck, DeckAdmin)
admin.site.register(Card, CardAdmin)
