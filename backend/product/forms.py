from django import forms
from .models import Product, Category


class ProductCreateForm(forms.ModelForm):
	class Meta:
		model = Product
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
		
class ProductSearchForm(forms.ModelForm):
   export_to_CSV = forms.BooleanField(required=False)
   class Meta:
     model = Product
     fields = ['category', 'item_name']

class ProductUpdateForm(forms.ModelForm):
	class Meta:
		model = Product
		fields = ['category', 'item_name', 'quantity']
		

class ReorderLevelForm(forms.ModelForm):
	class Meta:
		model = Product
		fields = ['reorder_level']


'''    		for instance in Stock.objects.all():
			 if instance.category == category:
				 raise forms.ValidationError(category + "is already created")'''