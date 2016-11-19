from django.shortcuts import render, redirect
from .models import User, Book, Reviews
from django.contrib.messages import get_messages

# Create your views here.
def index(request):

    if ('user_id' in request.session) == False:
        return render(request, 'bookreview_app/login.html')
    else:
        user = User.objects.get(id=request.session['user_id'])
        recent_reviews = Reviews.objects.all().order_by('-created_at')[:3]
        reviewed_books = Book.objects.all()

        return render(request, 'bookreview_app/books.html', context = {'user':user, 'recent_reviews':recent_reviews, 'reviewed_books':reviewed_books})


def login(request):

    email = request.POST['login_email']
    password = request.POST['login_password']

    user = User.objects.Login(email, password, request)

    if (user != 0):
        request.session['user_id'] = user.id

        #return render(request, 'bookreview_app/success.html', context = {'user':request.session['user']})
        return redirect('/')
    else:
        return render(request, 'bookreview_app/login.html')




def registration(request):

    email = request.POST['email']
    password = request.POST['password']
    confirm_password = request.POST['confirm_password']
    first_name =  request.POST['first_name']
    last_name = request.POST['last_name']
    birth_date  = request.POST['birth_date']


    if (User.objects.IsRegistrationValid(first_name, last_name, email, birth_date, password, confirm_password, request)):
        user = User(first_name=first_name, last_name=last_name, email=email, birth_date=birth_date, password=User.objects.EncryptPassword(password))
        user.save()

        user = User.objects.Login(email, password, request)

        if (user != 0):
            request.session['user_id'] = user.id
            return redirect('/')
    else:
        return render(request, 'bookreview_app/login.html', context={'first_name':first_name, 'last_name':last_name, 'email':email, 'birth_date':birth_date})


def logout(request):

    try:
        del request.session['user_id']
    except Exception as e:
        pass

    return redirect('/')


def add(request):

    user = User.objects.get(id=request.session['user_id'])
    authors = Book.objects.values('author').distinct()

    return render(request, 'bookreview_app/add_book.html', context = {'user':user, 'authors':authors})


def add_book_review(request):

    user = User.objects.get(id=request.session['user_id'])

    author = ''

    if (request.POST['author'] <> ''):
        author = request.POST['author']
    else:
        author = request.POST['author_list']

    book = Book(title = request.POST['title'], author = author )
    book.save()

    if ((request.POST['review'] <> '') or (request.POST['rating'] <> '')):
        review = Reviews(book=book, user=user, review=request.POST['review'], rating=request.POST['rating'])
        review.save()

    return redirect('/')

def book_reviews(request, id):
    user = User.objects.get(id=request.session['user_id'])
    book = Book.objects.get(id=id)

    return render(request, 'bookreview_app/book_reviews.html', context = {'book':book, 'user':user})

def add_review(request, id):

    user = User.objects.get(id=request.session['user_id'])
    book = Book.objects.get(id=id)

    review = Reviews(book=book, user=user, review=request.POST['review'], rating=request.POST['rating'])
    review.save()

    return redirect('/')

def delete_review(request, id):

    review = Reviews.objects.get(id=id)
    review.delete()

    return redirect('/')


def user(request, id):

    user = User.objects.get(id=id)

    return render(request, 'bookreview_app/user.html', context = {'user':user})

    return redirect('/')
