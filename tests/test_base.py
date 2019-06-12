import unittest
import json
import re
from base64 import b64encode
from flask import url_for

from app import app
from app.models import *

class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()
        self.client = app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_404(self):
        response = self.client.get(
            '/wrong/url',
            headers='')
        responseHTML = str(response.data)
        self.assertTrue(response.status_code == 404)
        self.assertIn('Oops!', responseHTML)
        self.assertIn('Page Not found', responseHTML)
        self.assertIn('404', responseHTML)
        self.assertIn('You may have mistyped the address or the page may have moved', responseHTML)
        self.assertIn('<a class="button button-gray-800-outline" href="/">Go to home page</a>', responseHTML)


    def test_404(self):
        response = self.client.get(
            '/wrong/url',
            headers='')
        responseHTML = str(response.data)
        self.assertTrue(response.status_code == 404)
        self.assertIn('Oops!', responseHTML)
        self.assertIn('Page Not found', responseHTML)
        self.assertIn('404', responseHTML)
        self.assertIn('You may have mistyped the address or the page may have moved', responseHTML)
        self.assertIn('<a class="button button-gray-800-outline" href="/">Go to home page</a>', responseHTML)

if __name__ == '__main__':
    unittest.main()