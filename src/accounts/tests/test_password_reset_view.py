from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm, PasswordChangeForm
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User
from django.core import mail
from django.test import TestCase
from django.urls import resolve, reverse

class PasswordResetViewsTests(TestCase):
    def setUp(self):
        url = reverse('password_reset')
        self.response = self.client.get(url)
    
    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)
        
    def test_view_function(self):
        view = resolve('/auth/reset/')
        self.assertEquals(view.func.view_class, auth_views.PasswordResetView)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, PasswordResetForm)
        
    def test_form_inputs(self):
        self.assertContains(self.response, '<input', 2)
        self.assertContains(self.response, 'type="email"', 1)

class PasswordResetSuccessTests(TestCase):
    def setUp(self):
        self.user=User.objects.create_user(
            username='tester', 
            email='tester@example.com', 
            password='test',
        )
        url = reverse('password_reset')
        self.response = self.client.post(url, {
            'email': self.user.email,
        })
    
    def test_redirection(self):
        url = reverse('password_reset_done')
        self.assertRedirects(self.response, url)
    
    def test_email_sent(self):
        self.assertEqual(len(mail.outbox), 1)

class PasswordResetFailsTests(TestCase):
    def setUp(self):
        url = reverse('password_reset')
        self.response = self.client.post(url, {
            'email': 'doesnotexist@example.com'
        })

    def test_redirection(self):
        url = reverse('password_reset_done')
        self.assertRedirects(self.response, url)
    
    def test_email_not_sent(self):
        self.assertEqual(len(mail.outbox), 0)
