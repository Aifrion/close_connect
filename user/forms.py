from django import forms
from .models import User
from django.forms import ModelForm


class UploadFileForm(ModelForm):
    class Meta:
        model = User
        fields = ['profile_pic']
