from django.urls import path
from . import views

urlpatterns = [
    path('home', views.home),
    path('', views.index),
    path('start', views.start),
    path('logout', views.logout),
    path('sign_in', views.sign_in),
    path('login', views.login),
    path('create', views.create),
    path('register', views.register),
    path('check_admin', views.check_admin),
    path('dashboard', views.dashboard),
    path('dashboard/admin', views.admin_dashboard)
]