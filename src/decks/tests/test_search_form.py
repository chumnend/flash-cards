from django.test import TestCase
from decks.forms import SearchDeckForm

class SearchDeckFormTest(TestCase):
    def test_form_has_fields(self):
        form = SearchDeckForm()
        expected = ['name', 'category',]
        actual = list(form.fields)
        self.assertSequenceEqual(expected, actual)
