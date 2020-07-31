from django.test import TestCase
from decks.forms import SearchDeckForm, NewDeckForm

class SearchDeckFormTest(TestCase):
    def test_form_has_fields(self):
        form = SearchDeckForm()
        expected = ['name', 'category',]
        actual = list(form.fields)
        self.assertSequenceEqual(expected, actual)
        
class NewDeckFormTest(TestCase):
    def test_form_has_fields(self):
        form = NewDeckForm()
        expected = ['name', 'description', 'category',]
        actual = list(form.fields)
        self.assertSequenceEqual(expected, actual)
