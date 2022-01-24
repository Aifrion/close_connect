from django.db import models
import re
import _datetime
from django.db.models.deletion import DO_NOTHING

# Create your models here.
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class UserManager(models.Manager):
    def register_validator(self, postData):
        error = {}
        if not EMAIL_REGEX.match(postData['email']):
            error["email"] = "Invalid email address"
        if len(postData['first_name']) < 1:
            error["first_name"] = "Please enter a first name"
        if len(postData['last_name']) < 1:
            error["last_name"] = "Please enter a last name "
        if len(postData['password']) < 8:
            error["password"] = "Password needs to be at least 8 characters long"
        if postData['password_check'] != postData['password']:
            error["password"] = "Passwords do not match"
        return error

    def info_validator(self, postData):
        error = {}
        if not EMAIL_REGEX.match(postData['email']):
            error["email"] = "Invalid email address"
        if len(postData['first_name']) < 1:
            error["first_name"] = "Please enter a first name"
        if len(postData['last_name']) < 1:
            error["last_name"] = "Please enter a last name "
        return error

    def password_validator(self, postData):
        error = {}
        if len(postData['password']) < 8:
            error["password"] = "Password needs to be at least 8 characters long"
        if postData['password_check'] != postData['password']:
            error["password"] = "Passwords do not match"
        return error

    def description_validator(self, postData):
        error = {}
        if len(postData['description']) < 1:
            error["description"] = "Description cannot be empty"
        return error


class User(models.Model):
    user_level = models.IntegerField()
    email = models.CharField(max_length=255)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    password = models.CharField(max_length=60)
    description = models.TextField()
    profile_pic = models.ImageField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


class Chat(models.Model):
    room_id = models.CharField(max_length=50, null=True)
    messengers = models.ManyToManyField(User, related_name="chatrooms", null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Message(models.Model):
    content = models.CharField(max_length=10000, null=True)
    sender = models.ForeignKey(User, related_name="message_sends", on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    chat_room = models.ForeignKey(Chat, related_name="messages", on_delete=models.CASCADE, null=True)
