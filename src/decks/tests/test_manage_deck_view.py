from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse
from decks.models import Deck
from decks.views import manage_deck

class DeckManageViewTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='tester', 
            email='tester@example.com', 
            password='test',
        )
        self.user2 = User.objects.create_user(
            username='tester2', 
            email='tester2@example.com', 
            password='test2',
        )
        self.deck = Deck.objects.create(
            name='Django1', 
            description='Django deck', 
            owner=self.user1,
        )
        self.client.login(username='tester', password='test')
        url = reverse('manage_deck', kwargs={'pk': self.deck.pk})
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/decks/1/manage/')
        self.assertEquals(view.func, manage_deck)
        
    def test_redirection(self):
        self.client.login(username='tester2', password='test2')
        url = reverse('manage_deck', kwargs={'pk': self.deck.pk})
        response = self.client.get(url)
        self.assertRedirects(response, reverse('home'))

class DeckManageLoginRequiredTests(TestCase):
    def setUp(self):
        self.url = reverse('manage_deck', kwargs={'pk': 1})
        self.response = self.client.get(self.url)
    
    def test_redirection(self):
        url = reverse('login')
        self.assertRedirects(self.response, f'{url}?next={self.url}')
