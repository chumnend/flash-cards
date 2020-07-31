from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)
    
    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

class Deck(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    PUBLISH_STATUS = ( ("o", "public"), ("f", "followers"), ("x", "private") )
    publish_status = models.CharField(max_length=1, choices=PUBLISH_STATUS, default="o")
    owner = models.ForeignKey(User, related_name="decks", on_delete=models.CASCADE)
    categories = models.ManyToManyField("Category", related_name="decks", blank=True)
    
    class Meta:
        ordering = ['updated_at']
    
    def __str__(self):
        return self.name

class Card(models.Model):
    front_text = models.CharField(max_length=30)
    back_text = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    deck = models.ForeignKey("Deck", on_delete=models.CASCADE)
    
    class Meta:
        ordering = ['updated_at']
    
    def __str__(self):
        return f"{self.front_text} | {self.back_text}"
