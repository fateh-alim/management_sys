from django.shortcuts import render, redirect
from .models import Stock, StockHistory, Category
from .forms import StockCreateForm, StockSearchForm, StockUpdateForm, IssueForm, ReceiveForm, ReorderLevelForm, StockHistorySearchForm
from django.contrib import messages
from django.http import HttpResponse
import csv
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
	title = 'Stock Management Project'
	context = {
	"title": title,
	}
	return render(request, "home.html",context)

@login_required
def list_item(request):
	title = 'List of Items'
	form = StockSearchForm(request.POST or None)
	queryset = Stock.objects.all()
	context = {
		"title": title,
		"queryset": queryset,
		"form": form,
	}
	if request.method == 'POST':
		queryset = Stock.objects.filter(category=form['category'].value(),
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
	return render(request, "list_item.html", context)


@login_required
def add_item(request):
	form = StockCreateForm(request.POST or None)
	if form.is_valid():
		form.save()
		messages.success(request, 'Successfully Saved')
		return redirect('/list_item')
	context = {
		"form": form,
		"title": "Add Items",
	}
	return render(request, "add_item.html", context)

@login_required
def update_item(request, pk):
	queryset = Stock.objects.get(id=pk)
	form = StockUpdateForm(instance=queryset)
	if request.method == 'POST':
		form = StockUpdateForm(request.POST, instance=queryset)
		if form.is_valid():
			form.save()
			messages.success(request, 'Successfully Saved')
			return redirect('/list_item')

	context = {
		'form':form,
		"title": "Update Item Details",
	}
	return render(request, 'add_item.html', context)


def delete_item(request, pk):
	queryset = Stock.objects.get(id=pk)
	if request.method == 'POST':
		queryset.delete()
		messages.success(request, 'Successfully Saved')
		return redirect('/list_item')
	return render(request, 'delete_item.html')

def stock_detail(request, pk):
	queryset = Stock.objects.get(id=pk)
	context = {
		"title": queryset.item_name,
		"queryset": queryset,
	}
	return render(request, "stock_detail.html", context)


def issue_item(request, pk):
	queryset = Stock.objects.get(id=pk)
	form = IssueForm(request.POST or None, instance=queryset)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.receive_quantity = 0
		instance.quantity -= instance.issue_quantity
		instance.issue_by = str(request.user)
		messages.success(request, "Issued SUCCESSFULLY. \n" + str(instance.quantity) + " " + str(instance.item_name) + "s now left in Store.")
		instance.save()

		return redirect('/stock_detail/'+str(instance.id))
		# return HttpResponseRedirect(instance.get_absolute_url())

	context = {
		"title": 'Issue ' + str(queryset.item_name),
		"queryset": queryset,
		"form": form,
		"username": 'Issue By: ' + str(request.user),
	}
	return render(request, "add_item.html", context)



def receive_item(request, pk):
	queryset = Stock.objects.get(id=pk)
	form = ReceiveForm(request.POST or None, instance=queryset)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.issue_quantity = 0
		instance.quantity += instance.receive_quantity
		instance.receive_by = str(request.user)
		instance.save()
		messages.success(request, "Received SUCCESSFULLY. \n" + str(instance.quantity) + " " + str(instance.item_name)+"s now in Store.")

		return redirect('/stock_detail/'+str(instance.id))
		# return HttpResponseRedirect(instance.get_absolute_url())
	context = {
			"title": 'Receive ' + str(queryset.item_name),
			"instance": queryset,
			"form": form,
			"username": 'Receive By: ' + str(request.user),
		}
	return render(request, "add_item.html", context)

def reorder_level(request, pk):
	queryset = Stock.objects.get(id=pk)
	form = ReorderLevelForm(request.POST or None, instance=queryset)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		messages.success(request, "Reorder level for " + str(instance.item_name) + " is updated to " + str(instance.reorder_level))

		return redirect("/list_item")
	context = {
			"instance": queryset,
			"form": form,
		}
	return render(request, "add_item.html", context)

@login_required
def list_history(request):
	title = 'Stock Hisotry'
	form = StockHistorySearchForm(request.POST or None)
	queryset = StockHistory.objects.all()
	context = {
		'form': form,
		"title": title,
		"queryset": queryset,
	}
	if request.method == 'POST':
		category = form['category'].value()
		queryset = StockHistory.objects.filter(category=form['category'].value(),
										 		item_name__icontains=form['item_name'].value(),
										 		last_updated__range=[
																	form['start_date'].value(),
																	form['end_date'].value()
																]
										 	)
		if (category != ''):
			queryset = queryset.filter(category_id=category)
		if form['export_to_CSV'].value() == True:
			response = HttpResponse(content_type='text/csv')
			response['Content-Disposition'] = 'attachment; filename="Stock History.csv"'
			writer = csv.writer(response)
			writer.writerow(
				['CATEGORY', 
				'ITEM NAME',
				'QUANTITY', 
				'ISSUE QUANTITY', 
				'RECEIVE QUANTITY', 
				'RECEIVE BY', 
				'ISSUE BY', 
				'LAST UPDATED'])
			instance = queryset
			for stock in instance:
				writer.writerow(
				[stock.category, 
				stock.item_name, 
				stock.quantity, 
				stock.issue_quantity, 
				stock.receive_quantity, 
				stock.receive_by, 
				stock.issue_by, 
				stock.last_updated])
			return response
		context = {
		"form": form,
		"title": title,
		"queryset": queryset,
		}
	return render(request, "list_history.html",context)

