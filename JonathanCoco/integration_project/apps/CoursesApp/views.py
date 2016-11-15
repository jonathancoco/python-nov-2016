from django.shortcuts import render, redirect
from .models import Courses, Comments
from ..login_registration_app.models import User
from ..integration_project_app.models import UserCourse
from django.core.urlresolvers import reverse

# Create your views here.
def index(request):

    courses = Courses.objects.all()

    return render(request, 'CoursesApp/index.html', context={'courses':courses})


def add_course(request):
    print (request.method)

    course = Courses(course_name=request.POST["name"], description_name=request.POST["description"])
    course.save()

    return redirect(reverse('courses:index'))


def remove_course(request, id):

    course = Courses.objects.get(id=id)
    return render(request, 'CoursesApp/remove.html', context={'course':course})


def delete(request, id):

    course = Courses.objects.get(id=id)
    course.delete()

    return redirect('/courses')

def edit_course(request, id):

    course = Courses.objects.get(id=id)
    return render(request, 'CoursesApp/edit.html', context={'course':course})

def view_comments(request, id):

    course = Courses.objects.get(id=id)
    comments = Comments.objects.filter(Course_id=id)

    return render(request, 'CoursesApp/comments.html', context={'course':course, 'comments':comments})


def save_course(request, id):

    course = Courses.objects.get(id=id)

    course.course_name = request.POST["name"]
    course.description_name = request.POST["description"]


    course.save()

    return redirect(reverse('courses:index'))

def add_comment(request, id):

    course = Courses.objects.get(id=id)
    comment = Comments(comment_name=request.POST["comment"], Course=course)
    comment.save()

    comments = Comments.objects.filter(Course_id=course.id)

    return render(request, 'CoursesApp/comments.html', context={'course':course, 'comments':comments})

# Create your views here.
def view_user_courses(request):

    courses = Courses.objects.all()
    users = User.objects.all()
    user_courses = UserCourse.objects.all()

    return render(request, 'CoursesApp/user_courses.html', context = { 'users':users, 'courses':courses, 'user_courses':user_courses})

def add_user_course(request):

    user = User.objects.get(id=request.POST['user_select'])
    course = Courses.objects.get(id=request.POST['course_select'])
    user_course = UserCourse(user=user, course=course)
    user_course.save()

    return redirect(reverse('courses:view_user_courses'))

def delete_user_course(request, id):

    user_course = UserCourse.objects.get(id=id)
    user_course.delete()

    return redirect(reverse('courses:view_user_courses'))





# Create your views here.
