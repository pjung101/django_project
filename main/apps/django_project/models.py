from __future__ import unicode_literals
from django.db import models
import bcrypt
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$")
BIRTHDAY_REGEX = re.compile(r"^\d{4}[-/]\d{2}[-/]\d{2}")

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 1:
            errors['first_name'] = "First Name cannot be blank"
        elif len(postData['first_name']) < 2:
            errors['first_name'] = "First Name must be at least 2 characters long"
        elif postData['first_name'].isalpha == False:
            errors['first_name'] = "First Name cannot contain numbers"
        if len(postData['last_name']) < 1:
            errors['last_name'] = "Last Name cannot be blank"
        elif len(postData['last_name']) < 2:
            errors['last_name'] = "Last Name must be at least 2 characters long"
        elif postData['last_name'].isalpha == False:
            errors['last_name'] = "Last Name cannot contain numbers"
        if len(postData['email']) < 1:
            errors['email'] = "Email cannot be blank"
        elif not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Email is not valid"
        elif len(User.objects.filter(email = postData['email'])) == 1:
            errors['email'] = "Email already exists"
        if len(postData['password']) < 1:
            errors['password'] = "Password cannot be blank"
        elif not PASSWORD_REGEX.match(postData['password']):
            errors['password'] = "Password must have one capital, one number, and be at least 8 characters"
        elif postData['password'] != postData['confirm']:
            errors['confirm'] = "Password does not match"
        return errors
    def login_validator(self,postData):
        errors = {}
        if len(postData['lemail']) < 1:
            errors['lemail'] = "Invalid Email"
        elif not User.objects.filter(email=postData['lemail']):
            errors['lemail'] = "Email does not exist"
        if User.objects.filter(email=postData['lemail']):
            if not bcrypt.checkpw(postData['lpassword'].encode(), User.objects.get(email=postData['lemail']).password.encode()):
                errors['lpassword'] = "Invalid Password"
        return errors
    def wish_validator(self,postData):
        errors = {}
        if len(postData['item']) < 1:
            errors['item'] = "A wish must be provided!"
        elif len(postData['item']) < 3:
            errors['item'] = "A wish must consist of at least 3 characters!"
        if len(postData['desc']) < 1:
            errors['desc'] = "A description must be provided!"
        elif len(postData['desc']) < 3:
            errors['desc'] = "The description must be at least 3 characters!"
        return errors
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects =  UserManager()
class Wish(models.Model):
    item = models.TextField()
    desc = models.TextField()
    user = models.ForeignKey(User, related_name='wishes')
    granted = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
class Like(models.Model):
    user = models.ForeignKey(User, related_name='likes')
    wish = models.ForeignKey(Wish, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

