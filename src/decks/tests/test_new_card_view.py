from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse
from decks.forms import CardForm
from decks.models import Deck, Card
from decks.views import new_card

class NewCardViewTests(TestCase):
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
        )
        self.client.login(username='tester', password='test')
        url = reverse('new_card', kwargs={'pk': self.deck.pk})
        self.response = self.client.get(url)
    
    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)
    
    def test_view_function(self):
        view = resolve('/decks/1/card/new/')
        self.assertEquals(view.func, new_card)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, CardForm)
        
class NewCardLoginRequiredTests(TestCase):
    def setUp(self):
        self.url = reverse('new_card', kwargs={'pk': 1})
        self.response = self.client.get(self.url)
    
    def test_redirection(self):
        login_url = reverse('login')
        self.assertRedirects(self.response, f'{login_url}?next={self.url}')

class NewCardSuccessTests(TestCase):
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
        )
        self.client.login(username='tester', password='test')
        data = {
            'front_text': 'Lorem ipsum dolor sit amet',
            'back_text': 'Lorem ipsum dolor sit amet',
        }
        url = reverse('new_card', kwargs={'pk': self.deck.pk})
        self.response = self.client.post(url, data)

    def test_redirection(self):
        url = reverse('manage_deck', kwargs={'pk': self.deck.pk})
        self.assertRedirects(self.response, url)
    
    def test_create(self):
        self.assertTrue(Card.objects.exists())
        
class NewCardFailTests(TestCase):
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
        )
        self.client.login(username='tester', password='test')
        data = {
            'front_text': '',
            'back_text': 'Lorem ipsum dolor sit amet',
        }
        url = reverse('new_card', kwargs={'pk': self.deck.pk})
        self.response = self.client.post(url, data)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)
        
    def test_no_create(self):
        self.assertFalse(Card.objects.exists())
