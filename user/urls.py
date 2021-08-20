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
    path('dashboard/admin', views.admin_dashboard),
    path('users/show/<int:user_id>', views.show),
    path('users/edit', views.profile),
    path('remove/<int:user_id>', views.remove),
    path('new', views.new),
    path('add', views.add),
    path('users/new', views.new_user)
]