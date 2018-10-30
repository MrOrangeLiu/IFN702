import json
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.urls import reverse
from django.conf import settings
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect

from fileuploads.forms import UploadFileForm, SearchForm, ParameterForm
from fileuploads.models import Directory, Profile, ResultFile
from fileuploads.utils import handle_file_upload, handle_result_file

# Create your views here.
def dashboard(request):
	if not request.user.is_authenticated:
		return redirect(reverse('home'))
	return render(request, 'dashboard/index.html')

def file_upload(request):
	context = {}
	data = {}

	if request.method == "POST":
		form_field = UploadFileForm(request.POST, request.FILES)
		if form_field.is_valid():
			file_check_results = handle_file_upload(request)
			data['status'] = 'SUCCESS'
			data['file_not_accepted'] = file_check_results['file_not_accepted']
			data['file_accepted'] = file_check_results['file_accepted']
		else:
			data['status'] = 'ERROR'
			data['messages'] = list(form_field.errors.values())[0]
		return JsonResponse(data)
	else:
		form_field = UploadFileForm()

	context['form_field'] = form_field
	return render(request, 'dashboard/file_upload.html', context)

def my_files(request):
	context = {}
	username = request.user.username
	profile = Profile.objects.filter(owner=username)
	directory = Directory.objects.filter(owner=username)

	folder = request.GET.get('folder', 'all')

	directories = []
	files = []
	for p in profile:
		directories += list(p.directory.all())
	if folder == 'all':
		for d in directory:
			files += list(d.file.all())
	else:
		for d in directory.filter(directory_name=folder):
			files += list(d.file.all())

	page_of_files, page_range = my_paginator(request, files)


	context['directories'] = directories
	context['page_of_files'] = page_of_files
	context['files'] = page_of_files.object_list
	context['page_range'] = page_range
	context['current_directory'] = folder

	return render(request, 'dashboard/my_files.html', context)

def my_paginator(request, objects):
	paginator = Paginator(objects, settings.FILE_FOR_EACH_PAGE)
	page_num = request.GET.get('page', 1)
	page_of_objects = paginator.get_page(page_num)

	current_page_num = page_of_objects.number
	page_range = list(range(max(current_page_num - 2,  1), current_page_num)) + \
				list(range(current_page_num, min(paginator.num_pages, current_page_num + 2) + 1))

	# Add ... to pagination
	if page_range[0] - 1 >= 2:
		page_range.insert(0, '...')
	if paginator.num_pages - page_range[-1] >= 2:
		page_range.append('...')

	# Add first and last page number
	if page_range[0] != 1:
		page_range.insert(0, 1)
	if page_range[-1] != paginator.num_pages:
		page_range.append(paginator.num_pages)

	return page_of_objects, page_range

def perform(request):
	context = {}
	if request.method == "POST":
		file_selected = request.POST.get("file_selected", "")
		context['file_selected'] = file_selected
		context['parameter_form'] = ParameterForm()
	return render(request, 'dashboard/perform.html', context)

def discovery(request):
	context = {}
	data = {}
	file_pk = request.GET.get('id', '')
	if file_pk and request.method == "POST":
		search_field = SearchForm(request.POST, request=request)
		if search_field.is_valid():
			context['table_with_weight'] = json.dumps(search_field.cleaned_data['table_with_weight']['data'])
			context['table_without_weight'] = json.dumps(search_field.cleaned_data['table_without_weight']['data'])
	    # Filter function goes here
		    # request.POST.get("weight", "")
		    # request.POST.get("weight_input", "")
		    # request.POST.get("min_support", "")
		    # request.POST.get("min_support_input", "")
		    # request.POST.get("items", "")
		    # request.POST.get("items_input", "")
	else:
		search_field = SearchForm()

	context['search_field'] = search_field
	result_files = ResultFile.objects.filter(owner=request.user.username)
	context['result_files'] = result_files
	form_field = UploadFileForm()
	context['form_field'] = form_field
	context['file_selected'] = file_pk
	return render(request, 'dashboard/discovery.html', context)