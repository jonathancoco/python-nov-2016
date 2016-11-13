from __future__ import unicode_literals
from django.db import models
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


# Create your models here.

#Our new manager!
  #No methods in our new manager should ever catch the whole request object with a parameter!!! (just parts, like request.POST)
class EmailManager(models.Manager):
  def IsEmailValid(self, email):
    bEmailOk = True;

    if len(email) < 1:
        #flash("Email cannot be blank!")
        bEmailOk = False;
    elif not EMAIL_REGEX.match(email):
        #flash("Invalid Email Address!")
        bEmailOk = False;

    return bEmailOk

class Email(models.Model):
  email = models.CharField(max_length=45)
  created_at = models.DateTimeField(auto_now_add = True)
  updated_at = models.DateTimeField(auto_now = True)
  # *************************
  # Connect an instance of UserManager to our User model overwriting
  # the old hidden objects key with a new one with extra properties!!!
  objects = EmailManager()
