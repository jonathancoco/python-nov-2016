from django.shortcuts import render, redirect
from .models import User, Property
from django.db.models import Q, Count
from django.contrib.messages import get_messages
import googlemaps
import requests
import urllib
from xml.etree import ElementTree as ET
from decimal import *



# Create your views here.
def index(request):

    if ('user_id' in request.session) == True:
        user = User.objects.get(id=request.session['user_id'])
    else:
        user = 0

    return render(request, 'property_search_app/index.html', context = {'user':user})

def view_search(request):

    if ('user_id' in request.session) == False:
        return render(request, 'property_search_app/login.html')
    else:
        user = User.objects.get(id=request.session['user_id'])
        all_property = Property.objects.all()[:20]

        return render(request, 'property_search_app/search.html', context = {'user':user})

def view_login(request):

    return render(request, 'property_search_app/login.html')


def contact(request):

    return render(request, 'property_search_app/contact_us.html')



def search(request):

    global search_results

    #search = request.POST['search_criteria']

    #result = Contact.objects.filter(last_name__icontains=request.POST['query']) | Contact.objects.filter(first_name__icontains=request.POST['query']

    property_id = request.POST['property_id']
    geo_id = request.POST['geo_id']
    owner_name = request.POST['owner_name']
    dba_name = request.POST['dba_name']
    street_number = request.POST['street_number']
    street_name = request.POST['street_name']

    q = Q()

    if property_id <> '':
        q &= Q(prop_id=property_id)

    if geo_id <> '':
        q &= Q(geo_id=geo_id)

    if owner_name <> '':
        q &= Q(owner_name__icontains=owner_name)

    if street_number <> '':
        q &= Q(situs_num=street_number)

    if street_name <> '':
        q &= Q(situs_street__icontains=street_name)

    user = User.objects.get(id=request.session['user_id'])
    #search_results = Property.objects.filter(Q(owner_name__icontains=request.POST['search_criteria']) | Q(situs_display__icontains=request.POST['search_criteria']) | Q(dba_name__icontains=request.POST['search_criteria']))


    search_results = Property.objects.filter(q)

    #search_results = Property.objects.filter(prop_id=22222, owner_name__icontains='Johnson')

    request.session['num_pages'] = len(search_results)/10
    request.session['current_page'] = 1

    if request.session['num_pages'] <= 10:
        end_page = int(request.session['num_pages'])
    else:
        end_page = 10

    request.session['start_page'] = 1
    request.session['end_page'] = end_page

    sorted_list = sorted(search_results, key=lambda o: (o.owner_name, o.market))

    return render(request, 'property_search_app/search_results.html', context = {'user':user, 'property_search_results':sorted_list[:10], 'pages':range(1, end_page+1)})

def view_search_results(request, id):


    user = User.objects.get(id=request.session['user_id'])

    id = int(id)

    if (id > int(request.session['start_page'])) and (id < int(request.session['end_page'])):
        pass;
    else:
        if (id > 1):
            request.session['start_page'] = id - 1
        else:
            request.session['start_page'] = 1
        request.session['end_page'] = int(id) + 9

    if request.session['end_page'] > request.session['num_pages']:
        request.session['end_page'] = request.session['num_pages']

    request.session['current_page'] = id

    if request.session['sort'] == "name":
        sorted_list = sorted(search_results, key=lambda o: (o.owner_name, o.market))
    elif request.session['sort'] == "address":
        sorted_list = sorted(search_results, key=lambda o: (o.situs_street, o.situs_num))
    else:
        sorted_list = sorted(search_results, key=lambda o: (o.market))


    return render(request, 'property_search_app/search_results.html', context = {'user':user, 'property_search_results':sorted_list[(int(id)-1)*10:(int(id)-1)*10+10], 'pages':range(int(request.session['start_page']), int(request.session['end_page']+1))})


def view_property(request, id):

    property = Property.objects.filter(prop_id=id)

    #get geolocation
    gmaps = googlemaps.Client(key='AIzaSyCSSM8SAfdieagJmf6m1zQ4TbSb14JDjFA')
    geocode_result = gmaps.geocode(property[0].situs_display)

    #url = "http://www.zillow.com/webservice/GetSearchResults.htm?zws-id=X1-ZWz19k0a4so6x7_75222&address=2114+Bigelow+Ave&citystatezip=Seattle%2C+WA"

    #get zillow value
    url = "http://www.zillow.com/webservice/GetSearchResults.htm?zws-id=X1-ZWz19k0a4so6x7_75222&address={}+{}&citystatezip={}+{}+{}".format(property[0].situs_num, property[0].situs_street, property[0].situs_city, property[0].situs_state, property[0].situs_zip)

    zillow = requests.get(url)
    root = ET.fromstring(zillow.content)
    iter_ = root.getiterator()

    zEstimate = Decimal('0.0')
    zEstimate_diff = Decimal('0.0')
    mlsEstimate = Decimal('0.0')
    mlsEstimate_diff = Decimal('0.0')
    dfwEstimate = Decimal('0.0')
    dfwEstimate_diff = Decimal('0.0')

    for elem in iter_:
        if elem.tag == "amount":
            try:
                zEstimate = int(elem.text)
            except Exception as e:
                zEstimate = 0


    zEstimate_diff = zEstimate - property[0].market
    dfwEstimate = property[0].market * Decimal('0.80')
    dfwEstimate_diff = dfwEstimate - property[0].market
    mlsEstimate = property[0].market * Decimal('1.05')
    mlsEstimate_diff = mlsEstimate - property[0].market

    message = ''

    if dfwEstimate < property[0].market:
        message = "You could save approximately ${0:.2f} on your tax bill. Please contact us so that we can save you money!".format(((property[0].market - dfwEstimate)/100)*Decimal('2.5'))

    print message


    user = User.objects.get(id=request.session['user_id'])


    return render(request, 'property_search_app/view_property.html', context = {'property':property[0],'geocode':geocode_result[0]['geometry']['location'], 'zEstimate':zEstimate, 'zEstimate_diff':zEstimate_diff, 'mlsEstimate':mlsEstimate, 'mlsEstimate_diff':mlsEstimate_diff, 'dfwEstimate':dfwEstimate, 'dfwEstimate_diff':dfwEstimate_diff, 'message':message, 'user':user})



def sort_list(request, sort_option):

    request.session['sort'] = sort_option

    return redirect('/view_search_results/1')





def login(request):

    email = request.POST['login_email']
    password = request.POST['login_password']

    user = User.objects.Login(email, password, request)

    if (user != 0):
        request.session['user_id'] = user.id
        request.session['num_pages'] = 0
        request.session['current_page'] = 0
        request.session['start_page'] = 0
        request.session['end_page'] = 0
        request.session['search_criteria'] =''
        request.session['sort'] = 'name'

        #return render(request, 'bookreview_app/success.html', context = {'user':request.session['user']})
        return redirect('/')
    else:
        return render(request, 'property_search_app/login.html')




def registration(request):

    email = request.POST['email']
    password = request.POST['password']
    confirm_password = request.POST['confirm_password']
    first_name =  request.POST['first_name']
    last_name = request.POST['last_name']
    alias = request.POST['alias']
    birth_date  = request.POST['birth_date']


    if (User.objects.IsRegistrationValid(first_name, last_name, alias, email,birth_date, password, confirm_password, request)):
        user = User(first_name=first_name, last_name=last_name, alias=alias, email=email, birth_date=birth_date, password=User.objects.EncryptPassword(password))
        user.save()

        user = User.objects.Login(email, password, request)

        if (user != 0):
            request.session['user_id'] = user.id
            request.session['num_pages'] = 0
            request.session['current_page'] = 0
            request.session['start_page'] = 0
            request.session['end_page'] = 0
            request.session['search_criteria'] =''
            request.session['name'] = ''

            return redirect('/')
    else:
        return render(request, 'property_search_app/login.html', context={'first_name':first_name, 'last_name':last_name, 'email':email, 'birth_date':birth_date, 'alias':alias})


def logout(request):

    try:
        del request.session['user_id']
        del request.session['num_pages']
        del request.session['current_page']
        del request.session['search_criteria']
        del request.session['start_page']
        del request.session['end_page']
    except Exception as e:
        pass

    return redirect('/')
