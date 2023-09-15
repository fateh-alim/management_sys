from django import forms
from .models import UserProfile


class SignupForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ['username', 'first_name', 'last_name', 'email', 'password'] 
		
class SigninForm(forms.Form):
	username = forms.CharField(max_length=10, label='Username')
	password = forms.CharField(widget=forms.PasswordInput, label='password')
		