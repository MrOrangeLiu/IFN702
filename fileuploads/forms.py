import operator
from django import forms
from IFN702.utils import validator_decimal, is_float
from django.db.models import ObjectDoesNotExist
from .models import ResultFile
# from django.core.validators import MaxValueValidator
# from captcha.fields import CaptchaField

class UploadFileForm(forms.Form):
    # title = forms.CharField(max_length=50, label="Name Your File (Set default leave empty)", required=False)
    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={
    		'multiple': True, 
    		'class': 'form-control',
    		'id': 'chat_file',
    		'placeholder': 'Choose a file...',
    		}))

class ParameterForm(forms.Form):
	min_support = forms.DecimalField(label="Minimum Support", initial=1.0, decimal_places=3, required=True,  
				widget=forms.NumberInput(attrs={
					'class':'form-control', 
					'placeholder':'Minimum Support',
					}))
	threshold = forms.DecimalField(label="Threshold", initial=1.0, decimal_places=1, required=True,  
				widget=forms.NumberInput(attrs={
					'class':'form-control', 
					'placeholder':'Threshold'
					}))
	parameter3 = forms.DecimalField(label="parameter3", initial=1.0, decimal_places=1, required=True, 
				widget=forms.NumberInput(attrs={
					'class':'form-control', 
					'placeholder':'parameter3'
					}))
	query_input = forms.CharField(label="Query", max_length=128, required=True,
				widget=forms.TextInput(attrs={
					'class':'form-control', 
					'placeholder':'Please input your query'
					}))

	def clean_min_support(self):
		min_support = self.cleaned_data['min_support']
		if not is_float(min_support):
			raise forms.ValidationError('Your input has to be numbers')
		if not validator_decimal(min_support, 0, 1, 3):
			raise forms.ValidationError('Minimum support has to be [0, 1]')
		return min_support

	def clean_threshold(self):
		threshold = self.cleaned_data['threshold']
		if not is_float(threshold):
			raise forms.ValidationError('Your input has to be numbers')
		if not validator_decimal(threshold, 0, 2, 1):
			raise forms.ValidationError('Threshold has to be [0, 2]')
		return threshold

	def clean_parameter3(self):
		parameter3 = self.cleaned_data['parameter3']
		if not is_float(parameter3):
			raise forms.ValidationError('Your input has to be numbers')
		if not validator_decimal(parameter3, 0, 2, 1):
			raise forms.ValidationError('Parameter3 has to be [0, 1]')
		return parameter3


class SearchForm(forms.Form):

	Options1 = [('gt', 'Greater Than'), ('lt', 'Less Than'), ('eq', 'Equal To')]
	Options2 = [('contains', 'Contain'), ('eq', 'Equal To')]
	weight_input = forms.DecimalField(label="Weight", initial=0, max_digits=3, decimal_places=2, required=True,  
				widget=forms.TextInput(attrs={
					'id': 'weight_input', 
					'name': 'weight_input', 
					'class':'form-control', 
					}))
	weight_select = forms.ChoiceField(label="Weight Operation", widget=forms.Select, choices=Options1)

	min_support_input = forms.DecimalField(label="Minimum Support", initial=0, max_digits=3, decimal_places=2, required=True,  
				widget=forms.TextInput(attrs={
					'id': 'min_support_input', 
					'name': 'min_support_input', 
					'class':'form-control', 
					}))
	min_support_select = forms.ChoiceField(label="Minimum Support Operation", widget=forms.Select, choices=Options1)

	items_input = forms.CharField(label="Items", max_length=128, required=False,  
				widget=forms.TextInput(attrs={
					'id': 'items_input', 
					'name': 'items_input', 
					'class':'form-control', 
					}))
	items_select = forms.ChoiceField(label="Items Operation", widget=forms.Select, choices=Options2)

	def __init__(self, *args, **kwargs):
		if 'request' in kwargs:
			self.request = kwargs.pop('request')
		super(SearchForm, self).__init__(*args, **kwargs)

	def clean(self):

		def search(source, relate, target):
			ops = {
				'gt':operator.gt,
				'lt':operator.lt,
				'eq':operator.eq,
				'contains': operator.contains,
			}
			return ops[relate](source, target)

		error = ''
		weight_input = self.cleaned_data['weight_input']
		min_support_input = self.cleaned_data['min_support_input']
		items_input = self.cleaned_data['items_input']

		if weight_input == '':
			weight_input = 0
		if min_support_input == '':
			min_support_input = 0

		weight_select = self.cleaned_data['weight_select']
		min_support_select = self.cleaned_data['min_support_select']
		items_select = self.cleaned_data['items_select']

		if not (is_float(weight_input) and is_float(min_support_input)):
			raise forms.ValidationError('Your input has to be numbers. %s and %s are not.' % (weight_input, min_support_input))
			
		w_b, w_decimal = validator_decimal(weight_input, 0, 3, 3)
		if not w_b:
			error += 'Weight has to be [0, 1] '
		m_b, m_decimal = validator_decimal(min_support_input, 0, 1, 3)
		if not m_b:
			error += 'Minimum support has to be [0, 3] '

		if error.strip() != '':
			raise forms.ValidationError(error)
		else:
			# Perform Search
			try:
				file_pk = self.request.GET.get('id', ResultFile.objects.first().pk)
				file = ResultFile.objects.get(owner=self.request.user.username, pk=file_pk)
				# For bootstrap-table
				table_with_weight = {}
				table_with_weight['filename'] = file.file_name
				table_with_weight['data'] = []

				table_without_weight = {}
				table_without_weight['filename'] = file.file_name
				table_without_weight['data'] = []

				# Iteratively search QueryItem objects
				contents = file.file_content
				for query_item in contents:
					# Generate the table without weight
					if float(query_item.weight) == 0.0:
						 # For bootstrap-table
						table_without_weight['data'].append({
						    'words': query_item.items,
						    'support': query_item.support
						    })

					# Generate the table with weight
					if search(float(query_item.weight), weight_select, float(weight_input)) and \
						search(float(query_item.support), min_support_select, float(min_support_input)) and \
						search(query_item.items, items_select, items_input):
						# Satisfied with the query
						 # For bootstrap-table
						table_with_weight['data'].append({
						    'words': query_item.items,
						    'weight': query_item.weight,
						    'support': query_item.support
						    })
						# raise forms.ValidationError("%s,%s,%s" % (query_item.items, query_item.weight, query_item.support))

				self.cleaned_data['table_with_weight'] = table_with_weight
				self.cleaned_data['table_without_weight'] = table_without_weight
			except ObjectDoesNotExist:
				raise forms.ValidationError('File target does not exist')
		return self.cleaned_data
