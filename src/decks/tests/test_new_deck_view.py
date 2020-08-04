from django.urls import resolve, reverse
from django.test import TestCase
from django.contrib.auth.models import User
from decks.views import new_deck
from decks.models import Deck, Category
from decks.forms import NewDeckForm

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
