from unittest import TestCase

from webtest import TestApp

from flashly import main


class Test(TestCase):
    def setUp(self):
        app = main({})

        self.testapp = TestApp(app)

    def test_status(self):
        response = self.testapp.get("/status", status=200)

    def test_404_not_found(self):
        response = self.testapp.get("/nonexistent", status=404)
