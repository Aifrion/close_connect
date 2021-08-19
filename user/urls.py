from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('start', views.start),
    path('sign_in', views.sign_in),
    path('login', views.login),
    path('create', views.create),
    path('register', views.register),
    path('check_admin', views.check_admin)
]