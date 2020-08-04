from django.test import TestCase
from decks.forms import NewCardForm

class NewCardFormTest(TestCase):
    def test_form_has_fields(self):
        form = NewCardForm()
        expected = ['front_text', 'back_text',]
        actual = list(form.fields)
        self.assertSequenceEqual(expected, actual)
