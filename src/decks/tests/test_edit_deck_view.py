from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse
from decks.forms import DeckForm
from decks.models import Deck
from decks.views import edit_deck

class EditDeckViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='tester', 
            email='tester@example.com', 
            password='test',
        )
        self.deck = Deck.objects.create(
            name='Django1', 
            description='Django deck', 
            owner=self.user, 
            publish_status='o',
        )
        self.client.login(username='tester', password='test')
        url = reverse('edit_deck', kwargs={'pk': self.deck.pk})
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)
    
    def test_view_function(self):
        view = resolve('/decks/1/edit/')
        self.assertEquals(view.func, edit_deck)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, DeckForm)

class EditDeckLoginRequiredTest(TestCase):
    def setUp(self):
        self.url = reverse('edit_deck', kwargs={'pk': 1})
        self.response = self.client.get(self.url)
    
    def test_redirection(self):
        url = reverse('login')
        self.assertRedirects(self.response, f'{url}?next={self.url}')

class EditDeckSuccessTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='tester', 
            email='tester@example.com', 
            password='test'
        )
        self.deck = Deck.objects.create(
            name='Django1', 
            description='Django deck', 
            owner=self.user, 
            publish_status='o'
        )
        self.client.login(
            username='tester', 
            password='test'
        )
        url = reverse('edit_deck', kwargs={'pk': self.deck.pk})
        self.response = self.client.post(url, {
            'name': 'Django2',
            'description': 'changed',
            'publish_status': 'x',
        })
        
    def test_redirection(self):
        url = reverse('manage_deck', kwargs={'pk': self.deck.pk})
        self.assertRedirects(self.response, url)
        
    def test_update(self):
        self.deck.refresh_from_db()
        self.assertEquals(self.deck.name, 'Django2')
        self.assertEquals(self.deck.description, 'changed')
        self.assertEquals(self.deck.publish_status, 'x')
    
class EditDeckUnauthorizedTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='tester', 
            email='tester@example.com', 
            password='test'
        )
        self.other_user = User.objects.create_user(
            username='tester1', 
            email='tester1@example.com', 
            password='test1'
        )
        self.deck = Deck.objects.create(
            name='Django1', 
            description='Django deck', 
            owner=self.user, 
            publish_status='o'
        )
        self.client.login(
            username='tester1', 
            password='test1'
        )
        url = reverse('edit_deck', kwargs={'pk': self.deck.pk})
        self.response = self.client.post(url, {
            'name': 'Django2',
            'description': 'changed',
            'publish_status': 'x',
        })
    
    def test_redirection(self):
        url = reverse('home')
        self.assertRedirects(self.response, url)

class EditDeckFailTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(
            username='tester', 
            email='tester@example.com', 
            password='test'
        )
        self.deck = Deck.objects.create(
            name='Django1', 
            description='Django deck', 
            owner=self.owner, 
            publish_status='o'
        )
        self.client.login(
            username='tester', 
            password='test'
        )
        url = reverse('edit_deck', kwargs={'pk': self.deck.pk})
        self.response = self.client.post(url, {
            'name': '',
            'description': 'changed',
            'publish_status': 'x',
        })
        
    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)
    
    def test_no_update(self):
        self.deck.refresh_from_db()
        self.assertEquals(self.deck.name, 'Django1')
        self.assertEquals(self.deck.description, 'Django deck')
        self.assertEquals(self.deck.publish_status, 'o')
    