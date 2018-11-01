from django.test import RequestFactory, TestCase
from django.test import Client
from django.contrib.auth.models import User
from .views import dashboard, file_upload, my_files, perform, discovery

class DashboardTestCase(TestCase):

	# Manipulate user logged in
	def setUp(self):
		# Every test needs access to the request factory.
		self.factory = RequestFactory()
		self.user = User.objects.create_user(username="test", email="test@test.com", password="test")

	def test_dashboard_main_page(self):
		# Create an instance of a GET request.
		request = self.factory.get('/dashboard/dashboard')
		# Recall that middleware are not supported. You can simulate a
        # logged-in user by setting request.user manually.
		request.user = self.user
		response = dashboard(request)
		self.assertEqual(response.status_code, 200)

	def test_dashboard_uploaded_files_page(self):
		# Create an instance of a GET request.
		request = self.factory.get('/dashboard/file_upload')
		# Recall that middleware are not supported. You can simulate a
        # logged-in user by setting request.user manually.
		request.user = self.user
		response = file_upload(request)
		self.assertEqual(response.status_code, 200)

	def test_dashboard_my_files_page(self):
		# Create an instance of a GET request.
		request = self.factory.get('/dashboard/my_files')
		# Recall that middleware are not supported. You can simulate a
        # logged-in user by setting request.user manually.
		request.user = self.user
		response = my_files(request)
		self.assertEqual(response.status_code, 200)

	def test_dashboard_perform_page(self):
		# Create an instance of a GET request.
		request = self.factory.get('/dashboard/perform')
		# Recall that middleware are not supported. You can simulate a
        # logged-in user by setting request.user manually.
		request.user = self.user
		response = perform(request)
		self.assertEqual(response.status_code, 200)

	def test_dashboard_discovery_page(self):
		# Create an instance of a GET request.
		request = self.factory.get('/dashboard/discovery')
		# Recall that middleware are not supported. You can simulate a
        # logged-in user by setting request.user manually.
		request.user = self.user
		response = discovery(request)
		self.assertEqual(response.status_code, 200)


class FileUploadTestCase(TestCase):

	# Manipulate user logged in
	def setUp(self):
		# Every test needs access to the request factory.
		self.factory = RequestFactory()
		self.user = User.objects.create_user(username="test", email="test@test.com", password="test")

	def test_file_upload(self):
		c = Client()
		with open('/Users/liuqinyu/Desktop/Project2/IFN702/test_files/APW20000824.txt') as fp:
			response = c.post('/dashboard/file_upload', {'file_field': fp})
			print(response.content)

 	