from django.shortcuts import render, redirect
from .models import Product, StockHistory, Category
from .forms import  IssueForm, ReceiveForm, StockHistorySearchForm
from django.contrib import messages
from django.http import HttpResponse
import csv
from django.contrib.auth.decorators import login_required

def stock_detail(request, pk):
	queryset = Product.objects.get(id=pk)
	context = {
		"title": queryset.item_name,
		"queryset": queryset,
	}
	return render(request, "stock_detail.html", context)


def issue_item(request, pk):
	queryset = Product.objects.get(id=pk)
	form = IssueForm(request.POST or None, instance=queryset)

	
	if form.is_valid():
		instance = form.save(commit=False)
		instance.receive_quantity = 0
		instance.quantity -= instance.issue_quantity
		instance.issue_by = str(request.user)
		messages.success(request, "Issued SUCCESSFULLY. \n" + str(instance.quantity) + " " + str(instance.item_name) + "s now left in Store.")
		instance.save()
		issue_history = StockHistory(
			id = instance.id, 
			last_updated = instance.last_updated,
			category_id = instance.category_id,
			item_name = instance.item_name, 
			quantity = instance.quantity, 
			issue_to = instance.issue_to, 
			issue_by = instance.issue_by, 
			issue_quantity = instance.issue_quantity, 
			)
		issue_history.save()
		
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
	queryset = Product.objects.get(id=pk)
	form = ReceiveForm(request.POST or None, instance=queryset)

	if form.is_valid():
		instance = form.save(commit=False)
		instance.issue_quantity = 0
		instance.quantity += instance.receive_quantity
		instance.receive_by = str(request.user)
		instance.save()
		receive_history = StockHistory(
			id = instance.id, 
			last_updated = instance.last_updated,
			category_id = instance.category_id,
			item_name = instance.item_name, 
			quantity = instance.quantity, 
			receive_quantity = instance.receive_quantity, 
			receive_by = instance.receive_by
			)
		receive_history.save()
				
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
		
		queryset = StockHistory.objects.filter(category=form['category'].value(),
										 		item_name__icontains=form['item_name'].value(),
										 		#last_updated__range=[form['start_date'].value(),form['end_date'].value()]
										 	)
	
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

