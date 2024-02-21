
#Import necessary modules and classes from Django

#Database conncetion handling in Django 
from django.db import connection
#Function and classes for rendering views and handling HTTP responses
from django.shortcuts import render, redirect, HttpResponse
from django.http import Http404
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
from django.core.validators import EmailValidator
from django.contrib.sessions.models import Session
from functools import wraps
from django.views.decorators.cache import never_cache

import nltk
nltk.download('punkt')
nltk.download('stopwords')

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
from django.template.loader import render_to_string


#################################################################
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six
class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return(
            six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.is_active)
        )
account_activation_token = AccountActivationTokenGenerator()

from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
from django.contrib.auth import update_session_auth_hash


#from django.core.files.storage import FileSystemStorage
from .models import FileUpload  # Import the model
import docx2txt
from PyPDF2 import PdfReader
from django.shortcuts import render
import requests
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
import os

# Create your views here.
#@login_required(login_url='login')

def not_logged_in(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return function(request, *args, **kwargs)
        else:
            # Redirect authenticated users to a specific URL, like the dashboard
            return redirect('/dashboard')
    return wrap
        
#View function for handling user signup requests 
@not_logged_in
def signupPage(request):
    #Check if the request method is POST 
    if request.method == 'POST':
        #Extract the user input from the POST data
        username = request.POST.get('username').strip()
        fname = request.POST.get('fname').strip()
        email = request.POST.get('email').strip()
        password = request.POST.get('password').strip()
        confirm_password = request.POST.get('confirm_password').strip()

        #Check if any required field is empty and display an error message 
        if not username or not fname or not password or not password:
            messages.error(request, 'Enter your username, first name, email, and password.')
            return render(request, 'signup.html')

        #Password Complexity Requirements to check if the passowrd is complex
        if not (re.search("[A-Z]", password) and re.search("[0-9]", password) and re.search("[!@#$%^&*]", password) and re.search("\s", password)):
            messages.error(request, 'Password must contain at least one uppercase letter, one symbol, and one number.')
            return render(request, 'signup.html')
        
        #Check if the entered password and confirm password matches 
        if password != confirm_password:
            messages.error(request, 'Password did not match.')
            return render(request, 'signup.html')
        
        # Check if the new full name meets the minimum length requirement
        if len(fname) < 6:
            messages.error(request, 'Full Name must be at least 6 characters long.')
            return render(request, 'signup.html')

        #Check if the name contains only alphanumeric characters and spaces
        if not all(char.isalpha() or (char.isspace() and not prev_char.isspace()) for prev_char, char in zip([''] + list(fname), fname)):
            messages.error(request, 'Name must contain alphabetic characters with spaces.')
            return render(request, 'signup.html')
        
        # Check if the new username meets the minimum length requirement
        if len(username) < 4:
            messages.error(request, 'Username must be at least 4 characters long.')
            return render(request, 'signup.html')
        
        # Check if the username already exists and does not contain spaces
        if ' ' in username:
            messages.error(request, 'Username cannot contain spaces.')
            return render(request, 'signup.html')
            
        #Check if the username already exists
        if User.objects.filter(username=username):
            messages.error(request, 'Username already exists. Please try a new username.')
            return render(request, 'signup.html')
        

        #Check if the email address already exists 
        if User.objects.filter(email=email):
            messages.error(request, 'Email already exists. Please try a new email.')
            return render(request, 'signup.html')

        # Email Validation
        #Check if the email format is valid using a regular expression
        # if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        #     messages.error(request, 'Invalid email format. Please provide a valid email.')
        #     return render(request, 'signup.html')
        
        #Django's EmailValidator for additional validation
        validator = EmailValidator(message='Enter a valid email address.')
        try:
            validator(email)
        except ValidationError:
            messages.error(request, 'Invalid email format. Please provide a valid email.')
            return render(request, 'signup.html')

        else:
            # If there are no error messages, create the user account
            user = User.objects.create_user(username, email, password)
            user.first_name = fname
            # Set is_active to False initially
            user.is_active = False 
            user.save()


            # Log the user's signup activity
            UserActivityLog.objects.create(
                user=user,  
                activity='signup',
                ip_address=request.META.get('REMOTE_ADDR')
            )

            subject = 'Activate Your Account'
            message = render_to_string("email.html", {
                'user': user.username,
                'domain': get_current_site(request).domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
                'protocol': 'https' if request.is_secure() else 'http'

            })
            from_email = 'paperlify@gmail.com'
            recipient_list = [user.email]
            #email = EmailMessage(subject, message, to=[to_email])
            email = EmailMessage(subject, message, from_email, recipient_list)

            if email.send():
                messages.success(request, 'Verfiy your email account via the link provided to your mail.')

            # message = f'Your account has been deleted. To reactivate it, click on the link below:\n\n'\
            #           f'{request.build_absolute_uri("reactivate_account/")}token={reactivation_token}'
            
            else:
                messages.error(request, f'Problem sending email')

            # Send a welcome email to the user
            # subject = 'Welcome to Paperlify'
            # message = f'Thank you for signing up, {fname}!\n\nYour account has been created successfully.'
            # from_email = 'paperlify@gmail.com'
            # recipient_list = [db_email]
            # send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        
            return render(request, 'login.html')

    #Render the signup.html template if the request method is not POST
    return render(request, 'signup.html')

#@not_logged_in
@never_cache
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username').strip()
        password = request.POST.get('password').strip()
        
        if not username or not password:
            messages.error(request, 'Enter your username and password.')
            return render(request, 'login.html')
        else:
            try:
                user = User.objects.get(username=username)
                if user.is_active:
                    user = authenticate(request, username=username, password=password)
                    if user is not None:
                        login(request, user)

                        # Log the user's activity
                        UserActivityLog.objects.create(
                            user=user, 
                            activity='login',
                            ip_address=request.META.get('REMOTE_ADDR')
                        )

                        return redirect('dashboard')
                    
                    else:
                        messages.error(request, 'Invalid password.')
                        return render(request, 'login.html')
                
                else:
                    messages.error(request, 'Your account is deactivated or requires email verification.')
                    return render(request, 'login.html')
            
            except User.DoesNotExist:
                messages.error(request, 'Username doesnot exist.')
                return render(request, 'login.html')
            
    return render(request, 'login.html')

def error_404(request, expection):
    return render(request, '4040.html')

@not_logged_in
def forgotpassword(request):
    return render(request, 'forgotpassword.html')

@not_logged_in
def send_otp(request):
    if request.method == 'POST':
        try:
            email = request.POST['email']
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM auth_user WHERE email = %s", [email])
                row = cursor.fetchone()

            if row:
                user_id = row[0]
                username = row[1]
                db_email = row[4]
                is_active = row[9]

                if is_active:
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

                    messages.success(request, 'An OTP has been sent to your email. Please check your inbox.')
                    return render(request, 'forgotpassword.html', {'otp_sent': True, 'email': db_email})
                
                else:
                    messages.error(request, 'Your account is deactivated. Please reactivate your account.')
                    return render(request, 'forgotpassword.html', {'otp_sent': False})

            else:
                raise ValueError('Email not found!')
                #return render(request, 'forgotpassword.html', {'user_not_found': True, 'error': 'Email not found!'})
        except ValueError as ve:
            messages.error(request, f'{str(ve)} Please make sure you entered a valid email.')
            return render(request, 'forgotpassword.html', {'otp_sent': False})
        # except Exception as e:
        #     messages.error(request, f'Something went wrong: {str(e)}')
        #     return render(request, 'forgotpassword.html', {'otp_sent': False})
    else:
        return render(request, 'forgotpassword.html', {'otp_sent': False, 'otp_verified': False})
    
@not_logged_in
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
                messages.error(request, 'Invalid OTP. Please try again.')
                return render(request, 'forgotpassword.html', {'otp_verified': False, 'email': email})
        except MultiValueDictKeyError:
            messages.error(request, 'Email or OTP not provided.')
            return render(request, 'forgotpassword.html', {'otp_verified': False, 'email_not_found': True})
    else:
        return render(request, 'forgotpassword.html', {'otp_verified': False, 'otp_sent': False})

@not_logged_in
def resetpassword(request):
    if request.method == 'POST':
        try:
            email = request.POST.get('email').strip()
            new_password = request.POST.get('new_password').strip()
            confirm_password = request.POST.get('confirm_password').strip()

            if new_password == confirm_password:
                if not (re.search("[A-Z]", new_password) and re.search("[0-9]", new_password) and re.search("[!@#$%^&*]", new_password) and re.search("\s", new_password)):
                    error = "Password must contain at least one uppercase letter, one symbol, and one number."
                    messages.error(request, error)
                    return render(request, 'resetpassword.html', {'otp_verified': True, 'error': error, 'email': email})

                hashed_password = make_password(new_password)
                with connection.cursor() as cursor:
                    cursor.execute("UPDATE auth_user SET password = %s WHERE email = %s", [hashed_password, email])

                messages.success(request, "Password changed successfully. You can now login with your new password.")
                return redirect('/login')
            else:
                error = "Passwords do not match."
                messages.error(request, error)
                return render(request, 'resetpassword.html', {'otp_verified': True, 'error': error, 'email': email})
        except Exception as e:
            error = "Something went wrong while resetting your password. Please try again later."
            messages.error(request, error)
            return render(request, 'resetpassword.html', {'otp_verified': True, 'error': error, 'email': email})
    return render(request, 'resetpassword.html')

# def homepage(request):
#     return render(request, 'homepage.html')


API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
HEADERS = {"Authorization": "Bearer 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"}

@never_cache
@login_required(login_url='login')
def dashboard(request):
    user_id = request.user.id
    # Filter documents based on the user_id and summarized_text__isnull=False
    context = {'documents': FileUpload.objects.filter(user_id=user_id, summarized_text__isnull=False, is_deleted=False).order_by('-created_at')[:3]}
    #context = {'documents': FileUpload.objects.filter(user_id=user_id, summarized_text__isnull=False).order_by('-created_at')}
    content = ''
    summary = None
    active_button = request.session.get('active_button', 'hugface') 
    if request.method == "POST":
        button_clicked = request.POST.get("button")
        if button_clicked == "hugface":
            active_button = "hugface"
            print("Hugging Face button clicked")  # Print to console
            success_message = f"You are using Hugging Face for summarization."
            messages.info(request, success_message)
            # Store active_button in session
            request.session['active_button'] = active_button  
        elif button_clicked == "nltk":
            active_button = "nltk"
            print("NLTK Library button clicked")  # Print to console
            success_message = f"You are using NLTK for summarization."
            messages.info(request, success_message)
            # Store active_button in session
            request.session['active_button'] = active_button  

    return render(request, 'dashboard.html', {'content': content, 'summary': summary, 'active_button': active_button, 'context':context})

@never_cache
@login_required(login_url='login')
def update_library(request):
    if request.method == 'POST':
        
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})

# import pythoncom
#from win32com import client
#from django.conf import settings
@never_cache
@login_required(login_url='login')
def upload_file(request):
    user_id = request.user.id
    # Filter documents based on the user_id and summarized_text__isnull=False
    context = {'documents': FileUpload.objects.filter(user_id=user_id, summarized_text__isnull=False, is_deleted=False).order_by('-created_at')[:3]}
    content = ''
    summary = None
    file_info = None
    # Retrieve active_button from session
    active_button = request.session.get('active_button', 'hugface') 

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

                # Check if a file with the same name already exists
                existing_files = FileUpload.objects.filter(doc_name=fileName)
                if existing_files.exists():
                    # Append a number to the file name if it already exists
                    #fileName = f"{os.path.splitext(fileName)[0]}-{existing_files.count() + 1}{os.path.splitext(fileName)[1]}"
                    # If file with same name exists, append a unique number to make it unique
                    fileName, file_extension = os.path.splitext(fileName)
                    count = 1
                    while True:
                        newfileName = f"{fileName}-{count}{file_extension}"
                        if not FileUpload.objects.filter(doc_name=newfileName).exists():
                            fileName = newfileName
                            break
                        count += 1

                # Save the file to the file system
                # file_info = FileUpload(
                #     user=user,
                #     doc_name=uploadfile.name,
                #     doc_size=uploadfile.size,
                #     doc_type=uploadfile.content_type
                # )
                # file_info.save()
                file_info = FileUpload.objects.create(
                    user=user,
                    doc_name=fileName,
                    doc_size=fileSize,
                    doc_type=contentType
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

                # elif uploadfile.name.endswith(('.doc')):
                #     try:
                #          # Initialize the COM library
                #         pythoncom.CoInitialize()
                        
                #         # Create a new Word application
                #         word_app = client.Dispatch("Word.Application")
                #         word_app.Visible = False
                        
                #         # Open the document
                #         doc_path = os.path.join(settings.MEDIA_ROOT, uploadfile.name)
                #         doc = word_app.Documents.Open(doc_path)
                        
                #         # Extract text from the document
                #         content = doc.Content.Text
                        
                #         # Close the document and Word application
                #         doc.Close()
                #         word_app.Quit()

                    # except Exception as e:
                    #     error_message = "Error processing the uploaded Word document."
                    #     messages.error(request, error_message)
                    #     print(f"Error processing doc file: {str(e)}")

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
    
    return render(request, 'dashboard.html', {'content': content, 'summary': summary, 'active_button': active_button, 'context': context})
    #return JsonResponse({'content': content, 'summary': summary})

from nltk.tokenize import sent_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
nltk.download('wordnet')

@never_cache
@login_required(login_url='login')
def summarize_text(request):
    user_id = request.user.id
    # Filter documents based on the user_id and summarized_text__isnull=False
    context = {'documents': FileUpload.objects.filter(user_id=user_id, summarized_text__isnull=False, is_deleted=False).order_by('-created_at')[:3]}
    content = ''
    summary = None
    file_info = None
    # Retrieve active_button from session
    active_button = request.session.get('active_button', 'hugface')  

    if request.method == 'POST':
        try:
            input_text = request.POST.get('input_text', '')
            

            if active_button == 'hugface':

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
                #     "parameters": {
                #     "truncation": "only_first"
                # }
                }

                '''
                {"content": "", "summary": {"error": "Input is too long for this model, shorten your input or use 'parameters': {'truncation': 'only_first'} 
                to run the model only on the first part.", "warnings": ["There was an inference error: unknown error: index out of range in self", 
                "Token indices sequence length is longer than the specified maximum sequence length for this model (3149 > 1024). Running this sequence 
                through the model will result in indexing errors"]}}
                '''
                response = requests.post(API_URL, headers=HEADERS, json=payload)
                summary = response.json()

                if summary and len(summary) > 0:
                    summarized_text = summary[0].get('summary_text', '') #summary_text
                # file_info = FileUpload(user=request.user)
                # file_info.doc_name = fileName
                # file_info.doc_size = fileSize
                # file_info.doc_type = contentType
                # file_info.extracted_text = input_text
                # file_info.summarized_text = summarized_text
                # file_info.save()
                    
                # Update file_info if needed
                file_info_id = request.session.get('file_info', {}).get('id')
                if file_info_id:
                    file_info = FileUpload.objects.get(id=file_info_id)
                    file_info.extracted_text = input_text
                    file_info.summarized_text = summarized_text
                    file_info.save()

                # Log the user's activity
                UserActivityLog.objects.create(
                    user=request.user,
                    activity='summarize using Hugging Face',
                    ip_address=request.META.get('REMOTE_ADDR')
                )
                    
            elif active_button == 'nltk':
                
                #Text Preprocessing 
                input_text = sent_tokenize(input_text)
                # Assuming input_text contains the tokenized sentences
                formatted_sentences = []

                emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"  # curly loop/scissors
                           u"\U000024C2-\U0001F251"  # metro station/accept symbols
                           "]+", flags=re.UNICODE)

                url_pattern = re.compile(r'https?://\S+|www\.\S+')

                #Removes the special characters from the sentences
                for sentence in input_text:
                    formatted_sentence = re.sub('[^a-zA-Z\s\'.]', '', sentence)  # Remove special characters except spaces and periods
                    formatted_sentence = emoji_pattern.sub(r' ', formatted_sentence)  # Remove emojis
                    formatted_sentence = url_pattern.sub(r'', formatted_sentence)  # Remove URLs
                    formatted_sentence = re.sub('\s+', ' ', formatted_sentence)  # Remove extra whitespaces
                    formatted_sentence = re.sub(r'\. ', '. ', formatted_sentence)  # Add a space after each full stop
                    formatted_sentences.append(formatted_sentence.strip())  # Strip leading/trailing whitespaces and append to the list

                #Sentence Tokenization
                #The input text is tokenized into sentences using NLTK's sent_tokenize function
                #sentences = nltk.sent_tokenize(stringText)

                #Frequency Analysis
                #Performs frequency analysis on the words in the input text. 
                frequencyDictionary = {}
                #stopwords = set(stopwords.words('english'))
                stopwords = nltk.corpus.stopwords.words('english')
                # Initialize lemmatizer and stemmer
                lemmatizer = WordNetLemmatizer()
                stemmer = PorterStemmer()


                for sentence in formatted_sentences:
                    words = nltk.word_tokenize(sentence)
                    for word in words:
                        if word.lower() not in stopwords and word.isalpha():
                            # Lemmatize and stem the word
                            lemma_word = lemmatizer.lemmatize(word.lower())
                            stemmed_word = stemmer.stem(word.lower())
                            # Update frequency dictionary
                            if stemmed_word not in frequencyDictionary:
                                frequencyDictionary[stemmed_word] = 1
                            else:
                                frequencyDictionary[stemmed_word] += 1



                maxFrequencyValue = max(frequencyDictionary.values())
                for word in frequencyDictionary:
                    frequencyDictionary[word] = frequencyDictionary[word] / maxFrequencyValue
                    
                #The sentences are scored based on the normalized frequencies of the words they contain.
                scores = {}
                for sentence in formatted_sentences:
                    for word in nltk.word_tokenize(sentence.lower()):
                    # Lemmatize and stem the word
                        lemma_word = lemmatizer.lemmatize(word)
                        stemmed_word = stemmer.stem(word)
                        if stemmed_word in frequencyDictionary.keys() and sentence not in scores:
                            scores.update({sentence: frequencyDictionary[stemmed_word]})
                        elif word not in frequencyDictionary.keys():
                            continue
                        else:
                            scores[sentence] += frequencyDictionary[stemmed_word]

                #Summary generation
                #Sentences are sorted based on their scores, and a summary is generated by selecting the top 10% of sentences.
                sortedSentences = sorted(scores, key=scores.get, reverse=True)

                summary = ''
                for i in range(0, len(sortedSentences) // 10 + 1):
                    summary += sortedSentences[i]  + ' '

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
                    activity='summarize using NLTK library',
                    ip_address=request.META.get('REMOTE_ADDR')
                )

            else:
                # Summarize the content using the Hugging Face model
                payload = {
                    "inputs": input_text,
                #     "parameters": {
                #     "truncation": "only_first"
                # }
                }

                response = requests.post(API_URL, headers=HEADERS, json=payload)
                summary = response.json()

                if summary and len(summary) > 0:
                    summarized_text = summary[0].get('summary_text', '') #summary_text generated_text
                # file_info = FileUpload(user=request.user)
                # file_info.doc_name = fileName
                # file_info.doc_size = fileSize
                # file_info.doc_type = contentType
                # file_info.extracted_text = input_text
                # file_info.summarized_text = summarized_text
                # file_info.save()
                    
                # Update file_info if needed
                file_info_id = request.session.get('file_info', {}).get('id')
                if file_info_id:
                    file_info = FileUpload.objects.get(id=file_info_id)
                    file_info.extracted_text = input_text
                    file_info.summarized_text = summarized_text
                    file_info.save()
            
                # Log the user's activity
                UserActivityLog.objects.create(
                    user=request.user,
                    activity='summarize using Hugging Face',
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
    return render(request, 'dashboard.html', {'content': content, 'summary': summary, 'active_button': active_button, 'context': context})

# def mydocuments(request):
#     user_id = request.user.id
#     # Filter documents based on the user_id and summarized_text__isnull=False
#     context = {'documents': FileUpload.objects.filter(user_id=user_id, summarized_text__isnull=False).order_by('-created_at')}
#     return render(request, 'mydocuments.html', context)


from datetime import datetime, timedelta
from django.db.models import Q
@never_cache
@login_required(login_url='login')
def mydocuments(request):
    user_id = request.user.id

    today = datetime.now().date()
    yesterday = today - timedelta(days=1)

    today_documents = FileUpload.objects.filter(
        user_id=user_id,
        summarized_text__isnull=False,
        created_at__date=today,
        is_deleted=False,
    ).order_by('-created_at')

    yesterday_documents = FileUpload.objects.filter(
        user_id=user_id,
        summarized_text__isnull=False,
        created_at__date=yesterday,
        is_deleted=False,
    ).exclude(id__in=today_documents.values_list('id', flat=True)
    ).order_by('-created_at')

    previous_documents = FileUpload.objects.filter(
        user_id=user_id,
        summarized_text__isnull=False,
        is_deleted=False,
    ).exclude(
        Q(created_at__date=today) |
        Q(created_at__date=yesterday)
    ).order_by('-created_at')

    context = {
        'today_documents': today_documents,
        'yesterday_documents': yesterday_documents,
        'previous_documents': previous_documents,
        'today_documents_available': bool(today_documents),
        'yesterday_documents_available': bool(yesterday_documents),
        'previous_documents_available': bool(previous_documents),
    }

    return render(request, 'mydocuments.html', context)


from django.shortcuts import get_object_or_404
def delete_document(request, doc_id):
    if request.method == 'POST':
        try:
            if 'confirm_delete' in request.POST:
                document = get_object_or_404(FileUpload, pk=doc_id)
                document.is_deleted = True  # Soft delete the document
                document.save()
                # Redirect to mydocuments view after deletion
                messages.success(request, 'Document deleted successfully.')
                return redirect('mydocuments')
            else:
                #return JsonResponse({'error': 'Confirmation not received'}, status=400)
                messages.error(request, 'Confirmation not received. Document not deleted.')
                return redirect('mydocuments')
            
        except Exception as e:
            messages.error(request, f'An error occurred while deleting the document: {str(e)}')
            return redirect('mydocuments')
    else:
        error_message = 'Method not allowed'
        return render(request, 'error_template.html', {'error_message': error_message})
        #return JsonResponse({'error': 'Method not allowed'}, status=405)

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

@never_cache
@login_required(login_url='login')
def document_detail(request, slug):
    context={}
    try:
        document_obj = FileUpload.objects.filter(slug = slug, is_deleted=False, user=request.user).first()
        if not document_obj:
            # If the document does not exist, raise a 404 error
            raise Http404("Document does not exist or you don't have permission to access it.")
        
        context['document_obj'] = document_obj

    except Exception as e:
        print(e)
    return render(request, 'document.html', context)

'''
def search(request):
    # return HttpResponse('This is a search')
    user_id = request.user.id
    query = request.GET.get('query')
    # Filter documents based on the user_id and the correct field name ('doc_name' in this case)
    context = {'documents': FileUpload.objects.filter(user_id=user_id, doc_name__icontains=query)}
    return render(request, 'search.html', context)
'''
@never_cache
@login_required(login_url='login')
def search(request):
    user_id = request.user.id
    query = request.GET.get('query')
    payload = []
    if query:
         # Fetch both doc_name and slug fields from the database
        documents = list(FileUpload.objects.filter(user_id=user_id, doc_name__icontains=query, is_deleted=False, summarized_text__isnull=False).values('doc_name', 'slug'))
        for document in documents:
            payload.append(document)
    return JsonResponse({'status': 200, 'data': payload})


@never_cache
@login_required(login_url='login')
def profile(request):
    user = request.user
    if request.method == 'POST':
        if 'update_profile' in request.POST:
            new_username = request.POST.get('username').strip() 
            new_full_name = request.POST.get('fullname').strip() 

            # Check if the new username meets the minimum length requirement
            if len(new_username) < 4:
                messages.error(request, 'Username must be at least 4 characters long.')
                return render(request, 'profile.html', {'user': user, 'button_disabled': True})
            
            # Check if there are any spaces in the username
            if ' ' in new_username:
                messages.error(request, 'Username cannot contain spaces.')
                return render(request, 'profile.html', {'user': user, 'button_disabled': True})

            # Check if the new full name meets the minimum length requirement
            if len(new_full_name) < 6:
                messages.error(request, 'Full Name must be at least 6 characters long.')
                return render(request, 'profile.html', {'user': user, 'button_disabled': True})
            
            # Check if the name contains only alphanumeric characters and spaces
            if not all(char.isalpha() or (char.isspace() and not prev_char.isspace()) for prev_char, char in zip([''] + list(new_full_name), new_full_name)):
                messages.error(request, 'Full Name must contain alphabetic characters.')
                return render(request, 'profile.html', {'user': user, 'button_disabled': True})
                
            try:
                existing_username = User.objects.get(username=new_username)
                if existing_username != user:
                    messages.error(request, 'Username already exists. Please choose a different username.')
                    return render(request, 'profile.html', {'user': user, 'button_disabled': True})
                
                # Check if any changes are made to the user's profile
                if (new_full_name != user.first_name or new_username != user.username):
                    # Update the user's profile
                    user.username = new_username
                    user.first_name = new_full_name
                    user.save()
                    messages.success(request, 'Profile updated successfully')
                

                else:
                     messages.info(request, 'No changes were made to the profile')

            except User.DoesNotExist:
                # If the new username doesn't exist, continue updating the profile
                user.username = new_username
                user.first_name = new_full_name
                user.save()
                messages.success(request, 'Profile updated successfully')

                # Log the user's activity for profile update
                UserActivityLog.objects.create(
                    user=user,
                    activity='update_profile',
                    ip_address=request.META.get('REMOTE_ADDR')
                )

            except Exception as e:
                messages.error(request, f' {str(e)} An error occurred while updating your profile. Please try again later.')

        if 'change_password' in request.POST:
            # Password change handling
            current_password = request.POST.get('current_password').strip()
            new_password = request.POST.get('new_password').strip().strip()
            confirm_password = request.POST.get('confirm_password').strip()

            # Validate the current password
            if user.check_password(current_password):
                # Check if the new password is different from the current password
                if new_password != current_password:
                    # Check password complexity requirements
                    if (re.search("[A-Z]", new_password) and
                        re.search("[0-9]", new_password) and
                        re.search("[!@#$%^&*]", new_password) and
                        re.search("\s", new_password)):
                          
                        if new_password == confirm_password:
                            user.set_password(new_password)
                            user.save()
                            update_session_auth_hash(request, user)  # Update the user's session
                            # Clear the session
                            #request.session.flush()
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
                        messages.error(request, 'Password must contain at least one uppercase letter, one symbol, and one number.')

                else:
                    messages.error(request, 'New password should be different from the current password')
            else:
                messages.error(request, 'Current password is incorrect')

    context = {'user': user, 'button_disabled': True}
    return render(request, 'profile.html', context)


@login_required
def confirmpassword(request):
    if request.method == 'POST':
        entered_password = request.POST.get('confirm_password')
        user = request.user
        if user.check_password(entered_password):
            # Password matches, proceed with account deactivation
            user.is_active = False
            user.save()

            # Log the user's activity for account deactivation
            UserActivityLog.objects.create(
                user=user,
                activity='deactivate_account',
                ip_address=request.META.get('REMOTE_ADDR')
            )

            # Send email notification about account deactivation
            subject = 'Account Deactivation Confirmation'
            message = render_to_string("email.html", {
                'user': user.username,
                'domain': get_current_site(request).domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
                'protocol': 'https' if request.is_secure() else 'http'
            })
            from_email = 'paperlify@gmail.com'
            recipient_list = [user.email]
            email = EmailMessage(subject, message, from_email, recipient_list)

            if email.send():
                # End the session
                request.session.flush()
                messages.info(request, f'Account deactivated successfully. If you want to reactivate, check your email.')
                return redirect('login')
            else:
                messages.error(request, f'Problem sending email')

        else:
            # Password does not match
            messages.error(request, 'Password does not match. Please try again.')
            return render(request, 'confirmpassword.html')
    else:
        return render(request, 'confirmpassword.html')


from .models import User
def activate_account(request, uidb64, token):
    User = get_user_model()
    try: 
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        # Extract the timestamp from the token
        try:
            timestamp = int(token.split('-')[-1])
            activation_time = datetime.fromtimestamp(timestamp, tz=timezone.utc)
        except ValueError:
            activation_time = None

        # Check if the activation link has expired
        if activation_time is not None:
            time_elapsed = timezone.now() - activation_time
            if time_elapsed > timedelta(days=30):
                messages.error(request, 'Activation link has expired.')
                return redirect('login')
        user.is_active = True
        user.save()

        # Log the user's activity for account reactivation
        UserActivityLog.objects.create(
            user=user,
            activity='activate_account',
            ip_address=request.META.get('REMOTE_ADDR')
        )

        messages.success(request, 'Account activated successfully. Now you can login to your account.')
        return redirect('login')
    else: 
        messages.error(request, 'Activation link is invalid.')

    #messages.success(request, 'Account reactivated successfully. You can now login.')
    return redirect('login')  # Redirect to login



# def test(request):
#     user_id = request.user.id
#     # Filter documents based on the user_id
#     context = {'documents': FileUpload.objects.filter(user_id=user_id)}
#     return render(request, 'test.html', context)

@not_logged_in
def terms_conditions(request):
    return render(request, 'terms&conditions.html')

@never_cache
@login_required(login_url='login')
def logoutUser(request):
    #if request.user.is_authenticated:
    # Log the user's activity
    UserActivityLog.objects.create(
        user=request.user,
        activity='logout',
        ip_address=request.META.get('REMOTE_ADDR')
    )
    logout(request)

    messages.success(request, 'You are logged out successfully.')
    return redirect('login')

