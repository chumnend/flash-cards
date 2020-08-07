from django.test import TestCase
from decks.forms import DeckForm

class DeckFormTest(TestCase):
    def test_form_has_fields(self):
        form = DeckForm()
        expected = ['name', 'description', 'categories', 'publish_status',]
        actual = list(form.fields)
        self.assertSequenceEqual(expected, actual)
