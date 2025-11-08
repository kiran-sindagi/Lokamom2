from django.shortcuts import render, redirect
from .forms import OneToOneForm, groupSessionForm, stressManagementForm
import os
from django.core.mail import send_mail

# Create your views here.
def Letter(request):
    return render(request, "letter.html")

def whatWeOffer(request):
    return render(request, 'sessions.html')

def oneOnOne(request):
    return render(request, "one.html")

def groupSession(request):
    return render(request, "group.html")

def StressSession(request):
    return render(request, 'stress_management.html')

# your_app/views.py
import os
import datetime
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .forms import OneToOneForm # Make sure to import your form

def oneToOne_view(request):
    if request.method == 'POST':
        form = OneToOneForm(request.POST)
        
        if form.is_valid():
            name = form.cleaned_data['name']
            age = form.cleaned_data['age']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone_number']
            concern = form.cleaned_data['concern']
            
            # --- 1. Prepare and Send Admin Notification Email ---
            admin_subject = f"New 1-on-1 Request from {name}"
            admin_plain_message = (
                f"You have a new one-on-one session request.\n\n"
                f"--- Details ---\n"
                f"Name: {name}\n"
                f"Age: {age}\n"
                f"Email: {email}\n"
                f"Phone: {phone}\n\n"
                f"Concern:\n{concern}"
            )
            
            # --- 2. Prepare and Send User Confirmation Email ---
            user_subject = "Your Request has been Received!"
            user_plain_message = f"Hi {name},\n\nThank you for reaching out. We have successfully received your request and will get in touch with you shortly.\n\nBest regards,\nLokamom"

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
                return redirect('success_page')

            except Exception as e:
                # If anything goes wrong with email sending, log the error
                print(f"An error occurred while sending email: {e}")
                return redirect('failure_page')
    
    else:
        form = OneToOneForm()
        
    return render(request, 'forms/book_1on1.html', {'form': form})


def groupSession_view(request):
    if request.method == 'POST':
        form = groupSessionForm(request.POST)
        
        if form.is_valid():
            name = form.cleaned_data['name']
            age = form.cleaned_data['age']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone_number']
            number_of_people = form.cleaned_data['number_of_people']
            subject = form.cleaned_data['subject']
            elaborate = form.cleaned_data['elaborate']
            
            # --- 1. Prepare and Send Admin Notification Email ---
            admin_subject = f"New Group session Request from {name}"
            admin_plain_message = (
                f"You have a new group session request.\n\n"
                f"--- Details ---\n"
                f"Name: {name}\n"
                f"Age: {age}\n"
                f"Email: {email}\n"
                f"Phone: {phone}\n"
                f"Number of people: {number_of_people}"
                f"Subject: {subject}\n\n"
                f"Elaboration:\n{elaborate}"
            )
            
            # --- 2. Prepare and Send User Confirmation Email ---
            user_subject = "Your Request has been Received!"
            user_plain_message = f"Hi {name},\n\nThank you for reaching out. We have successfully received your request and will get in touch with you shortly.\n\nBest regards,\nLokamom"

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
                return redirect('success_page')

            except Exception as e:
                # If anything goes wrong with email sending, log the error
                print(f"An error occurred while sending email: {e}")
                return redirect('failure_page')
    
    else:
        form = groupSessionForm()
        
    return render(request, 'forms/book_group_session.html', {'form': form})

def stressSession_view(request):
    if request.method == 'POST':
        form = stressManagementForm(request.POST)
        
        if form.is_valid():
            name = form.cleaned_data['name']
            age = form.cleaned_data['age']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone_number']
            number_of_people = form.cleaned_data['number_of_people']
            appointment_date = form.cleaned_data['appointment_date']
            
            # --- 1. Prepare and Send Admin Notification Email ---
            admin_subject = f"New Group session Request from {name}"
            admin_plain_message = (
                f"You have a new stress management session request.\n\n"
                f"--- Details ---\n"
                f"Name: {name}\n"
                f"Age: {age}\n"
                f"Email: {email}\n"
                f"Phone: {phone}\n"
                f"Number of people: {number_of_people}\n"
                f"Appointment Date: {appointment_date}"
            )
            
            # --- 2. Prepare and Send User Confirmation Email ---
            user_subject = "Your Request has been Received!"
            user_plain_message = f"Hi {name},\n\nThank you for reaching out. We have successfully received your request and will get in touch with you shortly.\n\nBest regards,\nLokamom"

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
                return redirect('success_page')

            except Exception as e:
                # If anything goes wrong with email sending, log the error
                print(f"An error occurred while sending email: {e}")
                return redirect('failure_page')
    
    else:
        form = stressManagementForm()
        
    return render(request, 'forms/book_stress_session.html', {'form': form})



# A simple view for the success page
def success_view(request):
    return render(request, 'forms/success.html')

def failure_view(request):
    return render(request, 'forms/failure.html')