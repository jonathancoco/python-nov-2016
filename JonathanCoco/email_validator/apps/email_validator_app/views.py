from django.shortcuts import render, redirect
from .models import Email

# Create your views here.
def index(request):

    message = ""

    return render(request, 'email_validator_app/index.html', context={'message':message})

def add_email(request):
    print (request.method)

    message = ""

    if (Email.objects.IsEmailValid(request.POST["email"])):

        email = Email(email=request.POST["email"])
        email.save()

        email = Email.objects.all()
        message = "The email address you entered {} is a VALID email address! Thank You".format(request.POST["email"])

        return render(request, 'email_validator_app/success.html', context={'message':message, 'all_emails':email, 'email':request.POST["email"]})
    else:
        message = "{} is Not Valid".format(request.POST["email"])
        return render(request, 'email_validator_app/index.html', context={'message':message})

def delete_email(request):

    print (request.method)

    id = request.POST["resultlist"]


    email = Email.objects.get(id=id)
    email.delete()

    email = Email.objects.all()

    return render(request, 'email_validator_app/success.html', context={'message':'', 'all_emails':email, 'email':''})
