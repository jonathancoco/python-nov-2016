from __future__ import unicode_literals

from django.db import models
from ..CoursesApp.models import Courses
from ..login_registration_app.models import User


class UserCourse(models.Model):
    user = models.ForeignKey(User)
    course = models.ForeignKey(Courses)
    created_dt = models.DateTimeField(auto_now_add=True)
