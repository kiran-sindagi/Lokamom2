from django import forms

class ContactUsForm(forms.Form):
    name = forms.CharField(max_length=100, label="Your Name")
    email = forms.EmailField(label="Email ID")
    phone_number = forms.CharField(max_length=10, label="Phone Number")
    OPTIONS = [
        ('to get featured', 'To Get Featured'),
        ('to purchase product', 'To Purchase Product'),
    ]
    reason = forms.ChoiceField(
        choices=OPTIONS,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Reason"
    )
    additional_message = forms.CharField(widget=forms.Textarea, label="Additional Message")
