from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.test import TestCase
from django.urls import resolve, reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

class PasswordResetConfirmViewTests(TestCase):
    def setUp(self):
        user = User.objects.create_user(
            username='tester', 
            email='tester@example.com', 
            password='test',
        )
        self.uid = urlsafe_base64_encode(force_bytes(user.pk))
        self.token = default_token_generator.make_token(user)
        url = reverse('password_reset_confirm', kwargs={
            'uidb64': self.uid, 
            'token': self.token,
        })
        self.response = self.client.get(url, follow=True)
    
    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve(f'/auth/reset/{self.uid}/{self.token}/')
        self.assertEquals(view.func.view_class, auth_views.PasswordResetConfirmView)
   
    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, SetPasswordForm)

    def test_form_inputs(self):
        self.assertContains(self.response, '<input', 3)
        self.assertContains(self.response, 'type="password"', 2)

class PasswordResetConfirmInvalidTests(TestCase):
    def setUp(self):
        user = User.objects.create_user(
            username='tester', 
            email='tester@example.com', 
            password='test',
        )
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        user.set_password('abcdef123')
        user.save()
        url = reverse('password_reset_confirm', kwargs={
            'uidb64': uid, 
            'token': token,
        })
        self.response = self.client.get(url, follow=True)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_html(self):
        url = reverse('password_reset')
        self.assertContains(self.response, 'invalid link')
        self.assertContains(self.response, f'href="{url}"')

class PasswordResetCompleteViewTests(TestCase):
    def setUp(self):
        url = reverse('password_reset_complete')
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/auth/reset/complete/')
        self.assertEquals(view.func.view_class, auth_views.PasswordResetCompleteView)
