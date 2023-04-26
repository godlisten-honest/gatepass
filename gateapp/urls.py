from django.contrib import admin
from django.urls import path, include
from . import views
from .import AdminViews, StaffViews

urlpatterns = [
	# path('admin/', admin.site.urls),
	# path('', views.home, name="home"),
	path('contact', views.contact, name="contact"),
	path('', views.loginUser, name="login"),
	path('logout_user', views.logout_user, name="logout_user"),
	path('doLogin', views.doLogin, name="doLogin"),
	

	##################################################################################################
	############################ ------ URL FOR STAFF MANAGEMENT ----------- #########################

	path('staff_home/', StaffViews.staff_home, name="staff_home"),
	path('staff_apply_leave/', StaffViews.staff_apply_leave, name="staff_apply_leave"),
	path('staff_apply_leave_save/', StaffViews.staff_apply_leave_save, name="staff_apply_leave_save"),
	path('staff_feedback/', StaffViews.staff_feedback, name="staff_feedback"),
	path('staff_feedback_save/', StaffViews.staff_feedback_save, name="staff_feedback_save"),
	path('staff_profile/', StaffViews.staff_profile, name="staff_profile"),
	path('staff_profile_update/', StaffViews.staff_profile_update, name="staff_profile_update"),
	
	##################################################################################################
	############################ ------ URL FOR ADMIN MANAGEMENT ----------- #########################
	
	# for profile
	path('admin_home/', AdminViews.admin_home, name="admin_home"),
	path('admin_profile/', AdminViews.admin_profile, name="admin_profile"),
	path('admin_profile_update/', AdminViews.admin_profile_update, name="admin_profile_update"),

	# for staff manaegement
	path('add_staff/', AdminViews.add_staff, name="add_staff"),
	path('add_staff_save/', AdminViews.add_staff_save, name="add_staff_save"),
	path('manage_staff/', AdminViews.manage_staff, name="manage_staff"),
	path('edit_staff/<staff_id>/', AdminViews.edit_staff, name="edit_staff"),
	path('edit_staff_save/', AdminViews.edit_staff_save, name="edit_staff_save"),
	path('grant_role/<staff_id>/',AdminViews.grant_role, name="grant_role"),
	path('grant_role_save/',AdminViews.grant_role_save, name="grant_role_save"),
	path('delete_staff/<staff_id>/', AdminViews.delete_staff, name="delete_staff"),

	# for role management
	path('manage_role/',AdminViews.manage_role, name="manage_role"),
	path('add_role/',AdminViews.add_role, name="add_role"),
	path('add_role_save/',AdminViews.add_role_save,name="add_role_save"),
	path('edit_role/<role_id>/',AdminViews.edit_role, name="edit_role"),
	path('edit_role_save/',AdminViews.edit_role_save, name="edit_role_save"),
	path('delete_role/<role_id>/',AdminViews.delete_role, name="delete_role"),

	# for trash
	path('staff_trash/',AdminViews.staff_trash, name="staff_trash"),
	path('staff_restore/<staff_id>/',AdminViews.staff_restore, name="staff_restore"),
	path('permanent_delete/<staff_id>/',AdminViews.permanent_delete, name="permanent_delete"),

	# for validations
	path('check_email_exist/', AdminViews.check_email_exist, name="check_email_exist"),
	path('check_username_exist/', AdminViews.check_username_exist, name="check_username_exist"),

	# for feedbacks
	path('staff_feedback_message/', AdminViews.staff_feedback_message, name="staff_feedback_message"),
	path('staff_feedback_message_reply/', AdminViews.staff_feedback_message_reply, name="staff_feedback_message_reply"),
	
	#for reports
	path('staff_leave_view/', AdminViews.staff_leave_view, name="staff_leave_view"),
	path('staff_leave_approve/<leave_id>/', AdminViews.staff_leave_approve, name="staff_leave_approve"),
	path('staff_leave_reject/<leave_id>/', AdminViews.staff_leave_reject, name="staff_leave_reject"),

	
]
