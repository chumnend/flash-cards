from django.urls import resolve, reverse
from django.test import TestCase
from django.contrib.auth.models import User
from accounts.models import UserDetails, Followers

class FollowViewTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="johndoe", email="johndoe@example.com", password="test",)
        self.user1_details = UserDetails.objects.create(user=self.user1)
        self.user2 = User.objects.create_user(username="chrishanell", email="chrishanell@example.com", password="test",)
        self.client.login(username='chrishanell', password='test')
        url = reverse('follow', kwargs={'pk': 1})
        self.response = self.client.get(url)
        
    def test_redirection(self):
        url = reverse('profile', kwargs={'pk': self.user1.pk })
        self.assertRedirects(self.response, url)
        
    def test_follow(self):
        self.assertTrue(Followers.objects.exists())

class FollowRequiredTests(TestCase):
    def setUp(self):
        self.url = reverse('follow', kwargs={'pk': 1})
        self.response = self.client.get(self.url)
    
    def test_redirection(self):
        login_url = reverse('login')
        self.assertRedirects(self.response, f'{login_url}?next={self.url}')