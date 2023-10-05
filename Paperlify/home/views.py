from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import re

# Create your views here.
@login_required(login_url='login')

def signupPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        fname = request.POST.get('fname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        #error_messages = []  # Create a list to collect error messages

        if not username or not fname or not password or not password:
            return render(request, 'signup.html', {'error': 'Enter your username, first name, email, and password.'})

        # Email Validation
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return render(request, 'signup.html', {'error': 'Invalid email format. Please provide a valid email.'})

        # Password Complexity Requirements
        if not (re.search("[A-Z]", password) and re.search("[0-9]", password) and re.search("[!@#$%^&*]", password)):
            return render(request, 'signup.html', {'error': 'Password must contain at least one uppercase letter, one symbol, and one number.'})

        if password != confirm_password:
            return render(request, 'signup.html', {'error': 'Password did not match.'})

        # Name Validation (Alphabet with spaces)
        if not all(char.isalpha() or char.isspace() for char in fname):
            return render(request, 'signup.html', {'error': 'Name must contain alphabetic characters with spaces.'})

        if User.objects.filter(username=username):
            return render(request, 'signup.html', {'error': 'Username already exists. Please try a new username.'})

        if User.objects.filter(email=email):
            return render(request, 'signup.html', {'error': 'Email already exists. Please try a new email.'})

        # Check if there are any error messages
        # if error_messages:
        #     for message in error_messages:
        #         messages.error(request, message)
        else:
            # If there are no error messages, create the user account
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
        
        if not username or not password:
            return render(request, 'login.html', {'error': 'Enter your username and password'})
        else:
            user = authenticate(request, username = username, password = password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                return render(request, 'login.html', {'error': 'Invalid username or password'})
    return render(request, 'login.html')


#from django.core.files.storage import FileSystemStorage
from .models import FileUpload  # Import the model
import docx2txt
from PyPDF2 import PdfReader

def dashboard(request):
    if request.method == 'POST':
        if 'file' in request.FILES:
            uploadfile = request.FILES['file']
            print(uploadfile.name)
            print(uploadfile.size)
            print(uploadfile.content_type)

            # Save the file to the file system
            # fs = FileSystemStorage()
            # fs.save(uploadfile.name, uploadfile)

            # Save upload information to the database 
            file_info = FileUpload(
                doc_name=uploadfile.name,
                doc_size=uploadfile.size,
                doc_type=uploadfile.content_type
            )
            file_info.save()

            # Extract and display content for supported file types
            if uploadfile.name.endswith('.txt'):
                with uploadfile.open() as file:
                    content = file.read().decode('utf-8')
                    file_info.extracted_text = content  
                    file_info.save()  
                    return render(request, 'dashboard.html', {'content': content})

            elif uploadfile.name.endswith(('.doc', '.docx')):
                content = docx2txt.process(uploadfile)
                file_info.extracted_text = content  
                file_info.save() 
                return render(request, 'dashboard.html', {'content': content})

            elif uploadfile.name.endswith('.pdf'):
                pdf_text = ''
                pdf_reader = PdfReader(uploadfile)
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    pdf_text += page.extract_text()
                file_info.extracted_text = pdf_text  
                file_info.save()  
                return render(request, 'dashboard.html', {'content': pdf_text})
        
        # If 'file' key is not in request.FILES, show an error message
        return render(request, 'dashboard.html', {'error': 'Please select a file to upload.'})

    return render(request, 'dashboard.html')



def mydocuments(request):
    return render(request, 'mydocuments.html')

def document(request):
    return render(request, 'document.html')

def profile(request):
    return render(request, 'profile.html')


def test(request):
    return render(request, 'test.html')


def logoutUser(request):
    logout(request)
    messages.success(request, 'You are logged out successfully.')
    return redirect('login')

