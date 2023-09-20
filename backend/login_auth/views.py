from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from djangoproject import settings
from django.core.mail import send_mail
from .forms import SignupForm, SigninForm
# Create your views here.
def home(request):
	title = 'Stock Management Project'
	context = {
	"title": title,
	}
	return render(request, "home.html",context)

def signup(request):
     form = SignupForm(request.POST or None)
     context = {"title": "SIGN UP",
                "form": form,}
     if request.method == "POST":
        

        username = form['username'].value()
        email = form['email'].value()
        pass1 = form['password'].value()
        fname = form['first_name'].value()
        lname = form['last_name'].value()
        
        

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists. Please try another username.")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email address is already registered.")
        elif len(username) > 10:
            messages.error(request, "Username must be 10 characters or less.")
        elif pass1 != pass1:
            messages.error(request, "Passwords do not match.")
        elif not username.isalnum():
            messages.error(request, "Username must be alphanumeric.")
        

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()

        messages.success(request, "Your account is successfully created, we have sent an email")

        return redirect('home')
	
     return render(request, "signup.html",context)

def signin(request):
     form = SigninForm(request.POST or None)
     context = {"title": "SIGN IN",
                "form": form,}
     
     if request.method == "POST":
         username = form['username'].value()
         password = form['password'].value()

         user = authenticate(username=username, password=password)

         if user is not None:
            login(request, user)
            return redirect("home")
         else:
            messages.error(request, "Bad credientials")
            return redirect("home")
        
     return render(request, "signin.html", context)

def signout(request):
    
    logout(request)
    messages.success(request, "Logged out successfully")
    
    return redirect('home')

