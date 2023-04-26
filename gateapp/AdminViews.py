from cmath import phase
from django.contrib.auth.models import User,auth,Permission,Group
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
import datetime
import json

# from .forms import AddStudentForm, EditStudentForm

from .models import *


def admin_home(request):
	

	return render(request, "hod_template/home_content.html")

###############################################################################################
########################## ------- USER PROFILE ---------------################################

def admin_profile(request):
	user = CustomUser.objects.get(id=request.user.id)

	context={
		"user": user
	}
	return render(request, 'hod_template/admin_profile.html', context)


def admin_profile_update(request):
	if request.method != "POST":
		messages.error(request, "Invalid Method!")
		return redirect('admin_profile')
	else:
		first_name = request.POST.get('first_name')
		last_name = request.POST.get('last_name')
		password = request.POST.get('password')

		try:
			customuser = CustomUser.objects.get(id=request.user.id)
			customuser.first_name = first_name
			customuser.last_name = last_name
			if password != None and password != "":
				customuser.set_password(password)
			customuser.save()
			messages.success(request, "Profile Updated Successfully")
			return redirect('admin_profile')
		except:
			messages.error(request, "Failed to Update Profile")
			return redirect('admin_profile')

########################################################################################
############ ------------- USER MANAGEMENT FUNCTION ------------ #######################

def add_staff(request):
	return render(request, "hod_template/add_staff_template.html")


def add_staff_save(request):
	if request.method != "POST":
		messages.error(request, "Invalid Method ")
		return redirect('add_staff')
	else:
		first_name = request.POST.get('first_name')
		last_name = request.POST.get('last_name')
		username = request.POST.get('username')
		email = request.POST.get('email')
		password = request.POST.get('password')
		phone = request.POST.get('phone')

		try:
			user = CustomUser.objects.create_user(username=username,
												password=password,
												email=email,
												first_name=first_name,
												last_name=last_name,
												phone = phone)
			user.save()
			messages.success(request, "Staff Added Successfully!")
			return redirect('add_staff')
		except:
			messages.error(request, "Failed to Add Staff!")
			return redirect('add_staff')



def manage_staff(request):
	staffs = CustomUser.objects.all().filter(is_deleted='False',is_staff='False')
	context = {
		"staffs": staffs
	}
	return render(request, "hod_template/manage_staff_template.html", context)


def edit_staff(request, staff_id):
	staff = CustomUser.objects.get(id=staff_id)

	context = {
		"staff": staff,
		"id": staff_id
	}
	return render(request, "hod_template/edit_staff_template.html", context)


def edit_staff_save(request):
	if request.method != "POST":
		return HttpResponse("<h2>Method Not Allowed</h2>")
	else:
		staff_id = request.POST.get('staff_id')
		username = request.POST.get('username')
		email = request.POST.get('email')
		first_name = request.POST.get('first_name')
		last_name = request.POST.get('last_name')
		phone = request.POST.get('phone')
		password = request.POST.get('password')

		try:
			# INSERTING into Customuser Model
			user = CustomUser.objects.get(id=staff_id)
			user.first_name = first_name
			user.last_name = last_name
			user.email = email
			user.username = username
			user.phone = phone
			if password != None and password != "":
				user.set_password(password)
			user.save()
			
			# INSERTING into Staff Model

			messages.success(request, "Staff Updated Successfully.")
			return redirect('/edit_staff/'+staff_id)

		except:
			messages.error(request, "Failed to Update Staff.")
			return redirect('/edit_staff/'+staff_id)

def grant_role(request,staff_id):
	role = Group.objects.all()
	staff = CustomUser.objects.get(id=staff_id)
	
	context = {
		'role':role,
		'staff':staff,
		'id':staff_id
	}
	return render(request, 'hod_template/grant_role.html',context)

def grant_role_save(request):
	if request.method != 'POST':
		messages.error(request,'Invalid Method')
		return redirect('grant_role')
	else:
		role = Group.objects.all()
		staff_id = request.POST.get('staff_id')
		staff = CustomUser.objects.get(id=staff_id)

		try:
			for role in Group.objects.all():
				staff.groups.remove(role.id)

			for j in Permission.objects.all():
				staff.user_permissions.remove(j.id)

			group = [x.name for x in Group.objects.all()]
			s_id = []

			for x in group:
				s_id.append(int(request.POST.get(x))) if request.POST.get(x) else print("")

			for s in s_id:
				staff.groups.add(Group.objects.get(id=s))

			messages.success(request, "Role Granted Successfully!")
			return redirect('/grant_role/'+staff_id)
		except:
			messages.error(request, "Failed to Grant role")
			return redirect('/grant_role/'+staff_id)

def delete_staff(request, staff_id):
	staff = CustomUser.objects.filter(id=staff_id)
	date = datetime.datetime.now()
	try:
		staff.update(is_deleted='True',is_active='False',deleted_at=date)
		messages.success(request, "Staff Deleted Successfully.")
		return redirect('manage_staff')
	except:
		messages.error(request, "Failed to Delete Staff.")
		return redirect('manage_staff')


def staff_trash(request):
	staffs = CustomUser.objects.all().filter(is_deleted='True',is_active='False')
	
	context = {
		"staffs":staffs
	}
	return render(request,"hod_template/staff_trash.html",context)

def staff_restore(request,staff_id):
	staff = CustomUser.objects.filter(id=staff_id)
	try:
		staff.update(is_deleted='False',is_active='True')
		messages.success(request, "Staff Restored Successfully.")
		return redirect('staff_trash')
	except:
		messages.error(request, "Failed to Restore Staff.")
		return redirect('staff_trash')

def permanent_delete(request, staff_id):
	staff = CustomUser.objects.get(id=staff_id)
	try:
		staff.delete()
		messages.success(request, "Staff Permanent Deleted Successfully.")
		return redirect('staff_trash')
	except:
		messages.error(request, "Failed to Delete Staff.")
		return redirect('staff_trash')

###############################################################################################
############################### --------- ROLES FUNCTION ------- ##############################

def manage_role(request):
	role = Group.objects.all()
	rp = ContentType.objects.get_for_model(Report)
	fd = ContentType.objects.get_for_model(FeedBack)
	permission = Permission.objects.filter(Q(content_type=rp) | Q(content_type=fd))
	
	context = {
		'role':role,
		'permission':permission
	}
	return render(request,'hod_template/manage_role.html',context)

def add_role(request):
	rp = ContentType.objects.get_for_model(Report)
	fd = ContentType.objects.get_for_model(FeedBack)
	permission = Permission.objects.filter(Q(content_type=rp) | Q(content_type=fd))

	context = {
		'permission':permission
	}
	return render(request,'hod_template/add_role.html',context)

def add_role_save(request):
	if request.method != "POST":
		messages.error(request, "Invalid Method ")
		return redirect('add_role')
	else:
		role_name = request.POST.get('name')
		role = Group()

		try:
			permission = [perm.name for perm in Permission.objects.all()]
			s_id = []
			role.name = role_name

			for perm in permission:
				if request.POST.get(perm):
					s_id.append(int(request.POST.get(perm)))
				else:
					print("")
				# s_id.append(int(request.POST.get(x))) if request.POST.get(x) else print("")
			role.save()

			for s in s_id:
				role.permissions.add(Permission.objects.get(id=s)) 

			messages.success(request, "Role Added Successfully!")
			return redirect('add_role')
		except:
			messages.error(request, "Failed to Add role")
			return redirect('add_role')

def edit_role(request,role_id):
	role = Group.objects.get(id=role_id)
	rp = ContentType.objects.get_for_model(Report)
	fd = ContentType.objects.get_for_model(FeedBack)
	permission = Permission.objects.filter(Q(content_type=rp) | Q(content_type=fd))

	context = {
		'role':role,
		'permission':permission,
		'id':role_id
	}
	return render(request,'hod_template/edit_role.html',context)

def edit_role_save(request):
	if request.method != 'POST':
		messages.error(request, "Invalid Method ")
		return redirect('edit_role')
	else:
		role_id = request.POST.get('role_id')
		name = request.POST.get('name')
		role = Group.objects.get(id=role_id)

		try:
			for j in Permission.objects.all():
				role.permissions.remove(j.id)

			permission = [perm.name for perm in Permission.objects.all()]
			s_id = []

			for perm in permission:
				if request.POST.get(perm):
					s_id.append(int(request.POST.get(perm)))
				else:
					print("")
			Group.objects.filter(id=role_id).update(name=name)

			for s in s_id:
				role.permissions.add(Permission.objects.get(id=s)) 

			messages.success(request, "Role Edited Successfully!")
			return redirect('/edit_role/'+role_id)

		except:
			messages.error(request, "Failed to Edit role")
			return redirect('/edit_role/'+role_id)

def delete_role(request,role_id):
	role = Group.objects.get(id=role_id)

	try:
		role.delete()
		messages.success(request, "Role Deleted Successfully.")
		return redirect('manage_role')
	except:
		messages.error(request, "Failed to Delete Role.")
		return redirect('smanage_role')




##############################################################################################
############################# ---------- REPORT MANAGEMENT ------ ############################

def staff_leave_view(request):
	leaves = Report.objects.all()
	context = {
		"leaves": leaves
	}
	return render(request, 'hod_template/staff_leave_view.html', context)


def staff_leave_approve(request, leave_id):
	leave = Report.objects.get(id=leave_id)
	leave.status = 1
	leave.save()
	return redirect('staff_leave_view')


def staff_leave_reject(request, leave_id):
	leave = Report.objects.get(id=leave_id)
	leave.status = 2
	leave.save()
	return redirect('staff_leave_view')	


def staff_profile(request):
	pass


###############################################################################################
############################## ---------- FEEDBACK FUNCTION ------ ############################

def staff_feedback_message(request):
	feedbacks = FeedBack.objects.all()
	context = {
		"feedbacks": feedbacks
	}
	return render(request, 'hod_template/staff_feedback_template.html', context)


@csrf_exempt
def staff_feedback_message_reply(request):
	feedback_id = request.POST.get('id')
	feedback_reply = request.POST.get('reply')

	try:
		feedback = FeedBack.objects.get(id=feedback_id)
		feedback.feedback_reply = feedback_reply
		feedback.save()
		return HttpResponse("True")

	except:
		return HttpResponse("False")


@csrf_exempt
def check_email_exist(request):
	email = request.POST.get("email")
	user_obj = CustomUser.objects.filter(email=email).exists()
	if user_obj:
		return HttpResponse(True)
	else:
		return HttpResponse(False)


@csrf_exempt
def check_username_exist(request):
	username = request.POST.get("username")
	user_obj = CustomUser.objects.filter(username=username).exists()
	if user_obj:
		return HttpResponse(True)
	else:
		return HttpResponse(False)
