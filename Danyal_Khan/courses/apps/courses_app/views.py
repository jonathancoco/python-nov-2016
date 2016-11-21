from django.shortcuts import render, redirect
from .models import Course

def index(request):
	
	context = {
		"courses" : Course.objects.all()
	}
	
	return render(request, 'index.html', context)


def add(request):
	# name= request.POST['name']
	# description= request.POST['description']

	Course.objects.create(course_name=request.POST['name'], description=request.POST['description'])
	return redirect ('/')

def destroy(request, id):
	context={
		"course" : Course.objects.get(id=id)
	}
	print context['course']
	return render(request, 'courses_app/destroy.html', context)




def remove(request, id):
	Course.objects.filter(id=id).delete()
	return redirect ('/')


	