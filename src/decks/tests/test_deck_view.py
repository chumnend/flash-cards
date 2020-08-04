from django.urls import resolve, reverse
from django.test import TestCase
from django.contrib.auth.models import User
from decks.views import deck
from decks.models import Deck

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
