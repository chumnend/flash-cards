from django.urls import resolve, reverse
from django.test import TestCase
from django.contrib.auth.models import User
from decks.views import home, explore, deck, new_deck
from decks.models import Deck
from decks.forms import SearchDeckForm, NewDeckForm

class HomeViewTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user('tester', 'tester@example.com', 'test')
        self.deck = Deck.objects.create(name='Django1', description='Django deck', owner=self.owner)
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
    
    def test_home_url_resolves_dashboard_view(self):
        view = resolve('/')
        self.assertEquals(view.func, home)

class ExploreViewTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user('tester', 'tester@example.com', 'test')
        self.deck = Deck.objects.create(name='Django1', description='Django deck', owner=self.owner)
        self.private_deck = Deck.objects.create(name='Django2', description='Django deck', owner=self.owner, publish_status='x')
        url = reverse('explore')
        self.response = self.client.get(url)
    
    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/explore/')
        self.assertEquals(view.func, explore)
    
    def test_contains_link_to_home(self):
        home_url = reverse('home')
        self.assertContains(self.response, f'href="{home_url}"')
    
    def test_contains_link_to_deck(self):
        deck_url = reverse('deck', kwargs={'pk': self.deck.pk})
        self.assertContains(self.response, f'href="{deck_url}"')
        
    def test_contains_no_link_to_private_deck(self):
        deck_url = reverse('deck', kwargs={'pk': self.private_deck.pk})
        self.assertNotContains(self.response, f'href="{deck_url}"')
    
    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, SearchDeckForm)

class NewDeckViewTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user('tester', 'tester@example.com', 'test')
        self.client.login(username='tester', password='test')
        url = reverse('new_deck')
        self.response = self.client.get(url)
    
    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)
    
    def test_view_function(self):
        view = resolve('/decks/new/')
        self.assertEquals(view.func, new_deck)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, NewDeckForm)
        
    def test_form_inputs(self):
        self.assertContains(self.response, '<input', 2)
        self.assertContains(self.response, 'type="text"', 1)
        self.assertContains(self.response, 'textarea', 1)
        self.assertContains(self.response, 'select', 1)

class DeckViewTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user('tester', 'tester@example.com', 'test')
        self.deck = Deck.objects.create(name='Django1', description='Django deck', owner=self.owner)
        url = reverse('deck', kwargs={'pk': 1})
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test__not_found_status_code(self):
        url = reverse('deck', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_view_function(self):
        view = resolve('/decks/1/')
        self.assertEquals(view.func, deck)
        
    def test_contains_link_to_home(self):
        home_url = reverse('home')
        self.assertContains(self.response, f'href="{home_url}"')
    
    def test_contains_link_to_explore(self):
        explore_url = reverse('explore')
        self.assertContains(self.response, f'href="{explore_url}"')
