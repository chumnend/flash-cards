from django.urls import resolve, reverse
from django.test import TestCase
from django.contrib.auth.models import User
from decks.views import home, explore, decks, new_deck, deck, manage_deck
from decks.models import Deck, Category
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
    
    def test_view_function(self):
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

class NewDeckLoginRequiredTests(TestCase):
    def setUp(self):
        self.url = reverse('new_deck')
        self.response = self.client.get(self.url)
    
    def test_redirection(self):
        login_url = reverse('login')
        self.assertRedirects(self.response, f'{login_url}?next={self.url}')

class NewDeckSuccessTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user('tester', 'tester@example.com', 'test')
        self.category = Category.objects.create(name="Science")
        self.client.login(username='tester', password='test')
        data = {
            'name': 'Test',
            'description': 'Lorem ipsum dolor sit amet',
            'category': self.category,
        }
        url = reverse('new_deck')
        self.response = self.client.post(url, data)

    def test_redirection(self):
        url = reverse('home')
        self.assertRedirects(self.response, url)
    
    def test_create(self):
        self.assertTrue(Deck.objects.exists())
        
class NewDeckFailTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user('tester', 'tester@example.com', 'test')
        self.client.login(username='tester', password='test')
        data = {
            'name': '',
            'description': 'Lorem ipsum dolor sit amet',
        }
        url = reverse('new_deck')
        self.response = self.client.post(url, data)
        
    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)
        
    def test_no_create(self):
        self.assertFalse(Deck.objects.exists())
    
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

class DeckManageViewTests(TestCase):
    def setUp(self):
        self.owner1 = User.objects.create_user('tester', 'tester@example.com', 'test')
        self.owner2 = User.objects.create_user('tester2', 'tester2@example.com', 'test2')
        self.deck = Deck.objects.create(name='Django1', description='Django deck', owner=self.owner1)
        self.client.login(username='tester', password='test')
        url = reverse('manage_deck', kwargs={'pk': 1})
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/decks/1/manage/')
        self.assertEquals(view.func, manage_deck)
        
    def test_redirection(self):
        self.client.login(username='tester2', password='test2')
        url = reverse('manage_deck', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertRedirects(response, reverse('home'))
    
class DeckManageLoginRequiredTests(TestCase):
    def setUp(self):
        self.url = reverse('manage_deck', kwargs={'pk': 1})
        self.response = self.client.get(self.url)
    
    def test_redirection(self):
        url = reverse('login')
        self.assertRedirects(self.response, f'{url}?next={self.url}')
