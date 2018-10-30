from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('file_upload', views.file_upload, name='file_upload'),
    path('my_files', views.my_files, name='my_files'),
    path('perform', views.perform, name='perform'),
    path('discovery', views.discovery, name='discovery'),
]