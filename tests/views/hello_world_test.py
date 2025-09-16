import pytest
from pyramid.testing import DummyRequest

from flashly.views.hello_world import hello_world

class TestHelloWorld:
    def test_hello_world(self):
        request = DummyRequest()

        response = hello_world(request)

        assert response == {'message': "Hello World!"}
