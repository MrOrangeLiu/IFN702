from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.conf import settings

from suit_dashboard.views import DashboardView

from . import forms
from .models import File, Directory, Profile
from .forms import UploadFileForm
from .utils import handle_result_file

import os
import time
import zipfile

def validator_decimal(num, min, max, decimal_places):
    if float(num) >= float(min) and float(num) <= float(max):
        return round(float(num), decimal_places)
    return False

# Page of Result Files Uploads
def upload_result(request):
    context = {}
    data = {}
    if request.method == "POST":
        form_field = forms.UploadFileForm(request.POST, request.FILES)
        if form_field.is_valid():
            file_obj = handle_result_file(request)
            data['status'] = 'SUCCESS'
            data['table_data'] = file_obj['data']
            # return render(request, 'fileuploads/show_result.html', context)
        else:
            data['status'] = 'ERROR'
            data['messages'] = list(form_field.errors.values())[0]
        return JsonResponse(data)
    else:
        form_field = forms.UploadFileForm()
    context['form_field'] = form_field
    return render(request, 'dashboard/discovery.html', context)

def test(request):
    # latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # context = {'latest_question_list': latest_question_list}
    title = {'title': 'TestPage'}
    return render(request, 'fileuploads/test.html', title)