from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse
from accounts.models import UserDetails, Followers

class UnfollowViewTests(TestCase):
    def setUp(self):
        self.target_user = User.objects.create_user(
            username="johndoe", 
            email="johndoe@example.com", 
            password="test",
        )
        self.target_user_details = UserDetails.objects.create(user=self.target_user)
        self.user = User.objects.create_user(
            username="chrishanell", 
            email="chrishanell@example.com", 
            password="test",
        )
        self.client.login(username='chrishanell', password='test')
        url = reverse('follow', kwargs={'pk': self.target_user.pk})
        self.response = self.client.get(url)
        url = reverse('unfollow', kwargs={'pk': self.target_user.pk})
        self.response = self.client.get(url)
    
    def test_redirection(self):
        url = reverse('profile', kwargs={'pk': self.target_user.pk })
        self.assertRedirects(self.response, url)
    
    def test_follow(self):
        self.assertFalse(Followers.objects.exists())

class UnfollowLoginRequiredTests(TestCase):
    def setUp(self):
        self.url = reverse('unfollow', kwargs={'pk': 1 })
        self.response = self.client.get(self.url)
    
    def test_redirection(self):
        login_url = reverse('login')
        self.assertRedirects(self.response, f'{login_url}?next={self.url}')
