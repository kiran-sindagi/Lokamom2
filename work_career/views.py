from django.shortcuts import render, redirect
from .forms import WorkCareerForm
import os
from django.core.mail import send_mail

# Create your views here.
def WorkCareerView(request):
    if request.method == 'POST':
        form = WorkCareerForm(request.POST)
        
        if form.is_valid():
            name = form.cleaned_data['name']
            age = form.cleaned_data['age']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone_number']
            qualification = form.cleaned_data['qualification']
            years_of_experience = form.cleaned_data['years_of_experience']
            domain = form.cleaned_data['domain']
            elaborate = form.cleaned_data['elaborate']
            
            # --- 1. Prepare and Send Admin Notification Email ---
            admin_subject = f"New Work & Career Request from {name}"
            admin_plain_message = (
                f"You have a new Work & Career request.\n\n"
                f"--- Details ---\n"
                f"Name: {name}\n"
                f"Age: {age}\n"
                f"Email: {email}\n"
                f"Phone: {phone}\n"
                f"Qualification: {qualification}\n"
                f"Years of Experience: {years_of_experience}\n"
                f"Domain: {domain}\n\n"
                f"Elaboration:\n{elaborate}"
            )
            
            # --- 2. Prepare and Send User Confirmation Email ---
            user_subject = "Your Request has been Received!"
            user_plain_message = f"Hi {name},\n\nThank you for reaching out. Kindly share with us your resume and we will reach out you shortly.\n\nBest regards,\nLokamom"

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
        form = WorkCareerForm()
        
    return render(request, 'work_career_form.html', {'form': form})