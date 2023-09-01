from django.shortcuts import render, HttpResponse

# Create your views here.
def index(request):
    return render(request, 'index.html')
    #return HttpResponse("This is a home page")

def login(request):
    return HttpResponse("This is a login page")
