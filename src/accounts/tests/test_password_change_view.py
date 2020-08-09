from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse

class PasswordChangeViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='tester', 
            email='tester@example.com', 
            password='test',
        )
        self.client.login(username='tester', password='test')
        url = reverse('password_change')
        self.response = self.client.get(url)
        
    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)
    
    def test_view_function(self):
        view = resolve('/auth/change/')
        self.assertEquals(view.func.view_class, auth_views.PasswordChangeView)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, PasswordChangeForm)
        
    def test_form_inputs(self):
        self.assertContains(self.response, '<input', 4)
        self.assertContains(self.response, 'type="password"', 3)

class PasswordChangeLoginRequiredTests(TestCase):
    def test_redirection(self):
        url = reverse('password_change')
        login_url = reverse('login')
        response = self.client.get(url)
        self.assertRedirects(response, f'{login_url}?next={url}')

class PasswordChangeSuccessTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='tester', 
            email='tester@example.com',
            password='old_password1',
        )
        self.client.login(username='tester', password='old_password1')
        url = reverse('password_change')
        data = {
            'old_password': 'old_password1',
            'new_password1': 'new_password1',
            'new_password2': 'new_password1',
        }
        self.response = self.client.post(url, data)

    def test_redirection(self):
        url = reverse('password_change_done')
        self.assertRedirects(self.response, url)

    def test_password_changed(self):
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('new_password1'))

    def test_user_authentication(self):
        response = self.client.get(reverse('home'))
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated)
        
class PasswordChangeFailTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('tester', 'tester@example.com', 'old_password1')
        self.client.login(username='tester', password='old_password1')
        url = reverse('password_change')
        data = {}
        self.response = self.client.post(url, data)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)

    def test_didnt_change_password(self):
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('old_password1'))
