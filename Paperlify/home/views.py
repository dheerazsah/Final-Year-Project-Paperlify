from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
import re

# Create your views here.
def signupPage(request):
    #return render(request, 'signup.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        fname = request.POST.get('fname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

         # Email Validation
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messages.error(request, 'Invalid email format. Please provide a valid email.')

        # Password Complexity Requirements
        if not (re.search("[A-Z]", password) and re.search("[0-9]", password) and re.search("[!@#$%^&*]", password)):
            messages.error(request, 'Password must contain at least one uppercase letter, one symbol, and one number.')

        if password != confirm_password:
            messages.error(request, 'Password did not match.')

        # Name Validation (Alphabet with spaces)
        if not all(char.isalpha() or char.isspace() for char in fname):
            messages.error(request, 'Name must contain alphabetic characters with spaces.')

        if User.objects.filter(username=username):
            messages.error(request, 'Username already exists. Please try a new username.')

        if User.objects.filter(email=email):
            messages.error(request, 'Email already exists. Please try a new email.')

        if not messages.get_messages(request):  # If there are no error messages
            myuser = User.objects.create_user(username, email, password)
            myuser.first_name = fname
            myuser.save()
            messages.success(request, 'Your account has been created successfully')
            return redirect('login')

    return render(request, 'signup.html')


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username = username, password = password)

        if user is not None:
            login(request,user)
            return render(request, 'dashboard.html')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')


def dashboard(request):
    return render(request, 'dashboard.html')

def mydocuments(request):
    return render(request, 'mydocuments.html')

def document(request):
    return render(request, 'document.html')


