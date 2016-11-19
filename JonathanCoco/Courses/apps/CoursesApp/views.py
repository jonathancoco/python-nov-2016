from django.shortcuts import render, redirect
from .models import Courses, Comments

# Create your views here.
def index(request):

    courses = Courses.objects.all()

    return render(request, 'CoursesApp/index.html', context={'courses':courses})


def add_course(request):
    print (request.method)

    course = Courses(course_name=request.POST["name"], description_name=request.POST["description"])
    course.save()

    return redirect('/')


def remove_course(request, id):

    course = Courses.objects.get(id=id)
    return render(request, 'CoursesApp/remove.html', context={'course':course})


def delete(request, id):

    course = Courses.objects.get(id=id)
    course.delete()

    return redirect('/')

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

    return redirect('/')

def add_comment(request, id):

    course = Courses.objects.get(id=id)
    comment = Comments(comment_name=request.POST["comment"], Course=course)
    comment.save()

    comments = Comments.objects.filter(Course_id=course.id)

    return render(request, 'CoursesApp/comments.html', context={'course':course, 'comments':comments})




# Create your views here.
