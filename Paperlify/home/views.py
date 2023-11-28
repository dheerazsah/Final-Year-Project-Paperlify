from django.db import connection
from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import re
from .models import UserActivityLog


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

            # Log the user's activity
            UserActivityLog.objects.create(
                user=myuser,  
                activity='signup',
                ip_address=request.META.get('REMOTE_ADDR')
            )

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

                # Log the user's activity
                UserActivityLog.objects.create(
                    user=user, 
                    activity='login',
                    ip_address=request.META.get('REMOTE_ADDR')
                )

                return redirect('homepage')
            else:
                return render(request, 'login.html', {'error': 'Invalid username or password'})
    return render(request, 'login.html')

def forgotpassword(request):
    return render(request, 'forgotpassword.html')

def homepage(request):
    return render(request, 'homepage.html')


#from django.core.files.storage import FileSystemStorage
from .models import FileUpload  # Import the model
import docx2txt
from PyPDF2 import PdfReader
from django.shortcuts import render
import requests

API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
HEADERS = {"Authorization": "Bearer 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"}

def dashboard(request):
    content = ''
    summary = None
    file_info = None

    if request.method == 'POST':
        user = request.user
        fileName = ''
        fileSize = 0
        contentType = ''

        if 'file' in request.FILES:
            uploadfile = request.FILES['file']
            # print(uploadfile.name)
            # print(uploadfile.size)
            # print(uploadfile.content_type)

            fileName = uploadfile.name
            fileSize = uploadfile.size
            contentType = uploadfile.content_type
            # Save the file to the file system
            # fs = FileSystemStorage()
            # fs.save(uploadfile.name, uploadfile)

            # Save upload information to the database 
            file_info = FileUpload(
                user= request.user,
                doc_name=uploadfile.name,
                doc_size=uploadfile.size,
                doc_type=uploadfile.content_type
            )
            file_info.save()

            # Log the user's activity
            UserActivityLog.objects.create(
                user=request.user,
                activity='upload document',
                ip_address=request.META.get('REMOTE_ADDR')
            )

            # Extract and display content for supported file types
            if uploadfile.name.endswith('.txt'):
                with uploadfile.open() as file:
                    content = file.read().decode('utf-8')
                    file_info.extracted_text = content  
                    file_info.save()  
                    #return render(request, 'dashboard.html', {'content': content})

            elif uploadfile.name.endswith(('.doc', '.docx')):
                content = docx2txt.process(uploadfile)
                file_info.extracted_text = content  
                file_info.save() 
                #return render(request, 'dashboard.html', {'content': content})

            elif uploadfile.name.endswith('.pdf'):
                content = ''
                pdf_reader = PdfReader(uploadfile)
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    content += page.extract_text()
                file_info.extracted_text = content
                file_info.save()  
                #return render(request, 'dashboard.html', {'content': content})
            
        if 'summarize' in request.POST:
            input_text = request.POST.get('input_text', '')

            # Summarize the content using the Hugging Face model
            payload = {
                "inputs": input_text,
            }
            response = requests.post(API_URL, headers=HEADERS, json=payload)
            summary = response.json()

            # Initialize file_info if not created before
            # if not file_info:
            #     #file_info = FileUpload(user=request.user, doc_name=fileName, doc_size=fileSize, doc_type=contentType)
            #     file_info = FileUpload(user=request.user)

            if summary and len(summary) > 0:
                summarized_text = summary[0].get('summary_text', '')
                file_info = FileUpload(user=request.user)
                file_info.doc_name = fileName
                file_info.doc_size = fileSize
                file_info.doc_type = contentType
                file_info.extracted_text = input_text
                file_info.summarized_text = summarized_text
                file_info.save()

            # Log the user's activity
            UserActivityLog.objects.create(
                user=request.user,
                activity='summarize',
                ip_address=request.META.get('REMOTE_ADDR')
            )
    
    return render(request, 'dashboard.html', {'content': content, 'summary': summary})






def mydocuments(request):
    user = request.user 
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM document WHERE user_id = '" + str(user.id) + "'") #str(user.id) = typecast
        data = cursor.fetchall()

    

    myDocs = []
    for row in data:
        text = row[6]
        if text is not None:
            words = text.split()
            if len(words) > 25:
                text = ' '.join(words[:25]) + '... See more'
        else:
            text = row[6]

        doc = {
            'title': row[2],  # Assuming the title is in the third column (index 2)
            'time': row[7],   # Assuming the time is in the eighth column (index 7)
            'text': text, 
        }
        myDocs.append(doc)

    context = {
        'documents': myDocs,
    }

    return render(request, 'mydocuments.html', context)

def document(request):
    query = request.GET.get('query', '')

    documents = FileUpload.objects.filter(doc_name__icontains=query)

    context = {
        'documents': documents,
        'query': query,
    }

    return render(request, 'search_documents.html', context)


def dashboard2nd(request):
    return render(request, 'dashboard2nd.html')



from django.contrib.auth import update_session_auth_hash
def profile(request):
    user = request.user
    
    if request.method == 'POST':
        if 'update_profile' in request.POST:
            #user.username = request.POST.get('username')
            user.first_name = request.POST.get('fullname')
            user.email = request.POST.get('email')
            user.save()
            messages.success(request, 'Profile updated successfully')

            # Log the user's activity for profile update
            UserActivityLog.objects.create(
                user=user,
                activity='update_profile',
                ip_address=request.META.get('REMOTE_ADDR')
            )

        if 'change_password' in request.POST:
            # Password change handling
            current_password = request.POST.get('current_password')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')

            # Validate the current password
            if user.check_password(current_password):
                if new_password == confirm_password:
                    user.set_password(new_password)
                    user.save()
                    update_session_auth_hash(request, user)  # Update the user's session
                    messages.success(request, 'Password changed successfully')

                    # Log the user's activity for password change
                    UserActivityLog.objects.create(
                        user=user,
                        activity='change_password',
                        ip_address=request.META.get('REMOTE_ADDR')
                    )
                    
                else:
                    messages.error(request, 'New password and confirmation do not match')
            else:
                messages.error(request, 'Current password is incorrect')

            return redirect('profile')
    
    context = {
        'user': user
    }
    return render(request, 'profile.html', context)


def test(request):
    return render(request, 'test.html')


def logoutUser(request):
    logout(request)
    
    # Log the user's activity
    UserActivityLog.objects.create(
        user=request.user,
        activity='logout',
        ip_address=request.META.get('REMOTE_ADDR')
    )

    messages.success(request, 'You are logged out successfully.')
    return redirect('login')

