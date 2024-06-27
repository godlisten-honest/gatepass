import datetime
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


# Overriding the Default Django Auth
class CustomUser(AbstractUser):
	phone = models.CharField(max_length=10,null=True,blank=True)
	is_deleted = models.BooleanField(default=False)
	deleted_at = models.DateTimeField(null=True,blank=True)

	# def __str__(self) -> str:
    #     		return self.phone

class Report(models.Model):
	id = models.AutoField(primary_key=True)
	user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
	items_json = models.JSONField()
	to = models.CharField(max_length=50)
	descriptions = models.TextField(null=True,blank=True)
	status = models.IntegerField(default=0)
	datetime = models.DateTimeField()
	created_at = models.DateField(auto_now_add=True)
	objects = models.Manager()

	def __str__(self) -> str:
		return self.user_id.phone


class FeedBack(models.Model):
	id = models.AutoField(primary_key=True)
	user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
	feedback = models.TextField()
	feedback_reply = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = models.Manager()
 
	def __str__(self) -> str:
		return self.feedback





