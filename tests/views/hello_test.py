import pytest
from pyramid.testing import DummyRequest
from unittest import TestCase

from flashly.views.hello import hello_world


class TestHelloWorld(TestCase):
    def test_hello_world(self):
        request = DummyRequest()

        response = hello_world(request)

        self.assertEqual(response, {"message": "Hello World!"})
