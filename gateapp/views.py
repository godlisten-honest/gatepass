from django.shortcuts import render,HttpResponse, redirect,HttpResponseRedirect
from django.contrib.auth import logout, authenticate, login
from .models import *
from django.contrib import messages

def home(request):
	return render(request, 'home.html')


def contact(request):
	return render(request, 'contact.html')


def loginUser(request):
	return render(request, 'login_page.html')

def doLogin(request):
	
	print("here")
	email_id = request.POST.get('username')
	password = request.POST.get('password')
	# user_type = request.GET.get('user_type')
	print(email_id)
	print(password)
	print(request.user)
	if not (email_id and password):
		messages.error(request, "Please provide all the details!!")
		return render(request, 'login_page.html')

	user =authenticate(username=email_id, password=password)
	if not user:
		messages.error(request, 'Invalid Login Credentials!!')
		return render(request, 'login_page.html')

	login(request, user)
	print(request.user)

	if user.is_staff == True:
		return redirect('admin_home/')
	elif user.is_active == True:
		return redirect('staff_home/')


	
def logout_user(request):
	logout(request)
	return HttpResponseRedirect('/')

