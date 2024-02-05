
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

            # Send a welcome email to the user
            # subject = 'Welcome to Paperlify'
            # message = f'Thank you for signing up, {fname}!\n\nYour account has been created successfully.'
            # from_email = 'paperlify@gmail.com'
            # recipient_list = [db_email]
            # send_mail(subject, message, from_email, recipient_list, fail_silently=False)
            
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

def error_404(request, expection):
    return render(request, '4040.html')

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
from django.core.exceptions import ValidationError
import os

API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
HEADERS = {"Authorization": "Bearer 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"}

'''
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
        try:
            user = request.user
            fileName = ''
            fileSize = 0
            contentType = ''

            if 'file' in request.FILES:
                try:
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
                        try:
                            with uploadfile.open() as file:
                                content = file.read().decode('utf-8')
                                if not content.strip():  # Check if the text is empty
                                    messages.error(request, "No text found in the uploaded document.")
                                    # Remove the file if no text is found
                                    os.remove(uploadfile.path)
                                    return render(request, 'dashboard.html', {'content': content, 'summary': summary})
                                file_info.extracted_text = content  
                                file_info.save()  
                                #return render(request, 'dashboard.html', {'content': content})
                        except Exception as e:
                            error_message = "Error reading the uploaded text file."
                            messages.error(request, error_message)
                            print(f"Error reading text file: {str(e)}")

                    elif uploadfile.name.endswith(('.doc', '.docx')):
                        try:
                            content = docx2txt.process(uploadfile)
                            if not content.strip():
                                messages.error(request, "No text found in the uploaded document.")
                                # Remove the file if no text is found
                                os.remove(uploadfile.path)
                                return render(request, 'dashboard.html', {'content': content, 'summary': summary})
                            file_info.extracted_text = content  
                            file_info.save() 
                            #return render(request, 'dashboard.html', {'content': content})
                        except Exception as e:
                            error_message = "Error processing the uploaded Word document."
                            messages.error(request, error_message)
                            print(f"Error processing doc/docx file: {str(e)}")

                    elif uploadfile.name.endswith('.pdf'):
                        try:
                            content = ''
                            pdf_reader = PdfReader(uploadfile)
                            for page_num in range(len(pdf_reader.pages)):
                                page = pdf_reader.pages[page_num]
                                content += page.extract_text()
                            if not content.strip():
                                messages.error(request, "No text found in the uploaded document.")
                                # Remove the file if no text is found
                                os.remove(uploadfile.path)
                                return render(request, 'dashboard.html', {'content': content, 'summary': summary})
                            file_info.extracted_text = content
                            file_info.save()  
                            #return render(request, 'dashboard.html', {'content': content})

                            # Show a success message
                            success_message = "File uploaded successfully."
                            messages.success(request, success_message)

                        except Exception as e:
                            error_message = "Error reading the uploaded PDF document."
                            messages.error(request, error_message)
                            print(f"Error reading PDF file: {str(e)}")
                    else:
                        messages.error(request, "Unsupported file format")

                except ValidationError as e:
                    error_message = "Validation error during file upload."
                    messages.error(request, error_message)
                    print(f"Validation error: {str(e)}")
                except Exception as e:
                    error_message = "Unexpected error during file upload."
                    messages.error(request, error_message)
                    print(f"Unexpected error: {str(e)}")
            
            else:
                # No file selected, show an error message
                error_message = "Please select a file before uploading."
                messages.error(request, error_message)

            if 'summarize' in request.POST:
                try:
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
                    
                except requests.RequestException as e:
                    error_message = "Error connecting to the summarization service. Please try again later."
                    messages.error(request, error_message)
                    print(f"Request error: {str(e)}")
                except Exception as e:
                    error_message = "Unexpected error during summarization."
                    messages.error(request, error_message)
                    print(f"Unexpected error: {str(e)}")
        except ValidationError as e:
            error_message = "Validation error in the form submission."
            messages.error(request, error_message)
            print(f"Validation error: {str(e)}")
        except Exception as e:
            error_message = "Unexpected error in the form submission."
            messages.error(request, error_message)
            print(f"Unexpected error: {str(e)}")
            
        # user_id = request.user.id
        #  # Filter documents based on the user_id
        # documents = FileUpload.objects.filter(user_id=user_id).order_by('-upload_time')[:3]
        # context = {'documents': documents}
    
    #return render(request, 'dashboard.html', {'content': content, 'summary': summary, 'recent_documents': recent_documents})
    return render(request, 'dashboard.html', {'content': content, 'summary': summary})
'''
from django.http import JsonResponse
def dashboard(request):
    content = ''
    summary = None

    '''
    library = '' 
    if library == 'hugging_face':
        info_message = "You are using Hugging Face"
        messages.info(request, info_message)
        print(info_message)
    elif library == 'nltk':
        info_message = "You are using NLTK"
        messages.info(request, info_message)
        print(info_message)
    else:
        info_message = "Invalid Library"
        messages.info(request, info_message)
        print(info_message)
    #return JsonResponse({'message': message})
    '''
    return render(request, 'dashboard.html', {'content': content, 'summary':summary})

def update_library(request):
    if request.method == 'POST':
        selected_library = request.POST.get('selected_library')
        print(f'Selected Library: {selected_library}')
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})

import pythoncom
from win32com import client
from django.conf import settings
def upload_file(request):
    content = ''
    summary = None
    file_info = None

    if request.method == 'POST':
        try:
            user = request.user
            fileName = ''
            fileSize = 0
            contentType = ''

            if 'file' in request.FILES:
                uploadfile = request.FILES['file']

                fileName = uploadfile.name
                fileSize = uploadfile.size
                contentType = uploadfile.content_type

                # Save the file to the file system
                file_info = FileUpload(
                    user=user,
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
                # Uncomment and customize based on your UserActivityLog model
                # UserActivityLog.objects.create(
                #     user=user,
                #     activity='upload document',
                #     ip_address=request.META.get('REMOTE_ADDR')
                # )

                # Extract and display content for supported file types
                if uploadfile.name.endswith('.txt'):
                    try:
                        with uploadfile.open() as file:
                            content = file.read().decode('utf-8')
                            if not content.strip():
                                messages.error(request, "No text found in the uploaded document.")
                                os.remove(uploadfile.path)
                                return JsonResponse({'content': content, 'summary': summary})
                            file_info.extracted_text = content
                            file_info.save()
                    except Exception as e:
                        error_message = "Error reading the uploaded text file."
                        messages.error(request, error_message)
                        print(f"Error reading text file: {str(e)}")

                elif uploadfile.name.endswith(('.docx')):
                    try:
                        content = docx2txt.process(uploadfile)
                        if not content.strip():
                            messages.error(request, "No text found in the uploaded document.")
                            os.remove(uploadfile.path)
                            return JsonResponse({'content': content, 'summary': summary})
                        file_info.extracted_text = content
                        file_info.save()

                    except Exception as e:
                        error_message = "Error processing the uploaded Word document."
                        messages.error(request, error_message)
                        print(f"Error processing doc/docx file: {str(e)}")

                elif uploadfile.name.endswith(('.doc')):
                    try:
                         # Initialize the COM library
                        pythoncom.CoInitialize()
                        
                        # Create a new Word application
                        word_app = client.Dispatch("Word.Application")
                        word_app.Visible = False
                        
                        # Open the document
                        doc_path = os.path.join(settings.MEDIA_ROOT, uploadfile.name)
                        doc = word_app.Documents.Open(doc_path)
                        
                        # Extract text from the document
                        content = doc.Content.Text
                        
                        # Close the document and Word application
                        doc.Close()
                        word_app.Quit()

                    except Exception as e:
                        error_message = "Error processing the uploaded Word document."
                        messages.error(request, error_message)
                        print(f"Error processing doc file: {str(e)}")

                elif uploadfile.name.endswith('.pdf'):
                    try:
                        content = ''
                        pdf_reader = PdfReader(uploadfile)
                        for page_num in range(len(pdf_reader.pages)):
                            page = pdf_reader.pages[page_num]
                            content += page.extract_text()
                        if not content.strip():
                            messages.error(request, "No text found in the uploaded document.")
                            os.remove(uploadfile.path)
                            return JsonResponse({'content': content, 'summary': summary})
                        file_info.extracted_text = content
                        file_info.save()

                        # Show a success message
                        success_message = "File uploaded successfully."
                        messages.success(request, success_message)

                    except Exception as e:
                        error_message = "Error reading the uploaded PDF document."
                        messages.error(request, error_message)
                        print(f"Error reading PDF file: {str(e)}")
                else:
                    messages.error(request, "Unsupported file format")

            else:
                error_message = "Please select a file before uploading."
                messages.error(request, error_message)

        except ValidationError as e:
            error_message = "Validation error during file upload."
            messages.error(request, error_message)
            print(f"Validation error: {str(e)}")
        except Exception as e:
            error_message = "Unexpected error during file upload."
            messages.error(request, error_message)
            print(f"Unexpected error: {str(e)}")
    
    return render(request, 'dashboard.html', {'content': content, 'summary': summary})
    #return JsonResponse({'content': content, 'summary': summary})


def summarize_text(request):
    content = ''
    summary = None
    file_info = None

    if request.method == 'POST':
        try:
            input_text = request.POST.get('input_text', '')

            # Check if input_text is empty
            '''
            if not input_text.strip():
                error_message = "Please upload a file or enter text before summarizing."
                #return render(request, 'dashboard.html', {'error_message': error_message})
                messages.error(request, error_message)
                print(f"Request error: {str(e)}")
            '''

            # Summarize the content using the Hugging Face model
            payload = {
                "inputs": input_text,
            }
            response = requests.post(API_URL, headers=HEADERS, json=payload)
            summary = response.json()

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
                    
        except requests.RequestException as e:
            error_message = "Error connecting to the summarization service. Please try again later."
            messages.error(request, error_message)
            print(f"Request error: {str(e)}")

        except Exception as e:
            error_message = "Please upload a file or enter text before summarizing."
            messages.error(request, error_message)
            print(f"Unexpected error: {str(e)}")

        '''
        except ValidationError as e:
            error_message = "Validation error in the form submission."
            messages.error(request, error_message)
            print(f"Validation error: {str(e)}")
        except Exception as e:
            error_message = "Unexpected error in the form submission."
            messages.error(request, error_message)
            print(f"Unexpected error: {str(e)}")
        '''
            
        # user_id = request.user.id
        #  # Filter documents based on the user_id
        # documents = FileUpload.objects.filter(user_id=user_id).order_by('-upload_time')[:3]
        # context = {'documents': documents}

    #return JsonResponse({'content': content, 'summary': summary})
    return render(request, 'dashboard.html', {'content': content, 'summary': summary})

# def mydocuments(request):
#     user_id = request.user.id
#     # Filter documents based on the user_id and summarized_text__isnull=False
#     context = {'documents': FileUpload.objects.filter(user_id=user_id, summarized_text__isnull=False).order_by('-created_at')}
#     return render(request, 'mydocuments.html', context)


from datetime import datetime, timedelta
from django.db.models import Q

def mydocuments(request):
    user_id = request.user.id

    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    last_week = today - timedelta(weeks=1)
    last_month = today - timedelta(weeks=4)

    today_documents = FileUpload.objects.filter(
        user_id=user_id,
        summarized_text__isnull=False,
        created_at__date=today
    ).order_by('-created_at')

    yesterday_documents = FileUpload.objects.filter(
        user_id=user_id,
        summarized_text__isnull=False,
        created_at__date=yesterday
    ).exclude(id__in=today_documents.values_list('id', flat=True)
    ).order_by('-created_at')

    last_week_documents = FileUpload.objects.filter(
        user_id=user_id,
        summarized_text__isnull=False,
        created_at__date__range=[last_week, yesterday]
    ).exclude(id__in=today_documents.values_list('id', flat=True)
    ).exclude(id__in=yesterday_documents.values_list('id', flat=True)
    ).order_by('-created_at')

    last_month_documents = FileUpload.objects.filter(
        user_id=user_id,
        summarized_text__isnull=False,
        created_at__date__range=[last_month, yesterday]
    ).exclude(id__in=today_documents.values_list('id', flat=True)
    ).exclude(id__in=yesterday_documents.values_list('id', flat=True)
    ).exclude(id__in=last_week_documents.values_list('id', flat=True)
    ).order_by('-created_at')

    previous_documents = FileUpload.objects.filter(
        user_id=user_id,
        summarized_text__isnull=False
    ).exclude(
        Q(created_at__date=today) |
        Q(created_at__date=yesterday) |
        Q(created_at__date__range=[last_week, today]) |
        Q(created_at__date__range=[last_month, today])
    ).order_by('-created_at')

    context = {
        'today_documents': today_documents,
        'yesterday_documents': yesterday_documents,
        'last_week_documents': last_week_documents,
        'last_month_documents': last_month_documents,
        'previous_documents': previous_documents,
        'today_documents_available': bool(today_documents),
        'yesterday_documents_available': bool(yesterday_documents),
        'last_week_documents_available': bool(last_week_documents),
        'last_month_documents_available': bool(last_month_documents),
        'previous_documents_available': bool(previous_documents),
    }

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

            #Text Preprocessing 
            #Removes the special characters from the sentences
            stringText = input_text  # Use input_text instead of request.GET['newText']
            formattedStringText = re.sub('[^a-zA-Z]', ' ', stringText)
            formattedStringText = re.sub('\s+', ' ', formattedStringText)

            #Sentence Tokenization
            #The input text is tokenized into sentences using NLTK's sent_tokenize function
            sentences = nltk.sent_tokenize(stringText)

            #Frequency Analysis
            #Performs frequency analysis on the words in the input text. 
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
                
            #The sentences are scored based on the normalized frequencies of the words they contain.
            scores = {}
            for sentence in sentences:
                for word in nltk.word_tokenize(sentence.lower()):
                    if word in frequencyDictionary.keys() and sentence not in scores:
                        scores.update({sentence: frequencyDictionary[word]})
                    elif word not in frequencyDictionary.keys():
                        continue
                    else:
                        scores[sentence] += frequencyDictionary[word]

            #Summary generation
            #Sentences are sorted based on their scores, and a summary is generated by selecting the top 10% of sentences.
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
            # Generate a unique token for reactivation link
            reactivation_token = User.objects.make_random_password()

            # Save the token and set the account as inactive
            user.reactivation_token = reactivation_token
            user.is_active = False # Deactivate the user account
            user.save()

            subject = 'Account Deleted Confirmation'
            message = f'Your account has been deleted. To reactivate it, click on the link below:\n\n'\
                      f'{request.build_absolute_uri("reactivate_account/")}token={reactivation_token}'
            from_email = 'paperlify@gmail.com'
            recipient_list = [user.email]
            send_mail(subject, message, from_email, recipient_list, fail_silently = False)

            # Log the user's activity for account deletion
            UserActivityLog.objects.create(
                user=user,
                activity='delete_account',
                ip_address=request.META.get('REMOTE_ADDR')
            )
            messages.success(request, 'Account deleted successfully')
            return redirect('login')


    context = {
        'user': user
    }
    return render(request, 'profile.html', context)

def confirmpassword(request):

    return render(request, 'confirmpassword.html')

from .models import ReactivationToken

def reactivate_account(request, token):
    try:
        # Find the user with the provided reactivation token
        user = User.objects.get(reactivation_token=token, is_active=False)
    except User.DoesNotExist:
        # Token is invalid or the account is already active
        messages.error(request, 'Invalid reactivation link')
        return redirect('login')  # Redirect to login or any other page

    # If the token is valid, set the account as active and clear the reactivation token
    user.is_active = True
    user.reactivation_token = ''
    user.save()

    # Log the user's activity for account reactivation
    UserActivityLog.objects.create(
        user=user,
        activity='reactivate_account',
        ip_address=request.META.get('REMOTE_ADDR')
    )

    messages.success(request, 'Account reactivated successfully. You can now login.')
    return redirect('login')  # Redirect to login or any other page



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

