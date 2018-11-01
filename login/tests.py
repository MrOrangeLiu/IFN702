from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User

class LoginTestCase(TestCase):
	def setUp(self):
		User.objects.create_user(username="test", email="test@test.com", password="test")

	def test_user_login(self):
		c = Client()
		response = c.post('/login/login/', {'username': 'test', 'password': 'test'})
		self.assertEqual(response.status_code, 302)

	def test_user_register(self):
		c = Client()
		response = c.post('/login/register/', {'username': 'test_reg', 'email':'test_reg@test.com', 'password': 'test_reg'})
		self.assertEqual(response.status_code, 200)

	def test_database_user_existence(self):
		test_user = User.objects.get(username="test")
		self.assertIsNotNone(test_user)