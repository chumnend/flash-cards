from django.test import TestCase
from accounts.forms import UserForm

class UserFormTest(TestCase):
    def test_form_has_fields(self):
        form = UserForm()
        expected = ['email', 'about_me',]
        actual = list(form.fields)
        self.assertSequenceEqual(expected, actual)
