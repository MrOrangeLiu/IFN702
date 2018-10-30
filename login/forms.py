from django import forms
from django.contrib import auth
from django.contrib.auth.models import User

class LoginForm(forms.Form):
	username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Input your username'}))
	password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Input your password'}))

	def clean(self):
		username = self.cleaned_data['username']
		password = self.cleaned_data['password']
		user = auth.authenticate(username=username, password=password)
		if user is None:
			raise forms.ValidationError('Username or password is incorrect') # Throw exceptions
		else:
			self.cleaned_data['user'] = user
		return self.cleaned_data

class RegForm(forms.Form):
	username = forms.CharField(label='Username', 
							   max_length=30, 
							   min_length=3, 
							   widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Input your username (3-30 chars)'}))

	email = forms.EmailField(label='Email', 
							 widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Input your email'}))

	password = forms.CharField(label='Password', 
							   min_length=6, 
							   widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Input your password'}))

	password_again = forms.CharField(label='Input Password Again', 
									 min_length=6, 
									 widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Input your password again'}))

	# Verify if username is repeated
	def clean_username(self):
		username = self.cleaned_data['username']
		# if User.objects.filter(username=username).count():
		if User.objects.filter(username=username).exists():
			raise forms.ValidationError('Username has already existed')
		return username

	# Verify Email
	def clean_email(self):
		email = self.cleaned_data['email']
		if User.objects.filter(email=email).exists():
			raise forms.ValidationError('Email has already existed')
		return email

	# Verify password
	def clean_password_again(self):
		password = self.cleaned_data['password']
		password_again = self.cleaned_data['password_again']
		if password != password_again:
			raise forms.ValidationError('Password and password again are not same')
		return password_again

