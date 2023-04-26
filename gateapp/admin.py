from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

# Register your models here.
class UserModel(UserAdmin):
	pass


admin.site.register(CustomUser, UserModel)

admin.site.register(Report)
admin.site.register(FeedBack)