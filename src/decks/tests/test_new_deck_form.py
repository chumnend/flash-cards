from django.test import TestCase
from decks.forms import NewDeckForm

class NewDeckFormTest(TestCase):
    def test_form_has_fields(self):
        form = NewDeckForm()
        expected = ['name', 'description', 'categories',]
        actual = list(form.fields)
        self.assertSequenceEqual(expected, actual)
