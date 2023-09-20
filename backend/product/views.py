from django.shortcuts import render, redirect
from .models import Product, Category
from .forms import ProductCreateForm, ProductSearchForm, ProductUpdateForm, ReorderLevelForm, CategoryCreateForm
from django.contrib import messages
from django.http import HttpResponse
import csv
from django.contrib.auth.decorators import login_required

# Create your views here.
def add_category(request):
	form = CategoryCreateForm(request.POST or None)
	if form.is_valid():
		form.save()
		messages.success(request, 'Successfully Created')
		return redirect('/list_products')
	context = {
		"form": form,
		"title": "Add Category",
	}
	return render(request, "add_item.html", context)

@login_required
def list_products(request):
	title = 'List of Products'
	form = ProductSearchForm(request.POST or None)
	queryset = Product.objects.all()
	context = {
		"title": title,
		"queryset": queryset,
		"form": form,
	}
	if request.method == 'POST':
		queryset = Product.objects.filter(category=form['category'].value(),
										item_name__icontains=form['item_name'].value()
										)
				
		if form['export_to_CSV'].value() == True:
			response = HttpResponse(content_type='text/csv')
			response['Content-Disposition'] = 'attachment; filename="List of stock.csv"'
			writer = csv.writer(response)
			writer.writerow(['CATEGORY', 'ITEM NAME', 'QUANTITY'])
			instance = queryset
			for stock in instance:
				writer.writerow([stock.category, stock.item_name, stock.quantity])
			return response
		
		context = {
		"form": form,
		"title": title,
		"queryset": queryset,
		}
	return render(request, "list_products.html", context)


@login_required
def add_item(request):
	form = ProductCreateForm(request.POST or None)
	if form.is_valid():
		form.save()
		messages.success(request, 'Successfully Saved')
		return redirect('/list_products')
	context = {
		"form": form,
		"title": "Add Items",
	}
	return render(request, "add_item.html", context)

@login_required
def update_item(request, pk):
	queryset = Product.objects.get(id=pk)
	form = ProductUpdateForm(instance=queryset)
	if request.method == 'POST':
		form = ProductUpdateForm(request.POST, instance=queryset)
		if form.is_valid():
			form.save()
			messages.success(request, 'Successfully Saved')
			return redirect('/list_products')

	context = {
		'form':form,
		"title": "Update Product Details",
	}
	return render(request, 'add_item.html', context)


def delete_item(request, pk):
	queryset = Product.objects.get(id=pk)
	if request.method == 'POST':
		queryset.delete()
		messages.success(request, 'Successfully Saved')
		return redirect('/list_products')
	return render(request, 'delete_item.html')

def reorder_level(request, pk):
	queryset = Product.objects.get(id=pk)
	form = ReorderLevelForm(request.POST or None, instance=queryset)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		messages.success(request, "Reorder level for " + str(instance.item_name) + " is updated to " + str(instance.reorder_level))

		return redirect("/list_products")
	context = {
			"instance": queryset,
			"form": form,
		}
	return render(request, "add_item.html", context)
