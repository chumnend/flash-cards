from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse
from accounts.models import UserDetails, Followers

class FollowTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="tester", 
            email="tester@example.com", 
            password="test",
        )
        self.target_user = User.objects.create_user(
            username="target", 
            email="target@example.com", 
            password="test",
        )
        self.target_user_details = UserDetails.objects.create(
            user=self.target_user
        )

class FollowViewTests(FollowTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username='tester', password='test')
        url = reverse('follow', kwargs={'pk': self.target_user.pk})
        self.response = self.client.get(url)
        
    def test_redirection(self):
        url = reverse('profile', kwargs={'pk': self.target_user.pk })
        self.assertRedirects(self.response, url)
        
    def test_follow(self):
        self.assertTrue(Followers.objects.exists())

class FollowRequiredTests(FollowTestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse('follow', kwargs={'pk': self.target_user.pk})
        self.response = self.client.get(self.url)
    
    def test_redirection(self):
        login_url = reverse('login')
        self.assertRedirects(self.response, f'{login_url}?next={self.url}')
