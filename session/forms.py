# your_app/forms.py

from django import forms
import datetime

class OneToOneForm(forms.Form):
    name = forms.CharField(max_length=100, label="Your Name")
    age = forms.IntegerField(label="Age")
    email = forms.EmailField(label="Email ID")
    phone_number = forms.CharField(max_length=10, label="Phone Number")
    concern = forms.CharField(widget=forms.Textarea, label="Your Concern")

class groupSessionForm(forms.Form):
    name = forms.CharField(max_length=100, label="Your Name")
    age = forms.IntegerField(label="Age")
    email = forms.EmailField(label="Email ID")
    phone_number = forms.CharField(max_length=10, label="Phone Number")
    number_of_people = forms.IntegerField(label="Number of people")  
    CHOICES = [
        ('parenting', 'Parenting'),
        ('career and motherhood', 'Career and Motherhood'),
        ('children', 'Children'),
        ('relationship with partner after child-birth', 'Relationship with partner after child-birth'),
        ('others','Others')
    ]
    subject = forms.ChoiceField(
        choices=CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Choose"
    )
    elaborate = forms.CharField(max_length=500, label="Please elaborate")

class stressManagementForm(forms.Form):
    name = forms.CharField(max_length=100, label="Your Name")
    age = forms.IntegerField(label="Age")
    email = forms.EmailField(label="Email ID")
    phone_number = forms.CharField(max_length=10, label="Phone Number")
    number_of_people = forms.IntegerField(label="Number of people")
    today_str = datetime.date.today().strftime('%Y-%m-%d')

    appointment_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'min': today_str # This sets the minimum selectable date in the browser
            }
        )
    )

    def clean_appointment_date(self):
        """
        This method provides server-side validation.
        """
        date = self.cleaned_data.get('appointment_date')
        
        # Check if the selected date is in the past
        if date and date < datetime.date.today():
            raise forms.ValidationError("You cannot book an appointment in the past. Please select a future date.")
            
        return date