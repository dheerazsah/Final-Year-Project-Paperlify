
#Import necessary modules and classes from Django

#Database conncetion handling in Django 
from django.db import connection
#Function and classes for rendering views and handling HTTP responses
from django.shortcuts import render, redirect, HttpResponse
#User model for managing user related information
from django.contrib.auth.models import User
#Message framework for displaying information to the user
from django.contrib import messages
#Function and classes for user authentication
from django.contrib.auth import authenticate, login, logout
#Decorator for requring login to access certain views
from django.contrib.auth.decorators import login_required
#Importing expression module for pattern matching and validation
import re

import nltk
nltk.download('punkt')

#Import UserActivityLog model from the current app
from .models import UserActivityLog
#Module for sending email in Django
from django.core.mail import send_mail
#Utility functions for generating random strings
from django.utils.crypto import get_random_string
#Module for working wiht time and time zones in Django
from django.utils import timezone
#Exception handling for MultiVlaueDictKeyError
from django.utils.datastructures import MultiValueDictKeyError

from django.contrib.auth.hashers import make_password


# Create your views here.
#@login_required(login_url='login')

#View function for handling user signup requests 
def signupPage(request):
    #Check if the request method is POST 
    if request.method == 'POST':
        #Extract the user input from the POST data
        username = request.POST.get('username')
        fname = request.POST.get('fname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        #Check if any required field is empty and display an error message 
        if not username or not fname or not password or not password:
            return render(request, 'signup.html', {'error': 'Enter your username, first name, email, and password.'})

        #Password Complexity Requirements to check if th passowrd mee
        if not (re.search("[A-Z]", password) and re.search("[0-9]", password) and re.search("[!@#$%^&*]", password)):
            return render(request, 'signup.html', {'error': 'Password must contain at least one uppercase letter, one symbol, and one number.'})
        
        #Check if the entered password and confirm password matches 
        if password != confirm_password:
            return render(request, 'signup.html', {'error': 'Password did not match.'})

        #Check if the name contains only alphanumeric characters and spaces
        if not all(char.isalpha() or char.isspace() for char in fname):
            return render(request, 'signup.html', {'error': 'Name must contain alphabetic characters with spaces.'})
        
        #Check if the username already exists
        if User.objects.filter(username=username):
            return render(request, 'signup.html', {'error': 'Username already exists. Please try a new username.'})

        #Check if the email address already exists 
        if User.objects.filter(email=email):
            return render(request, 'signup.html', {'error': 'Email already exists. Please try a new email.'})

        # Email Validation
        #Check if the email format is valid using a regular expression
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return render(request, 'signup.html', {'error': 'Invalid email format. Please provide a valid email.'})

        else:
            # If there are no error messages, create the user account
            myuser = User.objects.create_user(username, email, password)
            myuser.first_name = fname
            myuser.save()

            # Log the user's signup activity
            UserActivityLog.objects.create(
                user=myuser,  
                activity='signup',
                ip_address=request.META.get('REMOTE_ADDR')
            )
            return render(request, 'login.html', {'success': 'Your account has been created successfully.'})
    #Render the signup.html template if the request method is not POST
    return render(request, 'signup.html')


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not username or not password:
            return render(request, 'login.html', {'error': 'Enter your username and password.'})
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
                return render(request, 'login.html', {'error': 'Invalid username or password.'})
    return render(request, 'login.html')

def forgotpassword(request):
    return render(request, 'forgotpassword.html')

def send_otp(request):
    if request.method == 'POST':
        email = request.POST['email']
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM auth_user WHERE email = %s", [email])
            row = cursor.fetchone()

        if row:
            user_id = row[0]
            username = row[1]
            db_email = row[4]

            otp = get_random_string(length=6, allowed_chars='1234567890')

            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE auth_user SET otp = %s, otp_created_at = %s WHERE id = %s",
                    [otp, timezone.now(), user_id]
                )

            subject = 'Forget Password'
            
            message = f'Hello {username},<br><br>'
            message += 'You requested a password reset. Please use the following OTP to proceed:<br><br>'
            message += f'<strong>OTP: {otp}</strong><br><br>'
            message += 'This OTP is valid for 15 minutes.<br>'
            message += 'If you did not request a password reset, please ignore this email.<br><br>'
            message += 'Thank You!'

            from_email = 'noreply'
            recipient_list = [db_email]

            send_mail(subject, message, from_email, recipient_list, html_message=message)

            return render(request, 'forgotpassword.html', {'otp_sent': True, 'email': db_email})
        else:
            return render(request, 'forgotpassword.html', {'user_not_found': True, 'error': 'Email not found!'})
    else:
        return render(request, 'forgotpassword.html', {'otp_sent': False, 'otp_verified': False})
    
def verify_otp(request):
    if request.method == 'POST':
        try:
            email = request.POST['email']
            otp_entered = request.POST['otp']

            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM auth_user WHERE email = %s AND otp = %s AND otp_created_at >= %s",
                    [email, otp_entered, timezone.now() - timezone.timedelta(minutes=15)]
                )
                row = cursor.fetchone()

            if row:
                user_id = row[0]
                with connection.cursor() as cursor:
                    cursor.execute("UPDATE auth_user SET otp_verified = TRUE WHERE id = %s", [user_id])

                return render(request, 'resetpassword.html', {'otp_verified': True, 'email': email})
            else:
                return render(request, 'forgotpassword.html', {'otp_verified': False, 'email': email})
        except MultiValueDictKeyError:
            return render(request, 'forgotpassword.html', {'otp_verified': False, 'email_not_found': True})
    else:
        return render(request, 'forgotpassword.html', {'otp_verified': False, 'otp_sent': False})

def resetpassword(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password == confirm_password:
            hashed_password = make_password(new_password)
            with connection.cursor() as cursor:
                cursor.execute("UPDATE auth_user SET password = %s WHERE email = %s", [hashed_password, email])

            return redirect('/login')
        else:
            error = "Passwords do not match."
            return render(request, 'resetpassword.html', {'otp_verified': True, 'error': error, 'email': email})
    return render(request, 'resetpassword.html')

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

    # Fetch recent documents
    user_id = request.user.id
    recent_documents = FileUpload.objects.filter(user_id=user_id, summarized_text__isnull=False).order_by('-created_at')[:3]


    # user_id = request.user.id
    # # Filter documents based on the user_id
    # documents = FileUpload.objects.filter(user_id=user_id).order_by('-upload_time')[:3]
    # context = {'documents': documents}

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

            request.session['file_info'] = {
                'id': file_info.id,
                'doc_name': file_info.doc_name,
                'doc_size': file_info.doc_size,
                'doc_type': file_info.doc_type,
            }

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

            # Check if input_text is empty
            if not input_text.strip():
                error_message = "Please upload a file or enter text before summarizing."
                return render(request, 'dashboard.html', {'error_message': error_message})


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
                # file_info = FileUpload(user=request.user)
                # file_info.doc_name = fileName
                # file_info.doc_size = fileSize
                # file_info.doc_type = contentType
                # file_info.extracted_text = input_text
                # file_info.summarized_text = summarized_text
                # file_info.save()

                # Retrieve the existing record using the stored file_info ID
                file_info_id = request.session.get('file_info', {}).get('id')
                if file_info_id:
                    file_info = FileUpload.objects.get(id=file_info_id)

                    # Update the existing record with summarized text
                    file_info.extracted_text = input_text
                    file_info.summarized_text = summarized_text
                    file_info.save()

            # Log the user's activity
            UserActivityLog.objects.create(
                user=request.user,
                activity='summarize',
                ip_address=request.META.get('REMOTE_ADDR')
            )

    # user_id = request.user.id
    #  # Filter documents based on the user_id
    # documents = FileUpload.objects.filter(user_id=user_id).order_by('-upload_time')[:3]
    # context = {'documents': documents}
    
    #return render(request, 'dashboard.html', {'content': content, 'summary': summary, 'recent_documents': recent_documents})
    return render(request, 'dashboard.html', {'content': content, 'summary': summary})



def mydocuments(request):
    user_id = request.user.id
    # Filter documents based on the user_id and summarized_text__isnull=False
    context = {'documents': FileUpload.objects.filter(user_id=user_id, summarized_text__isnull=False).order_by('-created_at')}
    return render(request, 'mydocuments.html', context)
    # user = request.user 
    # with connection.cursor() as cursor:
    #     cursor.execute("SELECT * FROM document WHERE user_id = '" + str(user.id) + "'") #str(user.id) = typecast
    #     data = cursor.fetchall()

    # myDocs = []
    # for row in data:
    #     text = row[6]
    #     if text is not None:
    #         words = text.split()
    #         if len(words) > 25:
    #             text = ' '.join(words[:25]) + '... See more'
    #     else:
    #         text = row[6]

    #     doc = {
    #         'title': row[2],  # Assuming the title is in the third column (index 2)
    #         'time': row[7],   # Assuming the time is in the eighth column (index 7)
    #         'text': text, 
    #     }
    #     myDocs.append(doc)

    # context = {
    #     'documents': myDocs,
    # }

    # return render(request, 'mydocuments.html', context)

def document_detail(request, slug):
    context={}
    try:
        document_obj = FileUpload.objects.filter(slug = slug).first()
        context['document_obj'] = document_obj

    except Exception as e:
        print(e)
    return render(request, 'document.html', context)

def search(request):
    # return HttpResponse('This is a search')
    user_id = request.user.id
    query = request.GET.get('query')
    # Filter documents based on the user_id and the correct field name ('doc_name' in this case)
    context = {'documents': FileUpload.objects.filter(user_id=user_id, doc_name__icontains=query)}
    return render(request, 'search.html', context)


def dashboard2nd(request):
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
            fileName = uploadfile.name
            fileSize = uploadfile.size
            contentType = uploadfile.content_type

            # Save upload information to the database
            file_info = FileUpload(
                user=request.user,
                doc_name=uploadfile.name,
                doc_size=uploadfile.size,
                doc_type=uploadfile.content_type
            )
            file_info.save()

            request.session['file_info'] = {
                'id': file_info.id,
                'doc_name': file_info.doc_name,
                'doc_size': file_info.doc_size,
                'doc_type': file_info.doc_type,
            }

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

            elif uploadfile.name.endswith(('.doc', '.docx')):
                content = docx2txt.process(uploadfile)
                file_info.extracted_text = content
                file_info.save()

            elif uploadfile.name.endswith('.pdf'):
                content = ''
                pdf_reader = PdfReader(uploadfile)
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    content += page.extract_text()
                file_info.extracted_text = content
                file_info.save()

        if 'summarize' in request.POST:
            input_text = request.POST.get('input_text', '')

            stringText = input_text  # Use input_text instead of request.GET['newText']
            formattedStringText = re.sub('[^a-zA-Z]', ' ', stringText)
            formattedStringText = re.sub('\s+', ' ', formattedStringText)

            sentences = nltk.sent_tokenize(stringText)

            frequencyDictionary = {}
            stopwords = nltk.corpus.stopwords.words('english')

            for word in nltk.word_tokenize(formattedStringText):
                if word not in stopwords and word not in frequencyDictionary:
                    frequencyDictionary.update({word: 1})
                elif word not in stopwords and word in frequencyDictionary:
                    frequencyDictionary[word] += 1

            maxFrequencyValue = max(frequencyDictionary.values())
            for word in frequencyDictionary:
                frequencyDictionary[word] = frequencyDictionary[word] / maxFrequencyValue

            scores = {}
            for sentence in sentences:
                for word in nltk.word_tokenize(sentence.lower()):
                    if word in frequencyDictionary.keys() and sentence not in scores:
                        scores.update({sentence: frequencyDictionary[word]})
                    elif word not in frequencyDictionary.keys():
                        continue
                    else:
                        scores[sentence] += frequencyDictionary[word]

            sortedSentences = sorted(scores, key=scores.get, reverse=True)

            summary = ''
            for i in range(0, len(sortedSentences) // 10 + 1):
                summary += sortedSentences[i]

            if summary and len(summary) > 0:
                # Retrieve the existing record using the stored file_info ID
                file_info_id = request.session.get('file_info', {}).get('id')
                if file_info_id:
                    file_info = FileUpload.objects.get(id=file_info_id)

                    # Update the existing record with summarized text
                    file_info.extracted_text = input_text
                    file_info.summarized_text = summary
                    file_info.save()

            # Log the user's activity
            UserActivityLog.objects.create(
                user=request.user,
                activity='summarize',
                ip_address=request.META.get('REMOTE_ADDR')
            )

    return render(request, 'dashboard2nd.html', {'content': content, 'summary': summary})


from django.contrib.auth import update_session_auth_hash
@login_required
def profile(request):
    user = request.user
    
    if request.method == 'POST':
        if 'update_profile' in request.POST:
            # user.username = request.POST.get('username')
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
                    return redirect('login')
                    
                else:
                    messages.error(request, 'New password and confirmation do not match')
            else:
                messages.error(request, 'Current password is incorrect')

        if 'delete_account' in request.POST:
            # Log the user's activity for account deletion
            UserActivityLog.objects.create(
                user=user,
                activity='delete_account',
                ip_address=request.META.get('REMOTE_ADDR')
            )
            user.is_active = False  # Deactivate the user account
            user.save()
            messages.success(request, 'Account deleted successfully')
            return redirect('login')


    context = {
        'user': user
    }
    return render(request, 'profile.html', context)



def test(request):
    user_id = request.user.id
    # Filter documents based on the user_id
    context = {'documents': FileUpload.objects.filter(user_id=user_id)}
    return render(request, 'test.html', context)


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

