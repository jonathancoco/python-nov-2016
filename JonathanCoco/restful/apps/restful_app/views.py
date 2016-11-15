from django.shortcuts import render, redirect
from .models import Products

# Create your views here.

def index(request):

    if request.method == "POST":
        product = Products(name = request.POST['name'], description=request.POST['description'], price=request.POST['price'])
        product.save()

    products = Products.objects.all()
    return render(request, 'restful_app/index.html', context={'products':products})

def new(request):

    return render(request, 'restful_app/new_product.html')


def show(request, id):

    product = Products.objects.get(id=id)
    return render(request, 'restful_app/show_product.html', context={'product':product})



def delete(request, id):

    product = Products.objects.get(id=id)
    product.delete()
    return redirect('/products')


def edit(request, id):

    product = Products.objects.get(id=id)
    return render(request, 'restful_app/edit_product.html', context={'product':product})

def update(request, id):

    product = Products.objects.get(id=id)

    product.name = request.POST['name']
    product.description = request.POST['description']
    product.price = request.POST['price']

    product.save()

    return redirect('/products')
