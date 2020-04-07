from django.shortcuts import render, redirect
from django.contrib import messages
import mysql.connector
from datetime import datetime

from django.contrib.auth.models import User, auth
# Create your views here.

def home(request):
    return render(request, 'home.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        mydb = mysql.connector.connect(host="localhost", user="root", passwd="root", database="bdmproject")
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM auth_user")
        myresult = mycursor.fetchall()
        i = 0
        for x in myresult:
            if username == x[3] and password == x[1]:
                i = 1
        if i == 1:
            return redirect('home')
        else:
            messages.info(request, 'Invalid Credentials...')
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
        now = datetime.now()

        # if password1==password2:
        #    if User.objects.filter(username=username).exists():
        #        print('Username Taken')
        #    elif User.objects.filter(email=email).exists():
        #        print('Email Taken')
        #    else:
        #        user = User.objects.create_user(username=username, password=password1, email=email, first_name=first_name, last_name=last_name)
        #        user.save();
        #        print('user created')
        # else:
        #    print('password not matching')
        # return redirect('/')
        # else:
        #    return render(request, 'register.html')

        if password1 == password2:
            if (check(username, email)):
                mydb = mysql.connector.connect(host="localhost", user="root", passwd="root", database="bdmproject")
                mycursor = mydb.cursor()
                sql = "INSERT INTO auth_user (password, username, first_name, last_name, email) VALUES (%s, %s, %s, %s, %s)"
                val = (password1, username, first_name, last_name, email)
                mycursor.execute(sql, val)
                mydb.commit()
                messages.info(request, 'User Created, Please login...')
                return redirect('login')
            else:
                messages.info(request, 'Already in use, use different email and username')
                return redirect('register')
        else:
            messages.info(request, 'Password Not Matching...')
            return redirect('register')
    else:
        return render(request, "register.html")

def check(username, email):
        mydb = mysql.connector.connect(host="localhost", user="root", passwd="root", database="bdmproject")
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM auth_user")
        myresult = mycursor.fetchall()
        i = 0
        for x in myresult:
            if username == x[3]:
                i = 1
            elif email == x[6]:
                i = 1
        if i == 0:
            return True
        else:
            return False