from django.contrib.auth.models import User
from django.urls import resolve, reverse
from django.test import TestCase
from accounts.views import register
from accounts.forms import RegisterForm

class RegisterViewTests(TestCase):
    def test_register_status_code(self):
        url = reverse('register')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_signup_url_resolves_signup_view(self):
        view = resolve('/auth/register/')
        self.assertEquals(view.func, register)

    def test_csrf(self):
        url = reverse('register')
        response = self.client.get(url)
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        url = reverse('register')
        response = self.client.get(url)
        form = response.context.get('form')
        self.assertIsInstance(form, RegisterForm)
        
    def test_form_inputs(self):
        url = reverse('register')
        response = self.client.get(url)
        self.assertContains(response, '<input', 5)
        self.assertContains(response, 'type="text"', 1)
        self.assertContains(response, 'type="email"', 1)
        self.assertContains(response, 'type="password"', 2)

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

    def test_register_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_dont_create_user(self):
        self.assertFalse(User.objects.exists())
