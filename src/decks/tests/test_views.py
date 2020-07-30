from django.urls import resolve, reverse
from django.test import TestCase
from django.contrib.auth.models import User
from decks.views import home, explore, deck
from decks.models import Deck
from decks.forms import SearchDeckForm

class HomeViewTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user('tester', 'tester@example.com', 'test')
        self.deck = Deck.objects.create(name='Django1', description='Django deck', owner=self.owner)
        self.private_deck = Deck.objects.create(name='Django2', description='Django deck', owner=self.owner, publish_status='x')
    
    def test_home_view_status_code(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEquals(view.func, home)
        
    def test_home_view_contains_link_to_explore_page(self):
        home_url = reverse('home')
        response = self.client.get(home_url)
        explore_url = reverse('explore')
        self.assertContains(response, f'href="{explore_url}"')
    
    def test_home_view_contains_link_to_deck_page(self):
        home_url = reverse('home')
        response = self.client.get(home_url)
        deck_url = reverse('deck', kwargs={'pk': self.deck.pk})
        self.assertContains(response, f'href="{deck_url}"')
    
    def test_home_view_contains_no_link_to_private_deck(self):
        home_url = reverse('home')
        response = self.client.get(home_url)
        deck_url = reverse('deck', kwargs={'pk': self.private_deck.pk})
        self.assertNotContains(response, f'href="{deck_url}"')

class ExploreViewTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user('tester', 'tester@example.com', 'test')
        self.deck = Deck.objects.create(name='Django1', description='Django deck', owner=self.owner)
        self.private_deck = Deck.objects.create(name='Django2', description='Django deck', owner=self.owner, publish_status='x')
    
    def test_explore_view_status_code(self):
        url = reverse('explore')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_explore_url_resolves_explore_view(self):
        view = resolve('/explore/')
        self.assertEquals(view.func, explore)
    
    def test_explore_view_contains_link_back_to_home(self):
        explore_url = reverse('explore')
        response = self.client.get(explore_url)
        home_url = reverse('home')
        self.assertContains(response, f'href="{home_url}"')
    
    def test_explore_view_contains_link_to_deck_page(self):
        explore_url = reverse('explore')
        response = self.client.get(explore_url)
        deck_url = reverse('deck', kwargs={'pk': self.deck.pk})
        self.assertContains(response, f'href="{deck_url}"')
        
    def test_explore_view_contains_no_link_to_private_deck(self):
        explore_url = reverse('explore')
        response = self.client.get(explore_url)
        deck_url = reverse('deck', kwargs={'pk': self.private_deck.pk})
        self.assertNotContains(response, f'href="{deck_url}"')
    
    def test_contains_form(self):
        explore_url = reverse('explore')
        response = self.client.get(explore_url)
        form = response.context.get('form')
        self.assertIsInstance(form, SearchDeckForm)

class DeckViewTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user('tester', 'tester@example.com', 'test')
        self.deck = Deck.objects.create(name='Django1', description='Django deck', owner=self.owner)

    def test_deck_view_success_status_code(self):
        url = reverse('deck', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_deck_view_not_found_status_code(self):
        url = reverse('deck', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_deck_url_resolves_deck_view(self):
        view = resolve('/decks/1/')
        self.assertEquals(view.func, deck)
        
    def test_deck_view_contains_link_back_to_home(self):
        deck_url = reverse('deck', kwargs={'pk': 1})
        response = self.client.get(deck_url)
        home_url = reverse('home')
        self.assertContains(response, f'href="{home_url}"')
    
    def test_deck_view_contains_link_back_to_explore(self):
        deck_url = reverse('deck', kwargs={'pk': 1})
        response = self.client.get(deck_url)
        explore_url = reverse('explore')
        self.assertContains(response, f'href="{explore_url}"')
