from django.urls import resolve, reverse
from django.test import TestCase
from django.contrib.auth.models import User
from accounts.views import register
from accounts.forms import RegisterForm

class RegisterViewTests(TestCase):
    def setUp(self):
        url = reverse('register')
        self.response = self.client.get(url)
    
    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/auth/register/')
        self.assertEquals(view.func, register)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, RegisterForm)
        
    def test_form_inputs(self):
        self.assertContains(self.response, '<input', 5)
        self.assertContains(self.response, 'type="text"', 1)
        self.assertContains(self.response, 'type="email"', 1)
        self.assertContains(self.response, 'type="password"', 2)

class RegisterSuccessTests(TestCase):
    def setUp(self):
        url = reverse('register')
        data = {
            'username': 'test',
            'email': 'test@example.com',
            'password1': 'abcdef123456',
            'password2': 'abcdef123456',
        }
        self.response = self.client.post(url, data)
        self.home_url = reverse('home')

    def test_redirection(self):
        self.assertRedirects(self.response, self.home_url)

    def test_user_creation(self):
        self.assertTrue(User.objects.exists())

    def test_user_authentication(self):
        response = self.client.get(self.home_url)
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated)

class RegisterFailTests(TestCase):
    def setUp(self):
        url = reverse('register')
        self.response = self.client.post(url, {})

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_no_user_creation(self):
        self.assertFalse(User.objects.exists())