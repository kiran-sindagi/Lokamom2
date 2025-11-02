from django import forms

class WorkCareerForm(forms.Form):
    name = forms.CharField(max_length=100, label="Your Name")
    age = forms.IntegerField(label="Age")
    email = forms.EmailField(label="Email ID")
    phone_number = forms.CharField(max_length=10, label="Phone Number")
    qualification = forms.CharField(label="Qualification")
    years_of_experience = forms.IntegerField(label="Years Of Experience")
    CHOICES = [
        ('healthcare', 'Healthcare'),
        ('technology/engineering', 'Technology/Engineering'),
        ('business and finance', 'Business & Finance'),
        ('education', 'Education'),
        ('service', 'Service'),
        ('others','Others')
    ]
    domain = forms.ChoiceField(
        choices=CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Choose your domain"
    )
    elaborate = forms.CharField(max_length=500, label="Please elaborate")

