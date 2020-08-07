from django.urls import resolve, reverse
from django.test import TestCase
from django.contrib.auth.models import User
from decks.views import decks
from decks.models import Deck

class DecksView(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user('tester', 'tester@example.com', 'test')
        self.client.login(username='tester', password='test')
        self.deck = Deck.objects.create(name='Django1', description='Django deck', owner=self.owner)
        self.private_deck = Deck.objects.create(name='Django2', description='Django deck', owner=self.owner, publish_status='x')
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
