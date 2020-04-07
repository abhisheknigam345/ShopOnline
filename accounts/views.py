from django.shortcuts import render, redirect
from django.contrib import messages
from .models import customer, location, supplier
from django.db import connection
import mysql.connector

from django.contrib.auth.models import User, auth
# Create your views here.

def customer_details(request):
    cursor = connection.cursor()
    if request.method == 'POST':
        CustomerId_id = request.POST['user_id']
        CompanyName = request.POST['CompanyName']
        PhoneNumber = request.POST['PhoneNumber']
        Mobile = request.POST['Mobile']
        Country = request.POST['Country']
        Address = request.POST['Address']
        PostalCode = request.POST['PostalCode']
        LocationId = request.POST['locationid']

        user = customer(CompanyName=CompanyName, PhoneNumber=PhoneNumber, Mobile=Mobile, Country=Country, Address=Address, CustomerId_id=CustomerId_id, PostalCode=PostalCode, LocationId_id=LocationId)
        user.save();
        return redirect('/show')
    else:
        locations = location.objects.all()
        return render(request, 'customer_details.html', {'locations': locations})

def update(request, id):
    if request.method == 'POST':

        customer_update = customer.objects.get(CustomerId_id=id)

        customer_update.CompanyName = request.POST['CompanyName']
        customer_update.PhoneNumber = request.POST['PhoneNumber']
        customer_update.Mobile = request.POST['Mobile']
        customer_update.Country = request.POST['Country']
        customer_update.Address = request.POST['Address']
        customer_update.PostalCode = request.POST['PostalCode']
        customer_update.LocationId_id = request.POST['locationid']

        customer_update.save();

        return redirect('/show')
    else:
        locations = location.objects.all()
        return render(request, 'customer_details_update.html', {'locations': locations})

def show_customer_details(request, id):
    #subcategorys = SubCategory.objects.filter(CategoryId_id=id)
    details = customer.objects.filter(CustomerId_id = id)
    return render(request, "show_customer_details.html", {'details': details})

def logout(request):
    auth.logout(request)
    return redirect('/')

def home(request):
    return render(request, 'home.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        print(user)

        if user is not None:
            #user_details = User.objects.get(username=username)
            if user.last_login is None:
                #auth.login(request, user)
                #return redirect('customer_details')
                auth.login(request, user)
                locations = location.objects.all()
                return render(request, 'customer_details.html', {'userid': user.id, 'locations': locations})
            else:
                auth.login(request, user)
                #return redirect('home')
                return redirect('/show')
        else:
            messages.info(request, 'Invalid Credentials')
            return redirect('login')
    else:
        return render(request, 'login.html')

def register(request):

    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username already taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email already registered')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, password=password1, email=email, first_name=first_name, last_name=last_name)
                user.save();
                messages.info(request, 'User Created, Please Login')
                return redirect('login')
        else:
            messages.info(request, 'Password Not Matching')
            return redirect('register')
    else:
            return render(request, 'register.html')

def supplierregister(request):

    if request.method == 'POST':
        supplier_name = request.POST['supplier_name']
        username = request.POST['username']
        email = request.POST['email']
        Mobile = request.POST['Mobile']
        Country = request.POST['Country']
        Address = request.POST['Address']
        PostalCode = request.POST['PostalCode']
        LocationId = request.POST['locationid']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1==password2:
            if supplier.objects.filter(SupplierUserName=username).exists():
                messages.info(request, 'Username already taken')
                return redirect('supplierregister')
            elif supplier.objects.filter(Email=email).exists():
                messages.info(request, 'Email already registered')
                return redirect('supplierregister')
            else:
                lid = location.objects.get(id=LocationId)
                add = supplier(SupplierUserName=username, SupplierName=supplier_name, Password=password1, Email=email, Mobile=Mobile, Country=Country, Address=Address, LocationId=lid, PostalCode=PostalCode)
                add.save();
                messages.info(request, 'User Created, Please Login')
                return redirect('supplierlogin')
        else:
            messages.info(request, 'Password Not Matching')
            return redirect('supplierregister')
    else:
        locations = location.objects.all()
        return render(request, 'supplierRegister.html', {'locations': locations})

def supplierlogin(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        s_login = supplier.objects.filter(SupplierUserName=username, Password=password)

        if s_login:
            for s in s_login:
                return redirect('/showProductDetails/' + str(s.id))
        else:
            messages.info(request, 'Invalid Credentials')
            return redirect('supplierlogin')
    else:
        return render(request, 'supplierlogin.html')