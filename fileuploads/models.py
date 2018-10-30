import datetime
import os

from djongo import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

class SentenceItem(models.Model):
	_id = models.ObjectIdField()
	sentence = models.CharField(max_length=255)
	class Meta:
		abstract = True
	def __str__(self):
		return self.sentence

class File(models.Model):
	_id = models.ObjectIdField()
	file_name = models.CharField(max_length=200)
	file_path = models.CharField(max_length=200)
	# pub_date = models.DateTimeField('date published')
	created_time = models.DateTimeField(auto_now_add=True)
	# last_updated_time = models.DateTimeField(auto_now=True)
	file_content = models.ArrayModelField(model_container=SentenceItem,)

	def __str__(self):
		return self.file_name

class Directory(models.Model):
	_id = models.ObjectIdField()
	directory_name = models.CharField(max_length=200)
	# user = models.EmbeddedModelField(model_container=User,)
	owner = models.CharField(max_length=200)
	file = models.ArrayReferenceField(to=File, on_delete=models.CASCADE,)

	def __str__(self):
		return self.directory_name

class Profile(models.Model):
	_id = models.ObjectIdField()
	owner = models.CharField(max_length=200)
	directory = models.ArrayReferenceField(to=Directory, on_delete=models.DO_NOTHING,)

	def __str__(self):
		return self.owner

class QueryItem(models.Model):
	_id = models.ObjectIdField()
	items = models.CharField(max_length=255)
	support = models.CharField(max_length=100)
	weight = models.CharField(max_length=100)
	class Meta:
		abstract = True
	def __str__(self):
		return self.items

class ResultFile(models.Model):
	_id = models.ObjectIdField()
	file_name = models.CharField(max_length=200)
	file_path = models.CharField(max_length=200)
	owner = models.CharField(max_length=200)
	# pub_date = models.DateTimeField('date published')
	created_time = models.DateTimeField(auto_now_add=True)
	# last_updated_time = models.DateTimeField(auto_now=True)
	file_content = models.ArrayModelField(model_container=QueryItem,)

	def __str__(self):
		return self.file_name




