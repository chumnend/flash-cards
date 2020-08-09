from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse
from decks.forms import DeckForm
from decks.models import Deck, Category
from decks.views import new_deck

class NewDeckViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='tester', 
            email='tester@example.com', 
            password='test',
        )
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
        self.assertIsInstance(form, DeckForm)

class NewDeckLoginRequiredTests(TestCase):
    def setUp(self):
        self.url = reverse('new_deck')
        self.response = self.client.get(self.url)
    
    def test_redirection(self):
        login_url = reverse('login')
        self.assertRedirects(self.response, f'{login_url}?next={self.url}')

class NewDeckSuccessTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='tester', 
            email='tester@example.com', 
            password='test',
        )
        self.category = Category.objects.create(name="Science")
        self.client.login(username='tester', password='test')
        url = reverse('new_deck')
        self.response = self.client.post(url, {
            'name': 'Test',
            'description': 'Lorem ipsum dolor sit amet',
            'category': self.category,
            'publish_status': 'o',
        })

    def test_redirection(self):
        url = reverse('decks')
        self.assertRedirects(self.response, url)
    
    def test_create(self):
        self.assertTrue(Deck.objects.exists())
        
class NewDeckFailTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='tester', 
            email='tester@example.com', 
            password='test',
        )
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
