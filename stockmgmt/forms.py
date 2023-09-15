from django import forms
from .models import  StockHistory
from products.models import Category, Products

class StockCreateForm(forms.ModelForm):
	class Meta:
		model = Products
		fields = ['category', 'item_name', 'quantity']

	def clean_category(self):
		category = self.cleaned_data.get('category')
		if not category:
			raise forms.ValidationError('This field is required')
		return category


	def clean_item_name(self):
		item_name = self.cleaned_data.get('item_name')
		if not item_name:
			raise forms.ValidationError('This field is required')
		return item_name
	
class CategoryCreateForm(forms.ModelForm):
	class Meta:
		model = Category
		fields = ['name']
		
class StockSearchForm(forms.ModelForm):
   export_to_CSV = forms.BooleanField(required=False)
   class Meta:
     model = Products
     fields = ['category', 'item_name']

class StockHistorySearchForm(forms.ModelForm):
	export_to_CSV = forms.BooleanField(required=False)
	start_date = forms.DateTimeField(required=False)
	end_date = forms.DateTimeField(required=False)
	class Meta:
		model = StockHistory
		fields = ['category', 'item_name', 'start_date', 'end_date']
	
class StockUpdateForm(forms.ModelForm):
	class Meta:
		model = Products
		fields = ['category', 'item_name', 'quantity']
		
class IssueForm(forms.ModelForm):
	class Meta:
		model = Products
		fields = ['issue_quantity', 'issue_to']


class ReceiveForm(forms.ModelForm):
	class Meta:
		model = Products
		fields = ['receive_quantity', 'receive_by']

class ReorderLevelForm(forms.ModelForm):
	class Meta:
		model = Products
		fields = ['reorder_level']


'''    		for instance in Stock.objects.all():
			 if instance.category == category:
				 raise forms.ValidationError(category + "is already created")'''