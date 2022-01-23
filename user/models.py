from django.db import models
import re
import _datetime
from django.db.models.deletion import DO_NOTHING
from django.db.models.fields.related import create_many_to_many_intermediary_model

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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


class message_comment_manager(models.Manager):
    def message_validator(self, postData):
        error = {}
        if len(postData['content']) < 1:
            error["content"] = "Please enter a message"
        return error

    def comment_validator(self, postData):
        error = {}
        if len(postData['comment']) < 1:
            error["comment"] = "Please enter a comment"
        return error


class Message(models.Model):
    content = models.TextField()
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = message_comment_manager()

    def get_date(self):
        time = _datetime.datetime.today()
        if self.created_at.hour == time.hour:
            return str(time.minute - self.created_at.minute) + " minutes ago"
        if self.created_at.day == time.day:
            return str(time.hour - self.created_at.hour) + " hours ago"
        elif self.created_at.month == time.month:
            return str(time.day - self.created_at.day) + " days ago"
        elif self.created_at.year == time.year:
            return str(time.month - self.created_at.month) + " months ago"
        else:
            return self.created_at


class Comment(models.Model):
    content = models.TextField()
    comment_message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="comments")
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comments")
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = message_comment_manager()

    def get_date(self):
        time = _datetime.datetime.today()
        if self.created_at.hour == time.hour:
            return str(time.minute - self.created_at.minute) + " minutes ago"
        if self.created_at.day == time.day:
            return str(time.hour - self.created_at.hour) + " hours ago"
        elif self.created_at.month == time.month:
            return str(time.day - self.created_at.day) + " days ago"
        elif self.created_at.year == time.year:
            return str(time.month - self.created_at.month) + " months ago"
        else:
            return self.created_at
