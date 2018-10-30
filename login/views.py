from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import auth
from django.contrib.auth.models import User

from .forms import LoginForm, RegForm

# Create your views here.
def login(request):

	if request.user.is_authenticated:
		return redirect(reverse('home'))

	if request.method == 'POST':
		login_form = LoginForm(request.POST)
		if login_form.is_valid():
			user = login_form.cleaned_data['user']
			auth.login(request, user)
			return redirect(reverse('dashboard:dashboard')) # Namespace is dashboard
	else:
		login_form = LoginForm()

	context = {}
	context['login_form'] = login_form
	return render(request, 'login/login.html', context)

def register(request):

	if request.user.is_authenticated:
		return redirect(reverse('home'))

	if request.method == 'POST':
		reg_form = RegForm(request.POST)
		if reg_form.is_valid():
			username = reg_form.cleaned_data['username']
			email = reg_form.cleaned_data['email']
			password = reg_form.cleaned_data['password']

			user = User.objects.create_user(username, email, password)
			user.save()

			user = auth.authenticate(username=username, password=password)
			auth.login(request, user)
			return redirect(reverse('dashboard:dashboard'))
	else:
		reg_form = RegForm()

	context = {}
	context['reg_form'] = reg_form

	return render(request, 'login/register.html', context)

def logout(request):
	auth.logout(request)
	return redirect(reverse('home'))