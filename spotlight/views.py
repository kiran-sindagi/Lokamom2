from django.shortcuts import render
from .models import WomenInSpotlight 
from .forms import ContactUsForm
from django.core.mail import send_mail
from django.shortcuts import render, redirect
import os


def WomenInSpotlight_list(request):
    """
    Renders a page displaying all WomenInSpotlights.
    """
    WomenInSpotlights = WomenInSpotlight.objects.all()
    return render(request, 'WomenInSpotlight_list.html', {'WomenInSpotlights': WomenInSpotlights})

def ContactUs_view(request):
    if request.method == 'POST':
        form = ContactUsForm(request.POST)
        
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone_number']
            reason = form.cleaned_data['reason']
            add_msg = form.cleaned_data['additional_message']
            
            # --- 1. Prepare and Send Admin Notification Email ---
            admin_subject = f"New Women In Spotlight Contact Request from {name}"
            admin_plain_message = (
                f"{name} wants to contact for women in spotlight.\n\n"
                f"--- Details ---\n"
                f"Name: {name}\n"
                f"Email: {email}\n"
                f"Phone: {phone}\n\n"
                f"Reason: {reason}\n"
                f"Additional Message:\n{add_msg}"
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
        form = ContactUsForm()
        
    return render(request, 'contactus.html', {'form': form})

