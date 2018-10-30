from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'fileuploads'
urlpatterns = [
    path('test/', views.test, name='test'),
    path('upload_result/', views.upload_result, name='upload_result'),
]