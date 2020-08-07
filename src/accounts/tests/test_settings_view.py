from django.urls import resolve, reverse
from django.test import TestCase
from django.contrib.auth.models import User
from accounts.models import UserDetails
from accounts.forms import UserForm
from accounts.views import settings

class SettingsViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", email="tester@example.com", password="test",)
        self.user_details = UserDetails.objects.create(user=self.user)
        self.client.login(username='tester', password='test')
        self.url = reverse('settings')
        self.response = self.client.get(self.url)
    
    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/auth/settings/')
        self.assertEquals(view.func, settings)
        
    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, UserForm)

class SettingsLoginRequired(TestCase):
    def setUp(self):
        self.url = reverse('settings')
        self.response = self.client.get(self.url)
    
    def test_redirection(self):
        login_url = reverse('login')
        self.assertRedirects(self.response, f'{login_url}?next={self.url}')

class UserFormSuccessTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tester', email='tester@example.com', password='test')
        self.user_details = UserDetails.objects.create(user=self.user, about_me='this is a test')
        self.client.login(username='tester', password='test')
        url = reverse('settings')
        self.response = self.client.post(url, {
            'email': 'tester2@example.com',
            'about_me': 'success'
        })

    def test_redirection(self):
        url = reverse('settings')
        self.assertRedirects(self.response, url)
    
    def test_update(self):
        self.user.refresh_from_db()
        self.user_details.refresh_from_db()
        self.assertEquals(self.user.email, 'tester2@example.com')
        self.assertEquals(self.user_details.about_me, 'success')
