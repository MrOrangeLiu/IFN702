from django.test import TestCase
from django.test import Client

class ResponseTestCase(TestCase):

    def test_login(self):
        response = self.client.get('/login/login')
        self.assertEqual(response.status_code, 200)
 
    def test_home(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)