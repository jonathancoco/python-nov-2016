from django.shortcuts import render, redirect
from .models import User
from django.contrib.messages import get_messages

# Create your views here.
def index(request):

    return render(request, 'login_registration_app/index.html')

def login(request):

    email = request.POST['login_email']
    password = request.POST['login_password']

    user = User.objects.Login(email, password, request)

    if (user != 0):
        return render(request, 'login_registration_app/success.html', context = {'user':user, 'message':'You have successfully registered'})
    else:
        return render(request, 'login_registration_app/index.html')




def registration(request):

    email = request.POST['email']
    password = request.POST['password']
    confirm_password = request.POST['confirm_password']
    first_name =  request.POST['first_name']
    last_name = request.POST['last_name']


    if (User.objects.IsRegistrationValid(first_name, last_name, email, password, confirm_password, request)):
        user = User(first_name=first_name, last_name=last_name, email=email, password=User.objects.EncryptPassword(password))
        user.save()

        user = User.objects.Login(email, password, request)

        if (user != 0):
            return render(request, 'login_registration_app/success.html', context = {'user':user, 'message':'You have successfully registered'})
    else:
        return render(request, 'login_registration_app/index.html', context={'first_name':first_name, 'last_name':last_name, 'email':email})
