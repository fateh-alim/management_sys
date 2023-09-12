from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.
def home(request):
	title = 'Stock Management Project'
	context = {
	"title": title,
	}
	return render(request, "home.html",context)


