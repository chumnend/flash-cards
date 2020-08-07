from django.urls import resolve, reverse
from django.test import TestCase
from django.contrib.auth.models import User
from accounts.models import UserDetails, Followers
from accounts.views import profile
from decks.models import Deck

class ProfileTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", email="tester@example.com", password="test",)
        self.user_details = UserDetails.objects.create(user=self.user)
        self.follower = User.objects.create_user(username="follower", email="follower@example.com", password="test")
        Followers.objects.create(follower=self.follower, followed=self.user)
        self.public_deck = Deck.objects.create(name="public", owner=self.user, publish_status="o")
        self.follower_deck = Deck.objects.create(name="follower", owner=self.user, publish_status="f")
        self.private_deck = Deck.objects.create(name="private", owner=self.user, publish_status="x")

class ProfileViewUserTests(ProfileTestCase):
    def setUp(self):
        super().setUp()
        url = reverse('profile', kwargs={'pk': 1})
        self.response = self.client.get(url)
        
    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/auth/user/1/')
        self.assertEquals(view.func, profile)
        
    def test_page(self):
        follow_url = reverse('follow', kwargs={'pk': 1})
        public_deck_url = reverse('deck', kwargs={'pk': self.public_deck.pk})
        follower_deck_url = reverse('deck', kwargs={'pk': self.follower_deck.pk})
        private_deck_url = reverse('deck', kwargs={'pk': self.private_deck.pk})
        self.assertContains(self.response, f'href="{follow_url}"')
        self.assertContains(self.response, f'href="{public_deck_url}"')
        self.assertNotContains(self.response, f'href="{follower_deck_url}"')
        self.assertNotContains(self.response, f'href="{private_deck_url}"')
        
class ProfileViewFollowerTests(ProfileTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username='follower', password='test')
        url = reverse('profile', kwargs={'pk': 1})
        self.response = self.client.get(url)
        
    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/auth/user/1/')
        self.assertEquals(view.func, profile)
        
    def test_page(self):
        unfollow_url = reverse('unfollow', kwargs={'pk': 1})
        public_deck_url = reverse('deck', kwargs={'pk': self.public_deck.pk})
        follower_deck_url = reverse('deck', kwargs={'pk': self.follower_deck.pk})
        private_deck_url = reverse('deck', kwargs={'pk': self.private_deck.pk})
        self.assertContains(self.response, f'href="{unfollow_url}"')
        self.assertContains(self.response, f'href="{public_deck_url}"')
        self.assertContains(self.response, f'href="{follower_deck_url}"')
        self.assertNotContains(self.response, f'href="{private_deck_url}"')
