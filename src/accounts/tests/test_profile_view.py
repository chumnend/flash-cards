from django.urls import resolve, reverse
from django.test import TestCase
from django.contrib.auth.models import User
from accounts.views import profile
from decks.models import Deck

class ProfileViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", email="tester@example.com", password="test",)
        self.public_deck = Deck.objects.create(name="public", owner=self.user, publish_status="o")
        self.follower_deck = Deck.objects.create(name="follower", owner=self.user, publish_status="f")
        self.private_deck = Deck.objects.create(name="private", owner=self.user, publish_status="x")
        url = reverse('profile', kwargs={'pk': 1})
        self.response = self.client.get(url)
    
    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/auth/user/1/')
        self.assertEquals(view.func, profile)
