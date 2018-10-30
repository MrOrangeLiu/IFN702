import json
from django.shortcuts import render, redirect
from django.urls import reverse
from fileuploads.forms import UploadFileForm, SearchForm, ParameterForm
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect

def home(request):
	if request.method == "POST":
		context = {}
		parameter_form = ParameterForm(request.POST)
		fileupload_form = UploadFileForm(request.POST, request.FILES)
		if parameter_form.is_valid():
			min_support = parameter_form.cleaned_data['min_support']
			threshold = parameter_form.cleaned_data['threshold']
			parameter3 = parameter_form.cleaned_data['parameter3']
			query_input = parameter_form.cleaned_data['query_input']

			# Upload files
			if fileupload_form.is_valid():
				search_field = SearchForm()
				context['search_field'] = search_field
				return render(request, 'trail.html', locals())
			else:
				return render(request, 'home.html', locals())
	else:
		parameter_form = ParameterForm()
		fileupload_form = UploadFileForm()
	return render(request, 'home.html', locals())

def trail(request):
	context = {}
	search_field = SearchForm()
	context['search_field'] = search_field
	if request.method == "POST":
		parameter_form = ParameterForm(request.POST, request.FILES)
		if parameter_form.is_valid():
			# Model function goes here
			# Insert your code here ...
			return render(request, 'trail.html', context)
	else:
		return render(request, 'trail.html', context)

def discovery(request):
	context = {}
	data = {}
	if request.method == "POST":
		search_field = SearchForm(request.POST, request=request)
		if search_field.is_valid():
			context['table_with_weight'] = json.dumps(search_field.cleaned_data['table_with_weight']['data'])
			context['table_without_weight'] = json.dumps(search_field.cleaned_data['table_without_weight']['data'])
			context['search_field'] = search_field
			return render(request, 'trail.html', context)
		else:
			context['search_field'] = search_field
			return render(request, 'trail.html', context)
	else:
		return redirect(reverse('home'))

def validator_decimal(num, min, max, decimal_places):
    if float(num) >= float(min) and float(num) <= float(max):
        return round(float(num), decimal_places)
    return False

