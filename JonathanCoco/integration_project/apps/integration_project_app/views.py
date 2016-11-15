from django.shortcuts import render, redirect
from django.contrib.messages import get_messages
from django.core.urlresolvers import reverse


# Create your views here.
def index(request):

    return render(request, 'integration_project_app/index.html')
