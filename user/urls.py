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
    path('dashboard/admin', views.dashboard),
    path('users/show/<int:user_id>', views.show),
    # path('add_message/<int:user_id>/<int:account_id>', views.add_message),
    # path('comment/<int:user_id>/<int:message_id>', views.comment),
    path('update_info', views.update_info),
    path('update_password', views.update_password),
    path('update_description', views.update_description),
    path('users/edit', views.edit),
    path('remove/<int:user_id>', views.remove),
    path('new', views.new),
    path('add', views.add),
    path('users/new', views.new_user),
    path('users/edit/<int:user_id>', views.admin_edit),
    path('update_info/<int:user_id>', views.admin_update_info),
    path('update_password/<int:user_id>', views.admin_update_password)
]