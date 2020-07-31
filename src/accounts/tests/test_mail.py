from django.core import mail
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase

class PasswordResetMailTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('tester', 'tester@example.com', 'test')
        url = reverse('password_reset')
        self.response = self.client.post(url, { 'email': self.user.email })
        self.email = mail.outbox[0]

    def test_email_subject(self):
        self.assertEqual('[Flash Cards] Reset your password', self.email.subject)
    
    def test_email_body(self):
        context = self.response.context
        token = context.get('token')
        uid = context.get('uid')
        password_reset_token_url = reverse('password_reset_confirm', kwargs={
            'uidb64': uid,
            'token': token
        })
        self.assertIn(password_reset_token_url, self.email.body)
        self.assertIn(self.user.username, self.email.body)
        self.assertIn(self.user.email, self.email.body)

    def test_email_to(self):
        self.assertEqual([self.user.email,], self.email.to)
