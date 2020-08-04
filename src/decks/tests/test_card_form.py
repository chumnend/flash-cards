from django.test import TestCase
from decks.forms import CardForm

class CardFormTest(TestCase):
    def test_form_has_fields(self):
        form = CardForm()
        expected = ['front_text', 'back_text',]
        actual = list(form.fields)
        self.assertSequenceEqual(expected, actual)
