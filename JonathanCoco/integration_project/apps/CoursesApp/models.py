from __future__ import unicode_literals
from django.db import models


# Create your models here.
class Courses(models.Model):
    course_name = models.CharField(max_length=255)
    description_name  = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# Create your models here.
class Comments(models.Model):
    comment_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    Course = models.ForeignKey('Courses', related_name="commentstocourses")
