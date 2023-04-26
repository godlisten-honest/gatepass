from multiprocessing import context
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json


from .models import *

def staff_home(request):

	
	return render(request, "staff_template/staff_home_template.html")

def staff_profile(request):
	user = CustomUser.objects.get(id=request.user.id)
	staff = CustomUser.objects.get(admin=user)

	context={
		"user": user,
		"staff": staff
	}
	return render(request, 'staff_template/staff_profile.html', context)


def staff_profile_update(request):
	if request.method != "POST":
		messages.error(request, "Invalid Method!")
		return redirect('staff_profile')
	else:
		first_name = request.POST.get('first_name')
		last_name = request.POST.get('last_name')
		password = request.POST.get('password')
		address = request.POST.get('address')

		try:
			customuser = CustomUser.objects.get(id=request.user.id)
			customuser.first_name = first_name
			customuser.last_name = last_name
			if password != None and password != "":
				customuser.set_password(password)
			customuser.save()

			staff = CustomUser.objects.get(admin=customuser.id)
			staff.address = address
			staff.save()

			messages.success(request, "Profile Updated Successfully")
			return redirect('staff_profile')
		except:
			messages.error(request, "Failed to Update Profile")
			return redirect('staff_profile')



def staff_apply_leave(request):
	print(request.user.id)
	staff_obj = CustomUser.objects.get(id=request.user.id)
	leave_data = Report.objects.filter(user_id=staff_obj)
	context = {
		"leave_data": leave_data
	}
	return render(request, "staff_template/staff_apply_leave_template.html", context)


def staff_apply_leave_save(request):
	if request.method != "POST":
		messages.error(request, "Invalid Method")
		return redirect('staff_apply_leave')
	else:
		leave_date = request.POST.get('leave_date')
		leave_message = request.POST.get('leave_message')

		staff_obj = CustomUser.objects.get(id=request.user.id)
		try:
			leave_report = Report(user_id=staff_obj,
											leave_date=leave_date,
											leave_message=leave_message,
											leave_status=0)
			leave_report.save()
			messages.success(request, "Applied for Leave.")
			return redirect('staff_apply_leave')
		except:
			messages.error(request, "Failed to Apply Leave")
			return redirect('staff_apply_leave')


def staff_feedback(request):
	user_obj = CustomUser.objects.get(id=request.user.id)
	feedback_data = FeedBack.objects.filter(user_id=user_obj)

	context = {
		'feedback_data':feedback_data
	}
	return render(request, "staff_template/staff_feedback_template.html",context)


def staff_feedback_save(request):
	if request.method != "POST":
		messages.error(request, "Invalid Method.")
		return redirect('staff_feedback')
	else:
		feedback = request.POST.get('feedback_message')
		staff_obj = CustomUser.objects.get(id=request.user.id)

		try:
			add_feedback = FeedBack(user_id=staff_obj,
										feedback=feedback,
										feedback_reply="")
			add_feedback.save()
			messages.success(request, "Feedback Sent.")
			return redirect('staff_feedback')
		except:
			messages.error(request, "Failed to Send Feedback.")
			return redirect('staff_feedback')



