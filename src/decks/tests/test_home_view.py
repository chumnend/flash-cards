from django.urls import resolve, reverse
from django.test import TestCase
from django.contrib.auth.models import User
from decks.views import home
from decks.models import Deck

class HomeViewTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user('tester', 'tester@example.com', 'test')
        self.deck = Deck.objects.create(name='Django1', description='Django deck', owner=self.owner, publish_status='o')
        self.private_deck = Deck.objects.create(name='Django2', description='Django deck', owner=self.owner, publish_status='x')
        url = reverse('home')
        self.response = self.client.get(url)
    
    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/')
        self.assertEquals(view.func, home)
        
    def test_contains_link_to_explore(self):
        explore_url = reverse('explore')
        self.assertContains(self.response, f'href="{explore_url}"')
    
    def test_contains_link_to_deck(self):
        deck_url = reverse('deck', kwargs={'pk': self.deck.pk})
        self.assertContains(self.response, f'href="{deck_url}"')
    
    def test_contains_no_link_to_private_deck(self):
        deck_url = reverse('deck', kwargs={'pk': self.private_deck.pk})
        self.assertNotContains(self.response, f'href="{deck_url}"')

class DashboardViewTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user('tester', 'tester@example.com', 'test')
        self.deck = Deck.objects.create(name='Django1', description='Django deck', owner=self.owner)
        self.client.login(username='tester', password='test')
        url = reverse('home')
        self.response = self.client.get(url)
        
    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)
    
    def test_view_function(self):
        view = resolve('/')
        self.assertEquals(view.func, home)
