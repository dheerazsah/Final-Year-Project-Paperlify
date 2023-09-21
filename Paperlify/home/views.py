from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login

# Create your views here.
def signupPage(request):
    #return render(request, 'signup.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        fname = request.POST.get('fname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_pasword = request.POST.get('confirm_pasword')
        
        myuser = User.objects.create_user(username, email, password)
        myuser.fname = fname

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


