from django.shortcuts import render, HttpResponse

# Create your views here.
def login(request):
    return render(request, 'login.html')


def signup(request):
    return render(request, 'signup.html')

def dashboard(request):
    return render(request, 'dashboard.html')

def mydocuments(request):
    return render(request, 'mydocuments.html')

def document(request):
    return render(request, 'document.html')


