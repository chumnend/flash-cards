from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse
from decks.models import Deck
from decks.views import decks

class DecksView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='tester', 
            email='tester@example.com', 
            password='test'
        )
        self.client.login(username='tester', password='test')
        self.deck = Deck.objects.create(
            name='Django1', 
            description='Django deck', 
            owner=self.user,
        )
        self.private_deck = Deck.objects.create(
            name='Django2', 
            description='Django deck', 
            owner=self.user, 
            publish_status='x',
        )
        url = reverse('decks')
        self.response = self.client.get(url)
    
    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)
    
    def test_view_function(self):
        view = resolve('/decks/')
        self.assertEquals(view.func, decks)

    def test_contains_link_to_deck(self):
        deck_url = reverse('deck', kwargs={'pk': self.deck.pk})
        self.assertContains(self.response, f'href="{deck_url}"')
        
    def test_contains_link_to_private_deck(self):
        deck_url = reverse('deck', kwargs={'pk': self.private_deck.pk})
        self.assertContains(self.response, f'href="{deck_url}"')

class DecksLoginRequiredTests(TestCase):
    def setUp(self):
        self.url = reverse('decks')
        self.response = self.client.get(self.url)
    
    def test_redirection(self):
        login_url = reverse('login')
        self.assertRedirects(self.response, f'{login_url}?next={self.url}')
