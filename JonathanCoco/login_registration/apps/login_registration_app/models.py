from __future__ import unicode_literals
from django.db import models
import re
#import bcrypt
from django.contrib import messages
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')


# Create your models here.

#Our new manager!
  #No methods in our new manager should ever catch the whole request object with a parameter!!! (just parts, like request.POST)
class UserManager(models.Manager):
    def Login(self, email, password, request):
        bLoginSuccessful = True;

        users = User.objects.filter(email = email)
        if len(users) == 0:
            messages.error(request, "User does not exists", extra_tags = "Login")
            return 0
        else:

            if (users[0].password != bcrypt.hashpw(password.encode('utf-8'), users[0].password.encode('utf-8'))):
                messages.error(request, "Invalid Password", extra_tags = "Login")

                return 0

        return users[0]

    def EncryptPassword(self, password):

        password = password.encode('utf-8')
        return bcrypt.hashpw(password, bcrypt.gensalt())


    def IsRegistrationValid(self, first_name, last_name, email, password, confirm_password, request):

        bOK = True

        if ((len(first_name) <=2) or not NAME_REGEX.match(first_name)):
            messages.error(request, "First Name - Alpha characters only and at least 2 characters", extra_tags="Registration")
            bOK = False
        if len(last_name) <=2:
            messages.error(request, "Last Name - Alpha characters only and at least 2 characters", extra_tags="Registration")
            bOK = False
        if len(email) < 1:
            messages.error(request, "Email cannot be blank!", extra_tags="Registration")
            bOK = False
        elif not EMAIL_REGEX.match(email):
            messages.error(request, "Invalid Email Address!", extra_tags="Registration")
            bOK = False

        if (password <> confirm_password ):
            messages.error(request, "Passwords do not match", extra_tags="Registration")
            bOK = False

        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters", extra_tags="Registration")
            bOK = False

        users = User.objects.filter(email = email)
        if len(users) > 0:
            messages.error(request, "User already exists")
            bOK = False

        return bOK


class User(models.Model):
    email = models.CharField(max_length=45)
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    password = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    # *************************
    # Connect an instance of UserManager to our User model overwriting
    # the old hidden objects key with a new one with extra properties!!!
    objects = UserManager()
