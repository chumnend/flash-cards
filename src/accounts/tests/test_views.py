from django.core import mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.urls import resolve, reverse
from django.test import TestCase
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
        email = 'tester@example.com'
        User.objects.create_user('tester', email, 'test')
        url = reverse('password_reset')
        self.response = self.client.post(url, {'email': email})
    
    def test_redirection(self):
        url = reverse('password_reset_done')
        self.assertRedirects(self.response, url)
    
    def test_email_sent(self):
        self.assertEqual(len(mail.outbox), 1)

class PasswordResetFailsTests(TestCase):
    def setUp(self):
        url = reverse('password_reset')
        self.response = self.client.post(url, {'email': 'doesnotexist@example.com'})

    def test_redirection(self):
        url = reverse('password_reset_done')
        self.assertRedirects(self.response, url)
    
    def test_email_not_sent(self):
        self.assertEqual(len(mail.outbox), 0)


class PasswordResetDoneViewTests(TestCase):
    def setUp(self):
        url = reverse('password_reset_done')
        self.response = self.client.get(url)
    
    def test_status_code(self):
        self.assertEqual(self.response.status_code, 200)
        
    def test_view_function(self):
        view = resolve('/auth/reset/done/')
        self.assertEquals(view.func.view_class, auth_views.PasswordResetDoneView)
        
class PasswordResetConfirmViewTests(TestCase):
    def setUp(self):
        user = User.objects.create_user('tester', 'tester@example.com', 'test')
        self.uid = urlsafe_base64_encode(force_bytes(user.pk))
        self.token = default_token_generator.make_token(user)
        url = reverse('password_reset_confirm', kwargs={'uidb64': self.uid, 'token': self.token})
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
        '''
        The view must contain two inputs: csrf and two password fields
        '''
        self.assertContains(self.response, '<input', 3)
        self.assertContains(self.response, 'type="password"', 2)

class PasswordResetConfirmInvalidTests(TestCase):
    def setUp(self):
        user = User.objects.create_user('tester', 'tester@example.com', 'test')
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        user.set_password('abcdef123')
        user.save()
        url = reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
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

class PasswordChangeViewTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user('tester', 'tester@example.com', 'test')
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
        self.user = User.objects.create_user('tester', 'tester@example.com', 'old_password1')
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
