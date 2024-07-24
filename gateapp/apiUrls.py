# myapp/urls.py
from django.urls import path
from .import APIViews

urlpatterns = [
    path('register/', APIViews.RegisterView.as_view(), name='register'),
    path('login/', APIViews.LoginView.as_view(), name='login'),
]
