from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse
from decks.forms import CardForm
from decks.models import Deck, Card
from decks.views import edit_card

class EditCardViewTests(TestCase):
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
        self.card = Card.objects.create(
            front_text='test', 
            back_text='test', 
            deck=self.deck,
        )
        self.client.login(username='tester', password='test')
        url = reverse('edit_card', kwargs={
            'deck_pk': self.deck.pk, 
            'card_pk': self.card.pk,
        })
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)
    
    def test_view_function(self):
        view = resolve('/decks/1/card/1/edit/')
        self.assertEquals(view.func, edit_card)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, CardForm)

class EditCardLoginRequiredTest(TestCase):
    def setUp(self):
        self.url = reverse('edit_card', kwargs={
            'deck_pk': 1, 
            'card_pk': 1
        })
        self.response = self.client.get(self.url)
    
    def test_redirection(self):
        url = reverse('login')
        self.assertRedirects(self.response, f'{url}?next={self.url}')

class EditCardSuccessTests(TestCase):
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
        self.card = Card.objects.create(
            front_text='test',
            back_text='test',
            deck=self.deck,
        )
        self.client.login(
            username='tester', 
            password='test'
        )
        url = reverse('edit_card', kwargs={
            'deck_pk': self.deck.pk, 
            'card_pk': self.card.pk,
        })
        self.response = self.client.post(url, {
            'front_text': 'test1',
            'back_text': 'test1',
        })
        
    def test_redirection(self):
        url = reverse('manage_deck', kwargs={'pk': self.deck.pk})
        self.assertRedirects(self.response, url)
        
    def test_update(self):
        self.card.refresh_from_db()
        self.assertEquals(self.card.front_text, 'test1')
        self.assertEquals(self.card.back_text, 'test1')
    
class EditCardUnauthorizedTests(TestCase):
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
        self.card = Card.objects.create(
            front_text='test',
            back_text='test',
            deck=self.deck,
        )
        self.client.login(
            username='tester1', 
            password='test1'
        )
        url = reverse('edit_card', kwargs={
            'deck_pk': self.deck.pk, 
            'card_pk': self.card.pk,
        })
        self.response = self.client.post(url, {
            'front_text': 'test2',
            'back_text': 'test1',
        })
    
    def test_redirection(self):
        url = reverse('home')
        self.assertRedirects(self.response, url)

class EditDeckFailTests(TestCase):
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
        self.card = Card.objects.create(
            front_text='test',
            back_text='test',
            deck=self.deck,
        )
        self.client.login(
            username='tester', 
            password='test'
        )
        url = reverse('edit_card', kwargs={
            'deck_pk': self.deck.pk, 
            'card_pk': self.card.pk,
        })
        self.response = self.client.post(url, {
            'front_text': '',
            'back_text': '',
        })
        
    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)
    
    def test_no_update(self):
        self.deck.refresh_from_db()
        self.assertEquals(self.card.front_text, 'test')
        self.assertEquals(self.card.back_text, 'test')
    