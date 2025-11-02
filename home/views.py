from articles.views import random_articles 
from .forms import ContributeForm, ContactForm
from django.shortcuts import render, redirect
from django.core.mail import send_mail
import os

# Create your views here.
def home(request):
    article_data = random_articles()
    return render(request, 'animated.html', {"article_data":article_data})

def about(request):
    return render(request, 'about.html')

def contribute(request):
    if request.method == 'POST':
        form = ContributeForm(request.POST)
        
        if form.is_valid():
            name = form.cleaned_data['name']
            age = form.cleaned_data['age']
            email = form.cleaned_data['email']
            contribution = form.cleaned_data['contribution']
            elaborate = form.cleaned_data['elaborate']
            
            # --- 1. Prepare and Send Admin Notification Email ---
            admin_subject = f"New Contribution from {name}"
            admin_plain_message = (
                f"You have a new contribution request.\n\n"
                f"--- Details ---\n"
                f"Name: {name}\n"
                f"Age: {age}\n"
                f"Email: {email}\n"
                f"Contribution: {contribution}\n\n"
                f"Elaboration:\n{elaborate}"
            )
            
            user_subject = "Your Request has been Received!"
            if "sessions" in contribution:
                user_plain_message = f"Hi {name},\n\nThank you for showing interest in contributing to our cause. We will contact you shortly.\n Best regards\n Lokamom"
            # --- 2. Prepare and Send User Confirmation Email ---
            elif "articles" in contribution:
                user_plain_message = f"Hi {name},\n\nThank you for showing interest in contributing to our cause. Please share the article in .docx or .pdf format.\n Best regards\n Lokamom"
            elif "monetary" in contribution:
                user_plain_message = f"Hi {name},\n\nThank you for showing interest in contributing to our cause. We will send you the details shortly.\n Best regards\n Lokamom"
            else:
                user_plain_message = f"Hi {name},\n\nThank you for showing interest in contributing to our cause. We will contact you shortly.\n Best regards\n Lokamom"

            try:
                # Send the detailed notification to yourself/admin
                send_mail(
                    subject=admin_subject,
                    message=admin_plain_message,
                    from_email=os.environ.get('EMAIL_HOST_USER'),
                    recipient_list=[os.environ.get('RECIEVER')], # Your admin email
                    fail_silently=False
                )
                
                # Send the confirmation email to the user
                send_mail(
                    subject=user_subject,
                    message=user_plain_message,
                    from_email=os.environ.get('EMAIL_HOST_USER'),
                    recipient_list=[email], # The user's email from the form
                    fail_silently=False
                )

                # Redirect to a success page after emails are sent
                return redirect('successful')

            except Exception as e:
                # If anything goes wrong with email sending, log the error
                print(f"An error occurred while sending email: {e}")
                return redirect('failure_page')
    
    else:
        form = ContributeForm()
        
    return render(request, 'contribute.html', {'form': form})

def successful(request):
    return render(request, "contri_success.html")

def workCareer(request):
    return render(request, "work_coming_soon.html")

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        
        if form.is_valid():
            name = form.cleaned_data['name']
            age = form.cleaned_data['age']
            email = form.cleaned_data['email']
            reason = form.cleaned_data['reason']
            
            # --- 1. Prepare and Send Admin Notification Email ---
            admin_subject = f"New Contact from {name}"
            admin_plain_message = (
                f"You have a new contact request.\n\n"
                f"--- Details ---\n"
                f"Name: {name}\n"
                f"Age: {age}\n"
                f"Email: {email}\n"
                f"Reason:\n{reason}"
            )
            
            user_subject = "Your Request has been Received!"
            user_plain_message = f"Hi {name},\n\nThank you for showing interest. We will contact you shortly.\n Best regards\n Lokamom"

            try:
                # Send the detailed notification to yourself/admin
                send_mail(
                    subject=admin_subject,
                    message=admin_plain_message,
                    from_email=os.environ.get('EMAIL_HOST_USER'),
                    recipient_list=[os.environ.get('RECIEVER')], # Your admin email
                    fail_silently=False
                )
                
                # Send the confirmation email to the user
                send_mail(
                    subject=user_subject,
                    message=user_plain_message,
                    from_email=os.environ.get('EMAIL_HOST_USER'),
                    recipient_list=[email], # The user's email from the form
                    fail_silently=False
                )

                # Redirect to a success page after emails are sent
                return redirect('successful')

            except Exception as e:
                # If anything goes wrong with email sending, log the error
                print(f"An error occurred while sending email: {e}")
                return redirect('failure_page')
    
    else:
        form = ContactForm()
        
    return render(request, 'contact.html', {'form': form})